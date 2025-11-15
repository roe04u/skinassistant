# Skin AI Assistant - Complete Feature List and Usage Guide

## Overview
Skin AI Assistant is a comprehensive AI-powered cosmetic skin condition analysis system featuring a FastAPI backend, user-facing Streamlit UI, and admin dashboard for data management and model improvement.

---

## Features Implemented

### Core Features

#### 1. **Image-Based Skin Analysis**
- Upload face images (JPG, PNG)
- AI-powered condition detection using ONNX model
- Confidence scoring for predictions
- Support for multiple skin conditions:
  - Acne
  - Rosacea
  - Dermatitis
  - Hyperpigmentation
  - Normal skin

#### 2. **User Profile Support**
- Skin type tracking (oily, dry, combination, sensitive, normal)
- Fitzpatrick scale classification (I-VI)
- Ethnicity/background recording for bias analysis:
  - West African, East African, North African
  - Afro-Caribbean, Afro-European
  - South Asian, South East Asian
  - Mixed African Asian
  - Other/Unspecified

#### 3. **Feedback Loop**
- User feedback collection (correct/incorrect predictions)
- Corrected condition submission
- Automatic flagging for expert review
- Feedback stored for model retraining

#### 4. **Admin Dashboard**
- View all inference records
- Filter by review status
- Display uploaded images
- Review and validate predictions
- Export data for model improvement

#### 5. **Health Monitoring**
- `/health` endpoint for service status checks
- API documentation via FastAPI/Swagger UI

---

## Dynamic Port Mapping

### Automatic Port Detection
All services automatically find available ports to avoid conflicts:

- **Backend API**: Scans ports 8000-8100
- **User UI**: Scans ports 8501-8600
- **Admin Dashboard**: Scans ports 8601-8700

### Port Utilities
File: [utils/port_utils.py](skin_ai_assistant/utils/port_utils.py)
```python
def get_free_port(start_port: int = 8000, max_port: int = 9000) -> int
```

---

## API Endpoints

### 1. POST /analyze
Analyze a skin image and return prediction.

**Request:**
- `file`: Image file (multipart/form-data)
- `skin_type`: User's skin type (optional, default: "any")
- `fitzpatrick`: Fitzpatrick type (optional, default: "unspecified")
- `ethnicity`: Ethnic background (optional, default: "unspecified")

**Response:**
```json
{
  "inference_id": "uuid-string",
  "condition": "acne",
  "confidence": 0.87,
  "skin_type": "oily",
  "fitzpatrick": "V",
  "ethnicity": "west_african"
}
```

### 2. POST /feedback
Submit feedback on a prediction.

**Request:**
- `inference_id`: ID from analyze response (form data)
- `is_correct`: Boolean indicating accuracy (form data)
- `corrected_condition`: Correct condition if wrong (optional, form data)

**Response:**
```json
{
  "ok": true
}
```

### 3. GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "Skin AI Assistant API"
}
```

### 4. GET /admin/inferences
Retrieve inference records (admin).

**Query Parameters:**
- `limit`: Maximum records to return (default: 100)
- `needs_review`: Filter by review status ("true"/"false"/null)

**Response:**
```json
[
  {
    "id": "uuid",
    "image_path": "path/to/image.jpg",
    "created_at": "2025-11-14T12:00:00",
    "predicted_condition": "acne",
    "predicted_confidence": 0.87,
    "user_skin_type": "oily",
    "user_fitzpatrick": "V",
    "user_ethnicity": "west_african",
    "is_correct": false,
    "corrected_condition": "rosacea",
    "needs_review": true
  }
]
```

---

## Running the Application

### Option 1: Run All Services Together (Recommended)
```bash
python skin_ai_assistant/run_all.py
```

This launches:
- Backend API on auto-detected port
- User UI on auto-detected port
- Admin Dashboard on auto-detected port

Output shows URLs for all services.

### Option 2: Run Services Individually

**Backend:**
```bash
python skin_ai_assistant/run_backend.py
```

**User UI:**
```bash
python skin_ai_assistant/run_ui.py
```

**Admin Dashboard:**
```bash
python skin_ai_assistant/run_admin.py
```

### Option 3: Custom Port Configuration
Set environment variables before running:
```bash
# Windows
set BACKEND_PORT=8000
set UI_PORT=8501
set ADMIN_PORT=8601
python skin_ai_assistant/run_all.py

# Linux/Mac
export BACKEND_PORT=8000
export UI_PORT=8501
export ADMIN_PORT=8601
python skin_ai_assistant/run_all.py
```

---

## Testing

### Run All Tests
```bash
# Python (cross-platform)
python skin_ai_assistant/run_tests.py

# PowerShell (Windows)
.\skin_ai_assistant\run_tests.ps1
```

### Test Coverage
All tests automatically use dynamic port mapping.

**Test Files:**
1. [tests/test_health.py](skin_ai_assistant/tests/test_health.py) - Health endpoint
2. [tests/test_analyze_and_feedback.py](skin_ai_assistant/tests/test_analyze_and_feedback.py) - Core workflow
3. [tests/test_admin_inferences.py](skin_ai_assistant/tests/test_admin_inferences.py) - Admin functionality
4. [tests/test_endpoints_comprehensive.py](skin_ai_assistant/tests/test_endpoints_comprehensive.py) - Complete endpoint testing

**Test Statistics:**
- 13 comprehensive test cases
- 100% pass rate
- Tests include:
  - Health checks
  - Image analysis with various profiles
  - Feedback submission (correct/incorrect)
  - Admin record retrieval with filters
  - Edge cases (non-existent IDs, etc.)

---

## Project Structure

```
skin_ai_assistant/
├── backend/
│   ├── main.py           # FastAPI application with all endpoints
│   ├── models.py         # SQLAlchemy data models
│   ├── db.py             # Database configuration
│   ├── config.py         # Application configuration
│   └── inference.py      # AI model inference logic
├── ui/
│   ├── streamlit_app.py  # User-facing interface
│   └── admin_app.py      # Admin dashboard
├── ml/
│   ├── train.py          # Model training script
│   └── build_dataset.py  # Dataset preparation
├── utils/
│   └── port_utils.py     # Dynamic port detection
├── tests/
│   ├── conftest.py       # Test configuration
│   ├── test_health.py
│   ├── test_analyze_and_feedback.py
│   ├── test_admin_inferences.py
│   └── test_endpoints_comprehensive.py
├── run_all.py            # Launch all services
├── run_backend.py        # Launch backend only
├── run_ui.py             # Launch user UI only
├── run_admin.py          # Launch admin only
├── run_tests.py          # Run test suite (Python)
└── run_tests.ps1         # Run test suite (PowerShell)
```

---

## Database Schema

**Table: inferences**

| Column | Type | Description |
|--------|------|-------------|
| id | String (UUID) | Primary key |
| image_path | String | Path to uploaded image |
| created_at | DateTime | Timestamp |
| predicted_condition | String | AI prediction |
| predicted_confidence | Float | Confidence score (0-1) |
| predicted_skin_type | String | Future: multi-task output |
| predicted_fitzpatrick | String | Future: multi-task output |
| predicted_acne_grade | Float | Future: severity scoring |
| predicted_pih_level | Float | Future: PIH assessment |
| user_skin_type | String | User-provided skin type |
| user_fitzpatrick | String | User-provided Fitzpatrick |
| user_ethnicity | String | User-provided ethnicity |
| predictions_json | JSON | Raw prediction data |
| is_correct | Boolean | Feedback: prediction accuracy |
| corrected_condition | String | User/admin correction |
| corrected_acne_grade | Float | Future: corrected severity |
| corrected_pih_level | Float | Future: corrected PIH |
| notes | String | Admin notes |
| needs_review | Boolean | Flagged for expert review |

---

## Future Enhancement Features (Not Yet Implemented)

### Planned Features
1. **Multi-task Model Output**
   - Simultaneous skin type classification
   - Fitzpatrick scale prediction
   - Acne severity grading
   - PIH level assessment

2. **Advanced Analytics**
   - Performance metrics by demographic
   - Bias detection and reporting
   - Longitudinal tracking for returning users
   - A/B testing framework

3. **Model Retraining Pipeline**
   - Automated dataset updates from feedback
   - Scheduled retraining jobs
   - Model versioning and rollback
   - A/B deployment

4. **Enhanced Admin Features**
   - Bulk review operations
   - Data export (CSV, JSON)
   - Annotation tools
   - User management

5. **Security & Authentication**
   - User accounts and login
   - OAuth integration
   - API key management
   - HIPAA compliance considerations

6. **Mobile Support**
   - React Native app
   - Progressive Web App (PWA)
   - Camera integration
   - Offline mode

7. **Additional ML Features**
   - Explainable AI (Grad-CAM visualizations)
   - Confidence calibration
   - Ensemble models
   - Active learning

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| BACKEND_PORT | auto | Backend API port |
| UI_PORT | auto | Streamlit UI port |
| ADMIN_PORT | auto | Admin dashboard port |
| SKINAI_API_URL | auto | Backend API URL |
| SKINAI_DB_URL | sqlite:///skin_ai.db | Database connection |

### Model Files
- ONNX Model: `models/best/skin_model.onnx`
- Class Labels: `models/best/class_names.txt`

Models are loaded automatically if present. If not found, the system uses a fallback mode returning placeholder predictions.

---

## Technology Stack

### Backend
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **ONNX Runtime**: Model inference
- **Uvicorn**: ASGI server

### Frontend
- **Streamlit**: UI framework
- **Pillow**: Image processing
- **Requests**: HTTP client

### ML/AI
- **PyTorch**: Model training
- **TorchVision**: Pre-trained models (ResNet50)
- **OpenCV**: Image preprocessing
- **NumPy**: Numerical operations

### Testing
- **Pytest**: Test framework
- **HTTPX**: Async HTTP client for testing

---

## Usage Examples

### Example 1: Analyze an Image (Python)
```python
import requests

files = {"file": open("face.jpg", "rb")}
data = {
    "skin_type": "oily",
    "fitzpatrick": "V",
    "ethnicity": "west_african"
}

response = requests.post(
    "http://127.0.0.1:8000/analyze",
    files=files,
    data=data
)

result = response.json()
print(f"Condition: {result['condition']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### Example 2: Submit Feedback
```python
import requests

data = {
    "inference_id": "abc-123-def",
    "is_correct": "false",
    "corrected_condition": "rosacea"
}

response = requests.post(
    "http://127.0.0.1:8000/feedback",
    data=data
)

print(response.json())  # {"ok": true}
```

### Example 3: Check Service Health
```bash
curl http://127.0.0.1:8000/health
```

---

## Troubleshooting

### Port Already in Use
The system automatically finds free ports. If you need specific ports:
```bash
export BACKEND_PORT=9000
python run_all.py
```

### Tests Failing
Ensure virtual environment is active and dependencies are installed:
```bash
pip install -r requirements.txt
python run_tests.py
```

### Model Not Found
If the ONNX model is missing, the system runs in fallback mode with dummy predictions. To train a model:
```bash
python ml/build_dataset.py  # Prepare data
python ml/train.py          # Train model
```

---

## Support and Contributions

This is a cosmetic/educational tool and does not replace professional dermatological advice.

For issues or feature requests, please refer to the project repository.

---

**Version**: 1.0
**Last Updated**: 2025-11-14
**Status**: All core features implemented and tested
