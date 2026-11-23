import json
import os
import sys
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv()
API = "https://openrouter.ai/api/v1"
NAME = "acmebot-lab"
KEY_NAME = os.getenv("KEY_NAME", "coba")   # existing API key that gets the guardrail


def call(method, path, body=None):
    req = urllib.request.Request(
        API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_MANAGEMENT_KEY']}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read().decode()}")


GUARDRAIL = {
    "name": NAME,
    "description": "AcmeBot lab: budget, model allowlist, content filters",
    "limit_usd": 2,
    "reset_interval": "monthly",
    "allowed_models": [os.getenv("MODEL", "deepseek/deepseek-v3.2")],
    "content_filter_builtins": [
        {"slug": "regex-prompt-injection", "action": "block"},
        {"slug": "email", "action": "redact"},
        {"slug": "phone", "action": "redact"},
    ],
}

existing = [g for g in call("GET", "/guardrails?limit=100")["data"] if g["name"] == NAME]
guardrail = existing[0] if existing else call("POST", "/guardrails", GUARDRAIL)["data"]
print("guardrail:", guardrail["id"], "(existing)" if existing else "(created)")

key = next((k for k in call("GET", "/keys")["data"] if k["name"] == KEY_NAME), None) or sys.exit(f"key '{KEY_NAME}' not found")
action = "assignments/keys/remove" if "--off" in sys.argv else "assignments/keys"
print(action, call("POST", f"/guardrails/{guardrail['id']}/{action}", {"key_hashes": [key["hash"]]}))
