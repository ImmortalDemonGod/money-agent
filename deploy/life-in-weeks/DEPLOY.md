# Deploy note (life-in-weeks landing → Vercel)

Ready-to-deploy crawlable landing page for the compliant Life-in-Weeks offer. Pending the Vercel
token from actuation ACT-001.

On token arrival (bin/actuate.py sync ACT-001):
1. `sed -i '' 's#__DEPLOY_URL__#https://<the-vercel-url>#g' index.html`  (sets canonical + JSON-LD url
   to the live vercel.app URL — do NOT point canonical at surge, which is robots-blocked).
2. `vercel deploy --prod --token <TOKEN>` from this dir.
3. `python3 bin/host_check.py <vercel-url>` must PASS (crawlable) before it counts.
4. Record a P3 publish decision (decision_gate) + register the indexation bet.

Buy link is the compliant capped link (buy.stripe.com/aFa4gB2JRahld6a3Qy7ok0e). Delivery seam stays
on surge unlock.html (already delivery_check PASS). Free tool (liw.js) is canvas-based, self-contained.
