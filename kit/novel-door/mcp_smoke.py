"""mcp_smoke.py — Gate 3: talk to the server exactly as an MCP client would, before any client exists.

Run:  .venv\\Scripts\\python.exe mcp_smoke.py
Starts server.py over stdio, sends JSON-RPC (initialize, tools/list, four tools/call), prints what comes
back, and checks that no reply contains a vector and that the door is SHUT. Ends with MCP_SMOKE_OK or
MCP_SMOKE_FAIL. The smoke test writes its own log (smoke-calls.jsonl), so calls.jsonl holds only the
client's calls, and it runs the server in smoke mode, so the door can never post an issue.

    mcp_smoke.py --door-test   (off camera, R0) the sign-in path without any client: prints Arcade's sign-in
                               link; after you approve it, run again: the door opens, the server reads the
                               repository (never writes) and DOOR_TEST_OK confirms the GitHub App can reach it.
"""
import json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(errors="replace")
here = Path(__file__).resolve().parent
env = dict(os.environ, NOVEL_DOOR_SMOKE="1", NOVEL_DOOR_LOG=str(here / "smoke-calls.jsonl"))
DOOR_TEST = "--door-test" in sys.argv
proc = subprocess.Popen([sys.executable, str(here / "server.py")], cwd=here, env=env, text=True,
                        encoding="utf-8", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL)
V2_Q1 = [1, 7, 24, 19]          # Vault 2 take, run 20261101_171405: 0.5717 · 0.5758 · 0.5851 · 0.5940

_id = 0
def rpc(method, params=None, notify=False):
    global _id
    msg = {"jsonrpc": "2.0", "method": method, "params": params or {}}
    if not notify:
        _id += 1; msg["id"] = _id
    proc.stdin.write(json.dumps(msg) + "\n"); proc.stdin.flush()
    if notify:
        return None
    while True:
        line = proc.stdout.readline()
        if not line:
            raise SystemExit("MCP_SMOKE_FAIL  the server closed the connection (run: .venv\\Scripts\\python.exe server.py)")
        reply = json.loads(line)
        if reply.get("id") == _id:
            return reply

def call(name, args):
    t = time.perf_counter()
    r = rpc("tools/call", {"name": name, "arguments": args})["result"]
    text = "".join(c.get("text", "") for c in r["content"])
    return r.get("isError", False), text, time.perf_counter() - t

ok, t0 = True, time.perf_counter()
init = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                          "clientInfo": {"name": "mcp_smoke", "version": "1"}})["result"]
rpc("notifications/initialized", notify=True)
print(f"SERVER     {init['serverInfo']['name']} {init['serverInfo']['version']}  "
      f"protocol {init['protocolVersion']}  ({time.perf_counter() - t0:.1f} s to start, includes the model load)")
tools = rpc("tools/list")["result"]["tools"]
for t in sorted(tools, key=lambda t: t["name"]):
    print(f"TOOL       {t['name']:<34} needs sign-in: {'yes' if 'Propose' in t['name'] else 'no'}")
names = {t["name"].split("_", 1)[-1]: t["name"] for t in tools}
ok &= len(tools) == 4

err, text, s = call(names["SearchByMeaning"],
                    {"question": "Someone stands motionless behind glass, observed from a building opposite, and never moves."})
res = json.loads(text)["results"]
got = [r["chapter"] for r in res]
print(f"MEANING    {got}  {' · '.join('%.4f' % r['distance'] for r in res)}  ({s:.1f} s)")
print(f"           Vault 2's order for Q1 was {V2_Q1}: {'same' if got == V2_Q1 else 'DIFFERENT (check the translator gate)'}")
ok &= not err and '"vector"' not in text

err, text, s = call(names["KeywordSearch"], {"word": "window"})
print(f"KEYWORD    'window' -> {[r['chapter'] for r in json.loads(text)['results']]}")
ok &= not err and '"vector"' not in text

err, text, s = call(names["ReadChapter"], {"chapter": 7})
print(f"READ       ch-07: {len(json.loads(text)['text'])} characters")
ok &= not err and '"vector"' not in text

err, text, s = call(names["ProposeSsotAmendment"],
                    {"title": "smoke", "proposal": "smoke", "evidence_chapters": [1]})
if DOOR_TEST:                                    # R0, off camera: does the sign-in path work end to end?
    if not err:
        info = json.loads(text)
        code = info.get("repo_status")
        print(f"DOOR       OPEN: signed in. Read {info.get('repo')}: HTTP {code}")
        if code == 200:
            print("DOOR_TEST_OK  sign-in works and the GitHub App reaches the repository (nothing was written)")
        else:
            print("DOOR_TEST_FAIL  404 = the GitHub App is not installed on this repository · 401 = sign-in revoked · 403 = a permission is missing")
            ok = False
    else:
        link = next((ln.split("Click this link:", 1)[1].strip() for ln in text.splitlines() if "Click this link:" in ln), "")
        print("DOOR       shut. " + ("Open this link, approve, then run --door-test again:\n           " + link
                                    if link else text.strip().splitlines()[0][:90]))
        print("DOOR_TEST_PENDING  not signed in yet")
        ok = False
elif not err:
    print("DOOR       OPEN: a GitHub sign-in already exists (smoke mode: no issue created)")
    print("           -> run the door reset in the runbook (R-3), then this test again")
    ok = False
elif "Authorization required" in text:
    print("DOOR       shut: sign-in required. Arcade issued a sign-in link")
elif "Missing Arcade API key" in text:
    print("DOOR       shut: no Arcade key. On SPOOKY this means 'arcade login' has not been run (P5)")
else:
    print(f"DOOR       shut: {text.strip().splitlines()[0][:70] if text.strip() else 'error'}")

proc.stdin.close(); proc.wait(timeout=10)
if ok and not DOOR_TEST:
    print("DATA_FIREWALL  no vector in any reply")
    print("MCP_SMOKE_OK")
elif not DOOR_TEST:
    print("MCP_SMOKE_FAIL")
sys.exit(0 if ok else 1)
