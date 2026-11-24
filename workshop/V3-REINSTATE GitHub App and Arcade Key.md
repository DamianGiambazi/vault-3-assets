# V3-REINSTATE — The GitHub App and the Arcade key, after a disconnection

**When to use this:** the GitHub App `novel-door-damian` or the Arcade key `novel-door-github` has been uninstalled, revoked, deleted or changed, or you aren't sure which.
**The goal:** the workshop exactly as chunk C shows it. The App installed on `novel-ssot` only, with two permissions. Arcade holding the key. **The door shut** (no sign-in held), so K shows a first sign-in.
**Time:** 10 min if only the installation is missing; 30–40 min if the App has to be recreated. Do it off camera.
**Blur in any recording:** the address bars, your email, the Client ID, the client secret, the Redirect URI, the GitHub password and 2FA screens.

**Two rules that cost an hour in the rehearsal:**
1. **The Arcade key must use your App.** If `novel-door-github` is missing, Arcade silently uses **its own** GitHub app, and GitHub then refuses the write with `403 Forbidden` (S06). So a shut door in the smoke test does **not** prove the key is right; step 5 does.
2. **One change at a time.** After each step, run its check before you go on.

---

## Step 0 · Find out what is actually disconnected (5 min, read-only)

| # | Look at | Healthy | If not → |
|---|---|---|---|
| 0.1 | GitHub → your avatar → **Settings → Developer settings → GitHub Apps** | `novel-door-damian` is listed | missing = the App was **deleted** → Step 1b |
| 0.2 | GitHub → **Settings → Applications → Installed GitHub Apps** | `novel-door-damian` listed; **Configure** shows *Read access to metadata* · *Read and write access to issues* · Only select repositories: **DamianGiambazi/novel-ssot** | missing → Step 1 · wrong permissions → Step 2 · wrong repositories → Step 1, part 3 |
| 0.3 | Arcade dashboard (`arcade dashboard`, or app.arcade.dev) → **Connections → OAuth providers** | a row **GitHub · Project · ID `novel-door-github`**, switch **on** | missing → Step 3 · switch off → turn it on |
| 0.4 | PowerShell: `arcade whoami` and `Test-Path "$HOME\.arcade\credentials.yaml"` | your account · `True` | → Step 4 |

Write down which rows failed. Only do the steps for those, then always Step 5.

---

## Step 1 · Reinstall the App on the one repository (the App still exists)
1. GitHub → Settings → Developer settings → GitHub Apps → **novel-door-damian** → in the left menu, **Install App**.
2. Next to **DamianGiambazi**, click **Install** (or the gear, if it's partly installed).
3. Choose **Only select repositories** → Select repositories → **novel-ssot** only.
4. Check that the permissions listed are exactly *Read access to metadata* and *Read and write access to issues*.
5. Click **Install** (or "Install & Authorize").
6. GitHub may now jump to Arcade's page: *"Authorization error … missing_parameters"*. **That is expected** (W5): no sign-in was waiting. Close the tab.
   - **But that jump may have authorized you.** Step 5.4 revokes it again, so don't skip Step 5.

**Check:** Installed GitHub Apps → novel-door-damian → Configure shows **2 permissions, 1 repository** (as in row 0.2).

## Step 1b · Recreate the App (only if it was deleted: 30–40 min)
A deleted App can't be restored. The new one gets a **new Client ID**, so the Arcade key must be updated as well (Step 3, edit or recreate).
1. **Arcade first:** if the `novel-door-github` row exists, open it and copy its **Redirect URI**. If it doesn't, do Step 3 up to its own "copy the Redirect URI" line, and leave that panel open.
2. GitHub → Settings → Developer settings → GitHub Apps → **New GitHub App**:

| Field | Value |
|---|---|
| GitHub App name | `novel-door-damian` (if GitHub says the name is taken, wait a few minutes and retry, or use `novel-door-damian-2`, then update the C card (cards §4) and the workshop video captions) |
| Homepage URL | `https://github.com/DamianGiambazi/novel-ssot` |
| Callback URL | the Redirect URI from step 1 |
| Expire user authorization tokens | ✅ |
| Request user authorization (OAuth) during installation | ✅ |
| Enable Device Flow | ☐ |
| Setup URL | empty (greyed out) · Redirect on update ☐ |
| **Webhook → Active** | **☐ untick**, or the form demands a Webhook URL (W1) |
| Repository permissions | **Issues: Read and write** · Metadata: Read-only (automatic) · everything else **No access** |
| Account permissions | none |
| Where can this GitHub App be installed? | **Only on this account** |

3. **Create GitHub App.** On the General page, copy the **Client ID** (`Iv23…`).
4. In the left menu, **Credentials** (or the *Client secrets* box) → **Generate a new client secret** → copy it **now**: it's shown only once.
5. Do Step 3 (Arcade) with this Client ID and secret, **then** Step 1 (install on `novel-ssot` only).

## Step 2 · Fix the permissions (the App exists, but they changed)
1. GitHub App → **Permissions & events** → Repository permissions: **Issues: Read and write**, Metadata: Read-only, all else No access. Account permissions: none. → **Save changes**.
2. A permission change must be **accepted** on the installation: Settings → Applications → Installed GitHub Apps → novel-door-damian → if there's a yellow **"review request"** bar → **Accept new permissions**.

**Check:** row 0.2 again.

## Step 3 · Reinstate the Arcade key
**If the row exists but is wrong** (a wrong Client ID, or the App was recreated):
- open it (pencil) → set **Client ID** to the App's `Iv23…` → **Client Secret**: Arcade needs one; generate a new one in the App's Credentials if you don't have it → Save;
- or delete the row and do the "missing" path below.

**If the row is missing:**
1. Arcade → **OAuth providers** → **Add OAuth Provider** → tab **Included Providers** → Provider **GitHub**.
2. **ID:** `novel-door-github`. This must match **exactly**: the Claude Desktop config, `tab-header.ps1` and the server all use it.
3. **Client ID:** the App's `Iv23…` from GitHub App → General. **Not** the provider name (W3: the root of S06).
4. **Client Secret:** generate a new one (GitHub App → Credentials) and paste it.
5. Copy the **Redirect URI** the form shows. Leave the panel open if you're in the middle of Step 1b.
6. **Create.** Then **open the saved row** and compare its Redirect URI with the one you copied. If they differ, use the saved one (W4: a draft's URI can belong to a provider that never existed).
7. GitHub App → General → **Callback URL** → paste the saved provider's Redirect URI → **Save changes** at the bottom of the page.
8. Clear the clipboard: `Set-Clipboard -Value ' '`.

**Check:** row 0.3. The row is GitHub · **Project** · `nov…` · switch on.
**Check:** Arcade → **Connected users** → there must be **no `arcade-github` line**. Revoke any you find.

## Step 4 · The Arcade CLI sign-in (only if row 0.4 failed)
```powershell
arcade login          # browser: sign in to Arcade (blur)
arcade whoami
Test-Path "$HOME\.arcade\credentials.yaml"     # True
```
Never open `credentials.yaml`.

---

## Step 5 · Prove it end to end, then shut the door again (15 min, nothing is posted)

**5.1 · The door answers, and is shut:**
```powershell
. C:\Dev\v3-preflight\tab-header.ps1 -NoTranscript
Get-Process claude, python -ErrorAction SilentlyContinue | Stop-Process -Force   # Claude Desktop must not be running
Set-Location C:\Dev\novel-door
& $DOOR_PY mcp_smoke.py
```
**Expect** `DOOR shut: sign-in required. Arcade issued a sign-in link` · `MCP_SMOKE_OK`.
- `DOOR OPEN`: a sign-in is still held → do 5.4 first, then come back.
- `Missing Arcade API key`: do Step 4.

**5.2 · The key opens your App, not Arcade's.** It reads the repository; it never writes.
```powershell
& $DOOR_PY mcp_smoke.py --door-test
```
It prints `DOOR shut. Open this link…` and a link. Open it:
- **GitHub's page must say "Authorize novel-door-damian".** If it names **Arcade** instead, the key isn't using your App: stop, Step 3.
- Approve → *"Authorization successful."* (it may open in Edge, W8) → close the tab.

**5.3 · Run the door test again:**
```powershell
& $DOOR_PY mcp_smoke.py --door-test
```
**Expect** `DOOR OPEN: signed in. Read DamianGiambazi/novel-ssot: HTTP 200` → **`DOOR_TEST_OK`**. Then Arcade → Connected users should show your line under **novel-door-github**.

| If you see | It means | Do |
|---|---|---|
| `HTTP 404` | the App isn't installed on `novel-ssot` | Step 1, then 5.3 again |
| `HTTP 401` | the sign-in was revoked on GitHub but Arcade still holds it | Arcade → Connected users → Revoke → 5.2 |
| `HTTP 403` | a permission is missing, or not yet accepted | Step 2 (and accept the review request) |
| GitHub: *"The redirect_uri is not associated with this application"* | the App's Callback URL ≠ the saved provider's Redirect URI | Step 3, items 6–7 |
| Arcade error after you approve | Arcade wants something the App doesn't grant, often your email | App → Account permissions → **Email addresses: Read-only** → Save → accept on the installation → 5.2. Record it as a new snag |
| the consent page names Arcade, or Connected users shows `arcade-github` | the provider ID isn't found, so Arcade fell back to its own app | Step 3: check the ID is exactly `novel-door-github` |

**5.4 · Shut the door again** (the take needs a first sign-in in K):
1. GitHub → Settings → Applications → **Authorized GitHub Apps** → novel-door-damian → **Revoke**. (Installed GitHub Apps stays as it is.)
2. Arcade → **Connected users** → your line under novel-door-github → **Revoke** → *"No connected users found"*.

**5.5 · Confirm it's shut:**
```powershell
& $DOOR_PY mcp_smoke.py
```
**Expect** `DOOR shut: sign-in required` · `MCP_SMOKE_OK`.
- If it says `OPEN`, one of the two revokes didn't take: repeat 5.4.
- If it's still `OPEN` after that, wait 60 s and run it again. Revocations can take a moment to reach Arcade.

**5.6 · Back to the take's starting state:**
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
. C:\Dev\v3-preflight\tab-header.ps1        # archives smoke-calls.jsonl; starts the transcript
C:\Dev\v3-preflight\preflight-check.ps1     # PREFLIGHT_OK
```

---

## If it's slow or flaky
- **GitHub asks for your password or 2FA ("sudo mode")** partway through: normal for App settings. Sign in, then repeat the click.
- **A change doesn't show yet:** reload the page once. GitHub and Arcade can lag 30–60 s. Never change a second thing while you wait for the first.
- **The browser tab is signed in to a different GitHub account** (check the avatar): everything above must happen as **DamianGiambazi**.
- **The smoke test is slow (40–120 s):** that's torch loading, not the network. If it hangs past 3 min, check free RAM (≥ 2 GB) and use `Stop-Process`, not Ctrl+C (W7).
- **Record what you changed** in the capture log's snags table (the next ID is V3-S12). If the App's name changed, update the C card (cards §4) and the workshop video captions.
