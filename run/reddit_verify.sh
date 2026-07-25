#!/usr/bin/env bash
# Post-handback usability probe for a Reddit script-app credential (actuate --verify-cmd).
# Exit 0 = the returned credential authenticates against the Reddit API.
# Expects ACTUATE_RETURN_FILE to hold JSON: {"client_id","secret","username","password"}.
set -uo pipefail
F="${ACTUATE_RETURN_FILE:-}"
[[ -z "$F" || ! -f "$F" ]] && { echo "no return file"; exit 1; }
read -r CID SECRET USER PASS < <(python3 -c "import json,sys;d=json.load(open('$F'));print(d.get('client_id',''),d.get('secret',''),d.get('username',''),d.get('password',''))")
[[ -z "$CID" || -z "$SECRET" || -z "$USER" || -z "$PASS" ]] && { echo "missing field(s)"; exit 1; }
TOK=$(curl -s -X POST -A "moneyagent-usabilitycheck/0.1 by $USER" \
  -d grant_type=password -d "username=$USER" -d "password=$PASS" \
  --user "$CID:$SECRET" https://www.reddit.com/api/v1/access_token \
  | python3 -c "import json,sys;print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)
[[ -z "$TOK" ]] && { echo "no access_token (bad creds / 2FA / app type)"; exit 1; }
ME=$(curl -s -H "Authorization: bearer $TOK" -A "moneyagent-usabilitycheck/0.1 by $USER" \
  https://oauth.reddit.com/api/v1/me | python3 -c "import json,sys;print(json.load(sys.stdin).get('name',''))" 2>/dev/null)
[[ -n "$ME" ]] && { echo "OK: authenticated as u/$ME"; exit 0; }
echo "token obtained but /me failed"; exit 1
