from fastapi import FastAPI, Request, HTTPException
import uvicorn
import json
import subprocess
import os

app = FastAPI()
secrets_file = 'secrets.json'

def get_secrets() -> dict:
    with open(secrets_file, 'r') as f:
        return f.read()

counter = 1

@app.post("/restart")
async def restart_service(request: Request):
    global counter
    data = await request.json()
    with open(f"received{counter}.txt", 'w+') as f:
        json.dump(data, f, indent=4)
        counter += 1
    # if data.get("password") != get_secrets():
    #     raise HTTPException(status_code=403, detail="Forbidden")
    # try:
    #     subprocess.run(["sudo", "systemctl", "restart", "blitz.service"], check=True)
    #     return {"status": "restarted"}
    # except subprocess.CalledProcessError as e:
    #     raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=5656,
        reload=False,
    )
