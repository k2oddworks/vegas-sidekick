"""Read-only deployment preflight. Never print credentials or binding values."""
import json
import os
import urllib.request
import urllib.error

token = os.environ.get("CF_TOKEN", "")
account = os.environ.get("CF_ACCOUNT", "")
if not token:
    raise SystemExit("Cloudflare deployment token missing.")
def get(path):
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4" + path,
        headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            body = json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Cloudflare preflight request denied or failed: HTTP {exc.code}") from None
    if not body.get("success"):
        raise SystemExit("Cloudflare preflight request failed.")
    return body["result"]

get("/user/tokens/verify")
if not account:
    accounts = get("/accounts?per_page=50")
    if len(accounts) != 1:
        raise SystemExit("Set CLOUDFLARE_ACCOUNT_ID explicitly to select the account.")
    account = accounts[0]["id"]
settings = get(f"/accounts/{account}/workers/scripts/vegas-sidekick-hub-api/settings")
bindings = settings.get("bindings", [])
by_name = {b.get("name"): b for b in bindings}
expected = "33e165d0-5e71-42c2-85c1-8b424727627f"
db = by_name.get("DB", {})
if db.get("type") != "d1" or (db.get("id") or db.get("database_id")) != expected:
    raise SystemExit("Existing Worker D1 binding does not match the supplied database ID.")
for name in ("ACCESS_AUD", "ACCESS_TEAM_DOMAIN"):
    if by_name.get(name, {}).get("type") not in ("plain_text", "secret_text"):
        raise SystemExit(f"Required Access binding missing: {name}")
print("Existing Hub Worker, expected D1 binding and Access binding names verified.")
print("Read-only preflight passed; write permission and live authentication are not proven.")
