from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DB_URL = os.getenv("SKINAI_DB_URL", f"sqlite:///{BASE_DIR/'skin_ai.db'}")

MODELS_DIR = BASE_DIR / "models"
BEST_MODEL = MODELS_DIR / "best" / "skin_model.onnx"
LABELS_PATH = MODELS_DIR / "best" / "class_names.txt"

MODELS_DIR.mkdir(exist_ok=True, parents=True)
(BEST_MODEL.parent).mkdir(exist_ok=True, parents=True)