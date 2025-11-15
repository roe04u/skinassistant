"""
Comprehensive integration tests for all Skin AI Assistant endpoints.
"""
import io
from PIL import Image


def _make_dummy_image_bytes(color=(128, 180, 220)) -> bytes:
    """Generate a simple in-memory JPEG image for testing."""
    img = Image.new("RGB", (256, 256), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_health_endpoint(client):
    """Test the health check endpoint."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert "service" in data


def test_analyze_with_defaults(client):
    """Test /analyze endpoint with default parameters."""
    img_bytes = _make_dummy_image_bytes()
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}

    resp = client.post("/analyze", files=files)
    assert resp.status_code == 200
    data = resp.json()

    assert "inference_id" in data
    assert "condition" in data
    assert "confidence" in data
    assert "skin_type" in data
    assert "fitzpatrick" in data
    assert "ethnicity" in data


def test_analyze_with_full_profile(client):
    """Test /analyze endpoint with complete user profile."""
    img_bytes = _make_dummy_image_bytes(color=(200, 150, 120))
    files = {"file": ("test_full.jpg", img_bytes, "image/jpeg")}
    data = {
        "skin_type": "combination",
        "fitzpatrick": "IV",
        "ethnicity": "south_asian",
    }

    resp = client.post("/analyze", files=files, data=data)
    assert resp.status_code == 200
    result = resp.json()

    assert result["skin_type"] == "combination"
    assert result["fitzpatrick"] == "IV"
    assert result["ethnicity"] == "south_asian"
    assert isinstance(result["confidence"], (int, float))
    assert 0.0 <= result["confidence"] <= 1.0


def test_feedback_correct_prediction(client):
    """Test feedback endpoint with correct prediction."""
    # First create an inference
    img_bytes = _make_dummy_image_bytes()
    files = {"file": ("feedback_test.jpg", img_bytes, "image/jpeg")}
    analyze_resp = client.post("/analyze", files=files)
    inference_id = analyze_resp.json()["inference_id"]

    # Submit positive feedback
    fb_data = {
        "inference_id": inference_id,
        "is_correct": "true",
    }
    fb_resp = client.post("/feedback", data=fb_data)
    assert fb_resp.status_code == 200
    assert fb_resp.json()["ok"] is True


def test_feedback_incorrect_with_correction(client):
    """Test feedback endpoint with incorrect prediction and correction."""
    # First create an inference
    img_bytes = _make_dummy_image_bytes()
    files = {"file": ("correction_test.jpg", img_bytes, "image/jpeg")}
    analyze_resp = client.post("/analyze", files=files)
    inference_id = analyze_resp.json()["inference_id"]

    # Submit negative feedback with correction
    fb_data = {
        "inference_id": inference_id,
        "is_correct": "false",
        "corrected_condition": "rosacea",
    }
    fb_resp = client.post("/feedback", data=fb_data)
    assert fb_resp.status_code == 200
    assert fb_resp.json()["ok"] is True


def test_feedback_nonexistent_inference(client):
    """Test feedback endpoint with non-existent inference ID."""
    fb_data = {
        "inference_id": "nonexistent-id-12345",
        "is_correct": "true",
    }
    fb_resp = client.post("/feedback", data=fb_data)
    # Should return 404 for non-existent inference
    assert fb_resp.status_code == 404
    result = fb_resp.json()
    assert "detail" in result


def test_admin_inferences_no_filter(client):
    """Test admin inferences endpoint without filters."""
    # Create some test inferences first
    for i in range(3):
        img_bytes = _make_dummy_image_bytes()
        files = {"file": (f"admin_test_{i}.jpg", img_bytes, "image/jpeg")}
        client.post("/analyze", files=files)

    # Query admin endpoint
    resp = client.get("/admin/inferences")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 3

    # Check structure of first record
    if data:
        rec = data[0]
        assert "id" in rec
        assert "predicted_condition" in rec
        assert "predicted_confidence" in rec
        assert "user_skin_type" in rec
        assert "user_fitzpatrick" in rec
        assert "user_ethnicity" in rec
        assert "needs_review" in rec
        assert "created_at" in rec


def test_admin_inferences_needs_review_filter(client):
    """Test admin inferences endpoint with needs_review filter."""
    # Create inference and mark it for review
    img_bytes = _make_dummy_image_bytes()
    files = {"file": ("review_needed.jpg", img_bytes, "image/jpeg")}
    analyze_resp = client.post("/analyze", files=files)
    inference_id = analyze_resp.json()["inference_id"]

    # Mark as incorrect to trigger needs_review
    fb_data = {
        "inference_id": inference_id,
        "is_correct": "false",
        "corrected_condition": "dermatitis",
    }
    client.post("/feedback", data=fb_data)

    # Query with needs_review=true
    resp = client.get("/admin/inferences", params={"needs_review": "true"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

    # All returned records should have needs_review=True
    for rec in data:
        if rec["needs_review"] is not None:
            assert rec["needs_review"] is True


def test_admin_inferences_limit(client):
    """Test admin inferences endpoint with limit parameter."""
    # Create multiple inferences
    for i in range(5):
        img_bytes = _make_dummy_image_bytes()
        files = {"file": (f"limit_test_{i}.jpg", img_bytes, "image/jpeg")}
        client.post("/analyze", files=files)

    # Query with limit=2
    resp = client.get("/admin/inferences", params={"limit": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 2


def test_multiple_inferences_different_profiles(client):
    """Test creating multiple inferences with different user profiles."""
    profiles = [
        {"skin_type": "oily", "fitzpatrick": "I", "ethnicity": "unspecified"},
        {"skin_type": "dry", "fitzpatrick": "VI", "ethnicity": "west_african"},
        {"skin_type": "sensitive", "fitzpatrick": "III", "ethnicity": "mixed_african_asian"},
    ]

    inference_ids = []
    for i, profile in enumerate(profiles):
        img_bytes = _make_dummy_image_bytes()
        files = {"file": (f"profile_test_{i}.jpg", img_bytes, "image/jpeg")}
        resp = client.post("/analyze", files=files, data=profile)
        assert resp.status_code == 200
        data = resp.json()
        inference_ids.append(data["inference_id"])

        # Verify profile was recorded correctly
        assert data["skin_type"] == profile["skin_type"]
        assert data["fitzpatrick"] == profile["fitzpatrick"]
        assert data["ethnicity"] == profile["ethnicity"]

    # Verify all inferences exist in admin endpoint
    resp = client.get("/admin/inferences", params={"limit": 100})
    assert resp.status_code == 200
    all_records = resp.json()

    returned_ids = [rec["id"] for rec in all_records]
    for inf_id in inference_ids:
        assert inf_id in returned_ids
