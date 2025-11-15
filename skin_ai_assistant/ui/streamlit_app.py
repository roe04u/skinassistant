import os
import requests
import streamlit as st
from PIL import Image
from io import BytesIO

API_BASE = os.getenv("SKINAI_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Skin AI Assistant", page_icon="[SKIN AI]", layout="centered")
st.title("[SKIN AI] Skin AI Assistant")
st.write("Upload a clear photo of your face and get a cosmetic skin condition suggestion.")

# Check backend health
@st.cache_data(ttl=30)
def check_backend():
    """Check if backend is reachable (cached for 30 seconds)."""
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False

# Show backend status
if not check_backend():
    st.warning(f"⚠️ Backend not reachable at {API_BASE}. Some features may not work.")
    st.info("Please ensure the backend is running: `python run_backend.py`")

# --- Profile inputs ---
col1, col2 = st.columns(2)
with col1:
    skin_type = st.selectbox(
        "Your skin type",
        ["any", "oily", "dry", "combination", "sensitive", "normal"],
        index=0,
    )
with col2:
    fitzpatrick = st.selectbox(
        "Fitzpatrick type",
        ["unspecified", "I", "II", "III", "IV", "V", "VI"],
        index=3,
    )

ethnicity = st.selectbox(
    "Ethnic background (rough)",
    [
        "unspecified",
        "west_african",
        "east_african",
        "north_african",
        "afro_caribbean",
        "afro_european",
        "south_asian",
        "south_east_asian",
        "mixed_african_asian",
        "other",
    ],
)

st.markdown("---")

uploaded = st.file_uploader("Upload a face image (jpg/png)", type=["jpg", "jpeg", "png"])

if uploaded:
    # Preview
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded image", use_column_width=True)

    if st.button("Analyze Skin"):
        with st.spinner("Contacting Skin AI backend..."):
            try:
                uploaded.seek(0)
                files = {"file": (uploaded.name, uploaded, uploaded.type)}
                data = {
                    "skin_type": skin_type,
                    "fitzpatrick": fitzpatrick,
                    "ethnicity": ethnicity,
                }
                resp = requests.post(f"{API_BASE}/analyze", files=files, data=data, timeout=60)
                if resp.status_code != 200:
                    st.error(f"API error {resp.status_code}: {resp.text}")
                else:
                    out = resp.json()
                    st.success("Analysis complete ✅")

                    st.subheader("Prediction")
                    st.write(f"**Condition:** `{out['condition']}`")
                    st.write(f"**Confidence:** `{out['confidence']*100:.1f}%`")

                    st.subheader("Profile used")
                    st.write(f"- Skin type: `{out['skin_type']}`")
                    st.write(f"- Fitzpatrick: `{out['fitzpatrick']}`")
                    st.write(f"- Ethnicity: `{out['ethnicity']}`")

                    inference_id = out["inference_id"]

                    st.markdown("---")
                    st.subheader("Help improve the AI")

                    colf1, colf2 = st.columns(2)
                    with colf1:
                        correct_choice = st.radio(
                            "Was this prediction accurate?",
                            ["Yes", "No"],
                            horizontal=True,
                        )
                    with colf2:
                        corrected_condition = st.selectbox(
                            "If **No**, what condition fits better?",
                            ["", "acne", "rosacea", "dermatitis", "hyperpigmentation", "normal"],
                        )

                    if st.button("Submit Feedback"):
                        is_correct = correct_choice == "Yes"
                        data_fb = {
                            "inference_id": inference_id,
                            "is_correct": str(is_correct).lower(),
                            "corrected_condition": corrected_condition or "",
                        }
                        fb_resp = requests.post(f"{API_BASE}/feedback", data=data_fb, timeout=30)
                        if fb_resp.status_code == 200:
                            st.success("Feedback submitted. Thank you! 🙏")
                        else:
                            st.error(f"Feedback error {fb_resp.status_code}: {fb_resp.text}")

                    st.info(
                        "This tool is for **cosmetic & educational purposes only** and "
                        "does **not** replace a dermatologist."
                    )
            except Exception as e:
                st.error(f"Request failed: {e}")
else:
    st.info("Upload a face image to begin.")
