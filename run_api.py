#!/usr/bin/env python3
"""
Launch script for the AI Community Waste-to-Energy Optimizer API.
"""

import sys
import os
import subprocess

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Launch the FastAPI server."""
    try:
        # Check if uvicorn is installed
        import uvicorn
        print("✅ Uvicorn is installed")
    except ImportError:
        print("❌ Uvicorn is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])
        print("✅ Uvicorn installed successfully")
    
    # Launch the API server
    api_path = os.path.join(os.path.dirname(__file__), 'src', 'api', 'main.py')
    
    print("🚀 Launching ♻️ Fialo AI - Personal Waste-to-Energy Optimizer API...")
    print("📊 API will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the API server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 API server stopped. Thank you for using ♻️ Fialo AI!")

if __name__ == "__main__":
    main()
