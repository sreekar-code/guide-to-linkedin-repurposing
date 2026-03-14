# Spike Opinions

This file grows over time. Each guide processed by the pipeline contributes 2-4 sharp opinions that emerged from its content. During post generation, Claude reads this file and picks the most relevant opinions to inform each post's point of view.

Do not delete entries without a reason. If Spike's thinking on a topic has evolved, update the entry rather than removing it.

---

## Follow-the-sun and other on-call models

- On-call systems that interrupt sleep are a design choice, not an inevitability — the follow-the-sun model proves coverage doesn't require 3am pages.
- New engineers learn incident response faster from live incidents with backup available than from observation or documentation alone.
- Calendar fairness in on-call scheduling often trades response speed for schedule equality — the person closest to the code resolves incidents faster than whoever happens to be on shift.
- The hidden cost of overnight on-call isn't just the interrupted nights — it's the background anxiety that runs through every day that might precede one.

---

## Getting started with on-call

- The prerequisites for starting on-call are simpler than most teams assume — two willing people and a system that sends alerts is enough to begin.
- Most teams default to 24/7 on-call coverage without asking whether their alert volume actually requires it.
- Handoff timing is a scheduling detail that shapes how every shift starts and ends — a midnight handoff is a design choice with real consequences.

---

## 5 things to do before you go on-call for the first time

- A backup responder on your first on-call shift isn't a sign of uncertainty; it's the removal of a single point of failure.
- When your on-call schedule doesn't live in your personal calendar, it creates a small but persistent cognitive overhead that accumulates across every rotation.
- Bank holidays are the most avoidable coverage gap in any on-call schedule — they're known in advance, and a short setup step is all that's needed to prevent them from becoming a problem.

---

## A compass for setting up your escalation policy

- The hardest part of severity-based escalation isn't the tool configuration — it's getting the team to agree on what SEV-1 actually means. The 3am question is often the fastest path to that answer.
- Channel selection is itself an escalation decision — a phone call communicates urgency in a way a Slack message can't, regardless of how the severity is labeled.
- Time-based escalation isn't a separate policy type — it's a precision layer that makes every other policy more context-aware.
