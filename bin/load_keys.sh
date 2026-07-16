#!/usr/bin/env bash
# Verifier credential loader. Two sources, Keychain preferred.
#
# Keychain is the convention the rest of the ecosystem already follows (garmin/edready/zybooks).
# The running-brief D1 defect is the argument: it read a .env off a removable volume, the
# LaunchAgent could not see it, and the brief emitted 85-byte stubs for 4 days while its error
# message blamed Strava credentials. Keychain does not unmount.
#
#   source bin/load_keys.sh
#
# Seed the Keychain once (per key):
#   security add-generic-password -a "$USER" -s money-agent-stripe-read -w 'rk_live_...'
#   security add-generic-password -a "$USER" -s money-agent-privacy-read -w '...'
set -uo pipefail
kc() { security find-generic-password -a "$USER" -s "$1" -w 2>/dev/null; }

if v=$(kc money-agent-stripe-read) && [[ -n "$v" ]]; then
  export STRIPE_READ_KEY="$v"
  [[ -n "${QUIET:-}" ]] || echo "keys: STRIPE_READ_KEY <- Keychain" >&2
elif [[ -f "$(dirname "${BASH_SOURCE[0]}")/../.env" ]]; then
  set -a; . "$(dirname "${BASH_SOURCE[0]}")/../.env"; set +a
  [[ -n "${QUIET:-}" ]] || echo "keys: loaded from .env (Keychain preferred for launchd -- see header)" >&2
fi
if v=$(kc money-agent-privacy-read) && [[ -n "$v" ]]; then export PRIVACY_READ_KEY="$v"; fi

for k in STRIPE_READ_KEY CARD_CAP_USD; do
  [[ "${!k:-}" == *REPLACE_ME* || -z "${!k:-}" ]] && echo "  ⚠ $k is unset or still REPLACE_ME" >&2
done
