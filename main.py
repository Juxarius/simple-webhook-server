import hmac
from fastapi import FastAPI, Request, HTTPException, Header
import uvicorn
import subprocess
from pathlib import Path
import json
import hashlib

app = FastAPI()
secrets_file = Path(__file__).parent / 'secrets.json'

def get_secrets() -> dict:
    with open(secrets_file, 'r') as f:
        return json.load(f)

def is_valid_github_request(body: bytes, x_hub_signature_256: str):
    secret = get_secrets()["githubSecret"].encode()
    expected_signature = 'sha256=' + hmac.new(secret, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, x_hub_signature_256)

@app.post("/restart/github")
async def restart_service(request: Request, x_hub_signature_256: str=Header(None)):
    global counter
    body = await request.body()
    if not is_valid_github_request(body, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Forbidden")

    data = await request.json()
    repo_data = get_secrets()["restart"].get(data["repository"]["full_name"], None)
    if repo_data is None:
        raise HTTPException(status_code=404, detail="Repo not found")

    try:
        subprocess.run(["sudo", "su", "-", repo_data["user"],"-c", f"cd {repo_data['appDir']} && git pull"])
        subprocess.run(["sudo", "systemctl", "restart", repo_data["service"]])
        return {"status": "restarted"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=5656,
        reload=False,
    )
