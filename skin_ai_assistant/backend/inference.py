import numpy as np
import onnxruntime as ort
import cv2
from pathlib import Path
from .config import BEST_MODEL, LABELS_PATH


def _get_providers():
    """
    Prefer GPU if available, but always fall back to CPU.
    """
    providers = ["CPUExecutionProvider"]
    try:
        # If CUDAExecutionProvider is available in this build of onnxruntime
        if "CUDAExecutionProvider" in ort.get_available_providers():
            providers.insert(0, "CUDAExecutionProvider")
    except Exception:
        pass
    return providers


class SkinAIModel:
    def __init__(self):
        self.model_path = BEST_MODEL
        self.labels = []
        if LABELS_PATH.exists():
            self.labels = LABELS_PATH.read_text().splitlines()

        if not self.model_path.exists():
            self.session = None
            print(f"[SkinAIModel] No ONNX model found at {self.model_path}, using fallback.")
        else:
            providers = _get_providers()
            print(f"[SkinAIModel] Loading ONNX from {self.model_path} with providers: {providers}")
            self.session = ort.InferenceSession(
                str(self.model_path),
                providers=providers
            )

    def preprocess(self, img_bytes):
        arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image bytes.")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img = (img - mean) / std
        img = img.transpose(2, 0, 1)  # CHW
        return img[None, ...]

    def predict(self, img_bytes):
        # Fallback if model doesn't exist yet
        if self.session is None:
            return "normal", 0.50

        x = self.preprocess(img_bytes)
        inputs = {self.session.get_inputs()[0].name: x}
        logits = self.session.run(None, inputs)[0][0]
        # Softmax
        logits = logits - np.max(logits)
        exp = np.exp(logits)
        probs = exp / exp.sum()

        idx = int(np.argmax(probs))
        label = self.labels[idx] if idx < len(self.labels) else "unknown"
        return label, float(probs[idx])


MODEL = SkinAIModel()
