# Installation Guide - Skin AI Assistant

## Prerequisites

- Python 3.12 or higher
- Windows 10/11, Linux, or macOS
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

---

## Installation Steps

### Quick Start (Recommended - Uses Global Python)

```powershell
# Navigate to project root
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant

# Run the application directly
python run_all.py
```

**Note:** The application uses your global Python installation which already has all required packages installed. This is the fastest and most reliable method.

### Advanced: Using Virtual Environment

If you prefer to use a virtual environment:

```powershell
# Navigate to project
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant\skin_ai_assistant

# Install dependencies in virtual environment
.venv\Scripts\pip install -r requirements.txt

# Verify installation
.venv\Scripts\python -c "import uvicorn, fastapi, streamlit; print('All packages installed!')"

# Navigate back to project root
cd ..

# Run the application
python run_all.py
```

### Automated Setup Script

```powershell
# Navigate to project root
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant

# Run setup script
.\setup.ps1
```

---

## Verification

### Check Installation

```powershell
# Check Python version
python --version
# Should show: Python 3.12.x

# Check if packages are installed
python -c "import fastapi, uvicorn, streamlit, torch; print('All packages installed!')"
```

### Run Tests

```powershell
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant
python run_tests.py
```

Expected output:
```
13 passed in 0.4s
[PASS] All tests passed!
```

---

## Troubleshooting

### Issue: "No module named 'uvicorn'"

**Solution 1:** Install in virtual environment
```powershell
cd skin_ai_assistant
.venv\Scripts\pip install -r requirements.txt
```

**Solution 2:** Use global Python
```powershell
deactivate  # Exit venv
python run_all.py
```

### Issue: "Port already in use"

The app automatically finds free ports. Just run it again.

### Issue: Virtual environment not activating

```powershell
# Allow scripts to run (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\Activate.ps1
```

---

## First Run

After installation, start the application:

```powershell
python run_all.py
```

You'll see:
```
======================================================================
>> Skin AI Assistant - Starting All Services
======================================================================
Backend API:       http://127.0.0.1:8001
User UI:           http://localhost:8502
Admin Dashboard:   http://localhost:8602
======================================================================
```

Access:
- **User Interface:** http://localhost:8502
- **Admin Dashboard:** http://localhost:8602
- **API Docs:** http://127.0.0.1:8001/docs

---

## Next Steps

1. Open User Interface in browser
2. Upload a test image
3. Check the prediction results
4. Provide feedback
5. View results in Admin Dashboard

---

## Uninstallation

```powershell
# Simply delete the project folder
rm -r C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant
```

---

## Support

If you encounter issues:
1. Check this guide
2. Run: `python run_tests.py`
3. Check logs: `tail -f skin_ai_assistant/skin_ai.log`
4. Review: `PRODUCTION_DEPLOYMENT.md`

---

**Installation complete!** You're ready to use Skin AI Assistant.
