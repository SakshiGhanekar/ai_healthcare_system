# AI Healthcare System - Execution Commands

Follow these steps to run the application locally within your virtual environment.

## 1. Environment Setup

Open a terminal in the project root directory (`e:\Projects\AI-Healthcare-System`).

### Activate Virtual Environment

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
.\venv\Scripts\activate.bat
```

### Install Dependencies (First time only)

```powershell
pip install -r backend/requirements.txt
# If you need the full feature set
pip install -r requirements-full.txt
```

---

## 2. Start the Backend (API)

Keep this terminal running. The backend handles AI chat, ML predictions, and PDF generation.

```powershell
# In the project root with venv activated:
uvicorn backend.main:app --reload --port 8000
```

_Port 8000 is the default. If it's busy, use `--port 8001` instead._

---

## 3. Start the Frontend (UI)

Open a **new terminal** and navigate to the project root.

```powershell
# Activate venv again in the new terminal
.\venv\Scripts\Activate.ps1

# Run the Streamlit app
streamlit run frontend/main.py
```

_The UI will automatically open at `http://localhost:8501`_

---

## Troubleshooting

- **Port already in use**: If you see `[Errno 10048]`, it means the backend is already running. You might have left `run_app.bat` active.
- **ModuleNotFoundError**: Ensure your virtual environment is activated (`(venv)` should appear in your terminal prompt).
- **Report unavailable**: Ensure the backend terminal is running and reachable!
