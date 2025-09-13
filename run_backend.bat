@echo off
echo Starting Fialo AI Backend...
echo.

REM Try different Python commands
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
if %errorlevel% neq 0 (
    echo Trying python3...
    python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
    if %errorlevel% neq 0 (
        echo Trying py...
        py -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
        if %errorlevel% neq 0 (
            echo Python not found. Please install Python and add it to PATH.
            pause
        )
    )
)
