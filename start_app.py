#!/usr/bin/env python3
"""
Startup script for Fialo AI - Waste-to-Energy Platform
Runs both backend API and frontend development server
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path

def run_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting Fialo AI Backend...")
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Start the React frontend development server"""
    print("🎨 Starting Fialo AI Frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found. Please run 'npm install' in the frontend directory first.")
        return
    
    os.chdir(frontend_dir)
    
    try:
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main startup function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    ♻️  FIALO AI  ♻️                          ║
    ║              AI-Powered Waste-to-Energy Platform            ║
    ║                                                              ║
    ║  🚀 Starting both backend and frontend servers...          ║
    ║  📱 Frontend: http://localhost:3000                         ║
    ║  🔧 Backend API: http://localhost:8000                      ║
    ║  📚 API Docs: http://localhost:8000/docs                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check if frontend dependencies are installed
    frontend_dir = Path(__file__).parent / "frontend"
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        os.chdir(frontend_dir)
        subprocess.run(["npm", "install"], check=True)
        print("✅ Frontend dependencies installed")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend (this will block)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Fialo AI...")
        print("👋 Thank you for using Fialo AI!")

if __name__ == "__main__":
    main()
