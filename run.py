"""
Convenience entrypoint to run LabManager REST API server from project root.
Usage:
    python run.py
"""

from src.app import create_app

app = create_app()

if __name__ == "__main__":
    print("[*] Starting LabManager REST API Server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
