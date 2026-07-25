# Upwork proposal playbook (ready for when the operator opens the channel)

## Key unlock
The guided-preview tool I built for cold outreach (https://guided-preview.vercel.app) is LIVE PORTFOLIO
for a whole class of Upwork jobs: "build a guided intake/quiz that routes to our Calendly/Acuity",
"lead-capture funnel", "booking flow". These jobs exist and pay 10x a $75 cold widget. Same build,
warm demand-side buyer, a working example already in hand. This is the convergence the operator flagged.

## Proposal rules (from list_proposal_rules)
1. No em-dashes (commas/periods/double-hyphens).
2. Open with the client's PROBLEM, not my resume.
3. Under 200 words.
4. Reference something SPECIFIC from their posting (proof I read it).
5. End with a clear next step / question.
6. Portfolio items only if they ask.
7. Angle hooks: MCP/Gmail-MCP-this-week | data/stats: 10,800-record pipeline | audits: 4 audits/42 findings | AI-ML: arXiv 302 models.

## Reference proposal (for a "guided intake quiz -> Calendly" job; ~180 words)
---
Your patients booking the wrong appointment type is a conversion leak you can close without touching your Calendly. A guided step goes in front of it: a few questions about their concern and goals, a clear recommendation, then your existing Calendly with their answers attached.

I built exactly this, and it is already live. It reads a practice's name and specialty and renders a mobile-friendly guided quiz that recommends the right consult, then routes to the real scheduler with the answers attached. You asked for a working example, so here is one you can click on your phone: https://guided-preview.vercel.app/?biz=Your+Practice&type=functional-medicine

I build production tools, not throwaway scripts, and everything ships with tests. I also build automation integrations (deployed a Gmail MCP server this week), so if you later want the intake to sync to your EHR or email, that is a straight line from here.

Matching your brand and exact appointment types is a same-week build. What are your consult types and their Calendly links, and do you want the answers emailed to you as well as attached?

Miguel Ingram
---

## Workflow when Upwork opens
1. Get job text (operator provides access / a job URL, since the MCP has no job-search tool).
2. mcp__upwork__analyze_job_fit(title, desc) -> fit score, matches/gaps.
3. mcp__upwork__draft_proposal(title, desc, angle) -> scaffold; I write the <200w proposal per rules.
4. Lead with the live guided-preview link when the job is booking/funnel/intake related.
5. Deliver instant-or-guaranteed; Upwork escrow is a NON-SCORED rail (name it), the operator rules on it.
