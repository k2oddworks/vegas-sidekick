"""Upload and activate a tested version; never change routes or Access settings."""
import json
import os
import urllib.request
import urllib.error
import uuid
from pathlib import Path

token = os.environ["CF_TOKEN"]
account = os.environ.get("CF_ACCOUNT")
def request(path, data=None, content_type=None):
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request("https://api.cloudflare.com/client/v4" + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            body = json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Cloudflare API request failed: HTTP {exc.code}") from None
    if not body.get("success"):
        raise SystemExit("Cloudflare API request failed.")
    return body["result"]
if not account:
    accounts = request("/accounts?per_page=50")
    if len(accounts) != 1:
        raise SystemExit("Explicit CLOUDFLARE_ACCOUNT_ID required.")
    account = accounts[0]["id"]
base = f"/accounts/{account}/workers/scripts/vegas-sidekick-hub-api"
settings = request(base + "/settings")
bindings = {b["name"]: b for b in settings.get("bindings", [])}
if set(bindings) != {"DB", "ACCESS_AUD", "ACCESS_TEAM_DOMAIN"}:
    raise SystemExit("Unexpected binding set; review before uploading.")
if bindings["DB"].get("type") != "d1" or (bindings["DB"].get("id") or bindings["DB"].get("database_id")) != "33e165d0-5e71-42c2-85c1-8b424727627f":
    raise SystemExit("D1 binding mismatch.")
for name in ("ACCESS_AUD", "ACCESS_TEAM_DOMAIN"):
    if bindings[name].get("type") not in ("plain_text", "secret_text"):
        raise SystemExit("Unexpected Access binding type.")
date = settings.get("compatibility_date")
if not date:
    raise SystemExit("Compatibility date unavailable; review settings.")
metadata = {"main_module": "worker.mjs", "compatibility_date": date,
            "compatibility_flags": settings.get("compatibility_flags") or [],
            "bindings": [{"name": name, "type": "inherit"} for name in sorted(bindings)]}
boundary = uuid.uuid4().hex
parts = []
def part(name, mime, value, filename=None):
    disposition = f'form-data; name="{name}"'
    if filename:
        disposition += f'; filename="{filename}"'
    parts.append((f"--{boundary}\r\nContent-Disposition: {disposition}\r\nContent-Type: {mime}\r\n\r\n").encode() + value + b"\r\n")
part("metadata", "application/json", json.dumps(metadata).encode())
part("worker.mjs", "application/javascript+module", Path(__file__).with_name("worker.mjs").read_bytes(), "worker.mjs")
body = b"".join(parts) + f"--{boundary}--\r\n".encode()
result = request(base + "/versions?bindings_inherit=strict", body, f"multipart/form-data; boundary={boundary}")
print("Inactive version uploaded:", result["id"])
version = result["id"]
# Check that anonymous access is denied before and after activation.
from urllib.parse import urlparse
import time
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None
def anonymous_blocked():
    opener = urllib.request.build_opener(NoRedirect())
    req = urllib.request.Request("https://vegassidekick.com/hub/api/test", headers={"Cache-Control":"no-cache"})
    try:
        with opener.open(req, timeout=20):
            return False
    except urllib.error.HTTPError as exc:
        if exc.code in (401,403):
            return True
        location = urlparse(exc.headers.get("Location", ""))
        return (exc.code in (302,303,307,308) and location.scheme == "https"
                and (location.hostname or "").endswith(".cloudflareaccess.com"))
def verify_blocked():
    for _ in range(3):
        if anonymous_blocked():
            return
        time.sleep(3)
    raise RuntimeError("Anonymous access protection not confirmed.")
verify_blocked()
current = request(base + "/deployments")
previous = current.get("deployments", []) if isinstance(current, dict) else current
if not previous or len(previous[0].get("versions", [])) != 1:
    raise SystemExit("Expected a single active version; review deployment manually.")
old = previous[0]["versions"][0]["version_id"]
def activate(v):
    return request(base + "/deployments", json.dumps({"strategy":"percentage","versions":[{"version_id":v,"percentage":100}]}).encode(), "application/json")
activate(version)
try:
    verify_blocked()
except Exception:
    activate(old)
    raise SystemExit("Anonymous access check failed; previous version restored.")
print("Activated version:", version)
print("Anonymous API request blocked; routes unchanged.")
