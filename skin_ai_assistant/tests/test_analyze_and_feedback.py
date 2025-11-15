import io
from PIL import Image


def _make_dummy_image_bytes() -> bytes:
    """
    Generate a simple in-memory JPEG image for testing.
    """
    img = Image.new("RGB", (256, 256), color=(128, 180, 220))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_analyze_and_feedback_flow(client):
    # 1. Call /analyze with fake image and profile
    img_bytes = _make_dummy_image_bytes()
    files = {
        "file": ("test.jpg", img_bytes, "image/jpeg")
    }
    data = {
        "skin_type": "oily",
        "fitzpatrick": "V",
        "ethnicity": "west_african",
    }

    resp = client.post("/analyze", files=files, data=data)
    assert resp.status_code == 200, resp.text
    out = resp.json()

    assert "inference_id" in out
    assert "condition" in out
    assert "confidence" in out
    assert "skin_type" in out
    assert "fitzpatrick" in out
    assert "ethnicity" in out
    assert out["skin_type"] == "oily"
    assert out["fitzpatrick"] == "V"
    assert out["ethnicity"] == "west_african"

    inference_id = out["inference_id"]

    # 2. Send feedback: mark as incorrect and give a corrected condition
    fb_data = {
        "inference_id": inference_id,
        "is_correct": "false",
        "corrected_condition": "acne",
    }
    fb_resp = client.post("/feedback", data=fb_data)
    assert fb_resp.status_code == 200, fb_resp.text
    fb_out = fb_resp.json()
    assert fb_out.get("ok") is True
