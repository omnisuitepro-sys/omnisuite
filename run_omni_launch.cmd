@echo off
cd /d C:\OmniSuite
call venv\Scripts\activate
python -m uvicorn backend.main:app --reload
pause