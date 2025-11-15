# Skin AI Assistant - Quick Start Guide

## 30-Second Setup

### 1. Install Dependencies
```bash
cd skin_ai_assistant/skin_ai_assistant
pip install -r requirements.txt
```

### 2. Run Everything

**Option A: From project root (recommended)**
```bash
cd skin_ai_assistant
python run_all.py
# or PowerShell:
.\start_skin_ai.ps1
```

**Option B: From nested directory**
```bash
cd skin_ai_assistant/skin_ai_assistant
python run_all.py
```

That's it! The application will:
- Automatically find available ports
- Start the backend API
- Launch the user interface
- Start the admin dashboard
- Display all URLs

---

## What You Get

After running `python run_all.py`, you'll see:

```
======================================================================
🚀 Skin AI Assistant - Starting All Services
======================================================================
Backend API:       http://127.0.0.1:8000
User UI:           http://localhost:8501
Admin Dashboard:   http://localhost:8601
======================================================================

✅ All services started successfully!

📝 Access URLs:
   • API Documentation: http://127.0.0.1:8000/docs
   • User Interface:    http://localhost:8501
   • Admin Dashboard:   http://localhost:8601

Press Ctrl+C to stop all services
```

---

## Using the Application

### User Interface (http://localhost:8501)
1. Select your skin type, Fitzpatrick type, and ethnicity
2. Upload a face image (JPG or PNG)
3. Click "Analyze Skin"
4. View prediction results
5. Optionally provide feedback on accuracy

### Admin Dashboard (http://localhost:8601)
1. View all inference records
2. Filter by review status
3. See uploaded images
4. Review and correct predictions
5. Mark records as reviewed

### API Documentation (http://127.0.0.1:8000/docs)
- Interactive Swagger UI
- Try out endpoints
- See request/response schemas

---

## Run Tests

Verify everything works:

**From project root:**
```bash
python run_tests.py
```

**From nested directory:**
```bash
cd skin_ai_assistant
python run_tests.py
# or PowerShell:
.\run_tests.ps1
```

Expected output:
```
13 passed in 0.35s
[PASS] All tests passed!
```

---

## Run Individual Services

If you prefer to run services separately:

**Backend only:**
```bash
python run_backend.py
```

**User UI only:**
```bash
python run_ui.py
```

**Admin dashboard only:**
```bash
python run_admin.py
```

---

## Port Configuration

### Automatic (Recommended)
Ports are automatically detected. No configuration needed!

### Manual (Optional)
Set specific ports:

**Windows:**
```cmd
set BACKEND_PORT=8000
set UI_PORT=8501
set ADMIN_PORT=8601
python run_all.py
```

**Linux/Mac:**
```bash
export BACKEND_PORT=8000
export UI_PORT=8501
export ADMIN_PORT=8601
python run_all.py
```

---

## Features at a Glance

✅ **Automatic port detection** - No conflicts, just works
✅ **AI-powered analysis** - ONNX model for fast inference
✅ **User profiles** - Track skin type, Fitzpatrick scale, ethnicity
✅ **Feedback loop** - Improve the model with user corrections
✅ **Admin dashboard** - Review and validate predictions
✅ **Health monitoring** - `/health` endpoint for status checks
✅ **Comprehensive tests** - 13 test cases, 100% passing
✅ **REST API** - Full FastAPI backend with Swagger docs
✅ **Cross-platform** - Windows, Linux, Mac

---

## File Structure

```
skin_ai_assistant/
├── run_all.py          ← Start here!
├── run_tests.py        ← Test everything
├── backend/            ← FastAPI application
├── ui/                 ← Streamlit interfaces
├── tests/              ← Test suite
└── utils/              ← Port utilities
```

---

## What's Next?

1. **Try the demo**: Upload an image and see the results
2. **Check the API**: Visit http://127.0.0.1:8000/docs
3. **Run tests**: Verify with `python run_tests.py`
4. **Read the full docs**: See `FEATURES_AND_USAGE.md`

---

## Troubleshooting

**Problem:** "Port already in use"
**Solution:** The app finds free ports automatically. If you set manual ports, choose different ones.

**Problem:** Tests failing
**Solution:** Ensure dependencies are installed: `pip install -r requirements.txt`

**Problem:** Model not found
**Solution:** The app runs in fallback mode without a trained model. See `ml/train.py` to train one.

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Run everything | `python run_all.py` |
| Run tests | `python run_tests.py` |
| Backend only | `python run_backend.py` |
| User UI only | `python run_ui.py` |
| Admin only | `python run_admin.py` |

---

**Ready to go!** Run `python run_all.py` and start analyzing skin conditions.

For detailed documentation, see [FEATURES_AND_USAGE.md](FEATURES_AND_USAGE.md)
