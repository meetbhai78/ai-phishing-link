import os
import sys
import uvicorn

if __name__ == "__main__":
    # Ensure current directory is in sys.path
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    if curr_dir not in sys.path:
        sys.path.insert(0, curr_dir)
        
    print("\n=======================================================")
    print("🛡️  CYBERSHIELD FASTAPI SERVER (v3.7)")
    print("=======================================================")
    print("👉 Live Dashboard: http://127.0.0.1:8000/dashboard")
    print("👉 Swagger API:    http://127.0.0.1:8000/docs")
    print("👉 Predictions:    http://127.0.0.1:8000/predict")
    print("=======================================================\n")
    
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
