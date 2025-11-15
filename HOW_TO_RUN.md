# How to Run Skin AI Assistant

## From Project Root (Recommended)

### Option 1: Python Launcher
```bash
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant
python run_all.py
```

### Option 2: PowerShell Script
```powershell
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant
.\start_skin_ai.ps1
```

---

## From Nested Directory

```bash
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant\skin_ai_assistant
python run_all.py
```

---

## What You'll See

```
======================================================================
>> Skin AI Assistant - Starting All Services
======================================================================
Backend API:       http://127.0.0.1:8001
User UI:           http://localhost:8502
Admin Dashboard:   http://localhost:8601
======================================================================

[1/3] Starting Backend API on port 8001...
[2/3] Starting User UI on port 8502...
[3/3] Starting Admin Dashboard on port 8601...

[OK] All services started successfully!
======================================================================

Access URLs:
   - API Documentation: http://127.0.0.1:8001/docs
   - User Interface:    http://localhost:8502
   - Admin Dashboard:   http://localhost:8601

Press Ctrl+C to stop all services
======================================================================
```

---

## Run Tests

### From Project Root
```bash
python run_tests.py
```

### From Nested Directory
```bash
cd skin_ai_assistant
python run_tests.py
```

**Expected Result:**
```
13 passed in 0.35s
[PASS] All tests passed!
```

---

## Run Individual Services

### Backend Only
```bash
cd skin_ai_assistant
python run_backend.py
```

### User UI Only
```bash
cd skin_ai_assistant
python run_ui.py
```

### Admin Dashboard Only
```bash
cd skin_ai_assistant
python run_admin.py
```

---

## Stop All Services

Press `Ctrl+C` in the terminal where services are running.

You'll see:
```
[STOP] Shutting down all services...
   Stopping Backend...
   Stopping UI...
   Stopping Admin...
[OK] All services stopped.
```

---

## Access the Application

Once running, visit these URLs:

| Service | URL |
|---------|-----|
| **User Interface** | http://localhost:8502 (or displayed port) |
| **Admin Dashboard** | http://localhost:8601 (or displayed port) |
| **API Docs** | http://127.0.0.1:8001/docs (or displayed port) |
| **Health Check** | http://127.0.0.1:8001/health |

---

## Troubleshooting

### "Port already in use"
The app automatically finds free ports. If you see this message, it will choose the next available port.

### "Module not found"
Install dependencies:
```bash
cd skin_ai_assistant
pip install -r requirements.txt
```

### "Can't find run_all.py"
Make sure you're in the correct directory:
```bash
# Check current directory
pwd  # Linux/Mac
cd   # Windows

# Navigate to project root
cd C:\Users\ROLAND\source\pythonrepo\skin_ai_assistant
```

### Services won't start
1. Check if virtual environment is activated (if using one)
2. Verify Python 3.12 is installed
3. Ensure all dependencies are installed
4. Check that ports in range 8000-8700 are not all blocked

---

## Quick Reference

| Task | Command |
|------|---------|
| **Start everything** | `python run_all.py` |
| **Run tests** | `python run_tests.py` |
| **Stop services** | Press `Ctrl+C` |
| **Check health** | Visit http://127.0.0.1:8001/health |

---

## Environment Variables (Optional)

Set custom ports:

**Windows:**
```cmd
set BACKEND_PORT=9000
set UI_PORT=9501
set ADMIN_PORT=9601
python run_all.py
```

**Linux/Mac:**
```bash
export BACKEND_PORT=9000
export UI_PORT=9501
export ADMIN_PORT=9601
python run_all.py
```

---

**That's it!** The app handles everything else automatically with dynamic port mapping.
