# ACT: provide a Reddit script-app credential

1. Log in to reddit.com in your own browser (or create an account there — signup solves its own hCaptcha in your human session).
2. Go to https://www.reddit.com/prefs/apps → "create another app…" → select type **script**. Name it anything (e.g. "moneyagent"); redirect URI can be http://localhost:8080.
3. After creating it, note the **client_id** (the string shown under the app name, top-left of the app box) and the **secret**.
4. Return a JSON object as the SECRET handback with exactly these fields:
   `{"client_id": "...", "secret": "...", "username": "<the reddit account username>", "password": "<that account's password>"}`
5. If the account has 2FA enabled: either turn it off for script access, or append the current TOTP to the password as `password:TOTP` per Reddit's script-auth convention (note it expires, so prefer disabling 2FA for a persistent script credential).

The sandbox will verify the credential with `run/reddit_verify.sh` (OAuth password-grant → /api/v1/me). Only the API credential is requested here.
