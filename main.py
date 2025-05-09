from fastapi import FastAPI, Request, HTTPException
import subprocess
import os

app = FastAPI()
secrets_file = 'secrets.json'

def get_secrets() -> dict:
    with open(secrets_file, 'r') as f:
        return f.read()

@app.post("/restart")
async def restart_service(request: Request):
    data = await request.json()
    with open("received.txt", 'a') as f:
        f.write(str(data))
    # if data.get("password") != get_secrets():
    #     raise HTTPException(status_code=403, detail="Forbidden")
    # try:
    #     subprocess.run(["sudo", "systemctl", "restart", "blitz.service"], check=True)
    #     return {"status": "restarted"}
    # except subprocess.CalledProcessError as e:
    #     raise HTTPException(status_code=500, detail=str(e))
