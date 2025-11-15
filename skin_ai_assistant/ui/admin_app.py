import os
import requests
from pathlib import Path
from PIL import Image
import streamlit as st
import time

API_BASE = os.getenv("SKINAI_API_URL", "http://127.0.0.1:8000")
BASE_DIR = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Skin AI Admin", page_icon="[ADMIN]", layout="wide")
st.title("[ADMIN] Skin AI Admin Dashboard")

# Check backend health with retry
def check_backend_health(max_retries=3, delay=2):
    """Check if backend is reachable."""
    for attempt in range(max_retries):
        try:
            health_resp = requests.get(f"{API_BASE}/health", timeout=5)
            if health_resp.status_code == 200:
                return True
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(delay)
    return False

# Display connection status
with st.spinner("Connecting to backend..."):
    backend_online = check_backend_health()

if not backend_online:
    st.error(f"❌ Cannot connect to backend at {API_BASE}")
    st.info("**Troubleshooting:**")
    st.markdown("""
    1. Ensure the backend is running: `python run_backend.py`
    2. Check the backend URL: `{}`
    3. Verify the backend port matches BACKEND_PORT environment variable
    """.format(API_BASE))
    st.stop()

st.success(f"✅ Connected to backend: {API_BASE}")

st.sidebar.header("Filters")
needs_review_opt = st.sidebar.selectbox(
    "Needs review?",
    ["All", "Yes", "No"],
    index=0,
)

params = {"limit": 100}
if needs_review_opt == "Yes":
    params["needs_review"] = "true"
elif needs_review_opt == "No":
    params["needs_review"] = "false"

try:
    resp = requests.get(f"{API_BASE}/admin/inferences", params=params, timeout=60)
    if resp.status_code != 200:
        st.error(f"Admin API error {resp.status_code}: {resp.text}")
        st.stop()
    records = resp.json()
except Exception as e:
    st.error(f"Failed to fetch inferences: {e}")
    st.info("The backend may still be starting up. Please refresh the page in a few seconds.")
    st.stop()

st.write(f"Found **{len(records)}** inference records.")

for rec in records:
    exp_label = f"{rec['id']} | Pred: {rec['predicted_condition']} | Corrected: {rec['corrected_condition']} | Needs review: {rec['needs_review']}"
    with st.expander(exp_label):
        cols = st.columns([1, 2])

        with cols[0]:
            # try to show image if present
            img_path = BASE_DIR / rec["image_path"]
            if img_path.exists():
                img = Image.open(img_path)
                st.image(img, caption=str(img_path.name), use_column_width=True)
            else:
                st.warning(f"Image not found: {img_path}")

        with cols[1]:
            st.write(f"**Created:** {rec['created_at']}")
            st.write(f"**User skin type:** {rec['user_skin_type']}")
            st.write(f"**User Fitzpatrick:** {rec['user_fitzpatrick']}")
            st.write(f"**User ethnicity:** {rec['user_ethnicity']}")
            st.write(f"**Predicted confidence:** {rec['predicted_confidence']}")

            st.markdown("---")
            st.write("Override / confirm feedback:")

            colc1, colc2 = st.columns(2)
            with colc1:
                choice = st.radio(
                    f"Prediction correctness ({rec['id']})",
                    ["Unknown", "Correct", "Incorrect"],
                    index=0,
                    key=f"corr_{rec['id']}",
                    horizontal=True,
                )
            with colc2:
                corrected_condition = st.selectbox(
                    f"Correct condition ({rec['id']})",
                    ["", "acne", "rosacea", "dermatitis", "hyperpigmentation", "normal"],
                    index=0,
                    key=f"cond_{rec['id']}",
                )

            if st.button(f"Save Review ({rec['id']})"):
                if choice == "Unknown":
                    st.warning("Mark as Correct or Incorrect before saving.")
                else:
                    is_correct = choice == "Correct"
                    data_fb = {
                        "inference_id": rec["id"],
                        "is_correct": str(is_correct).lower(),
                        "corrected_condition": corrected_condition or "",
                    }
                    try:
                        fb_resp = requests.post(f"{API_BASE}/feedback", data=data_fb, timeout=30)
                        if fb_resp.status_code == 200:
                            st.success("Review saved.")
                        else:
                            st.error(f"Error {fb_resp.status_code}: {fb_resp.text}")
                    except Exception as e:
                        st.error(f"Failed to send review: {e}")
