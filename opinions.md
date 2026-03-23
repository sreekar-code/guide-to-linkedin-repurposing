# Spike Opinions

This file grows over time. Each guide processed by the pipeline contributes 2-4 sharp opinions that emerged from its content. During post generation, Claude reads this file and picks the most relevant opinions to inform each post's point of view.

Do not delete entries without a reason. If Spike's thinking on a topic has evolved, update the entry rather than removing it.

## 5 Offbeat on-call rotations that work

- The on-call rotation your team runs today was probably never chosen — it was inherited, and nobody questioned it
- Uniform on-call coverage is a lazy default, not a best practice — incident volume varies by day and your rotation should too
- The right rotation length is discovered by experiencing multiple lengths, not by debating it in a meeting that goes nowhere
- Predictability in on-call scheduling matters more to the engineer carrying the pager than to the manager who designed the schedule

## How to set up Incident Alert Routing rules effectively

- Alert noise is almost never a volume problem — it's a routing problem, and the fix is rules that know which incidents don't need a human
- The same incident at 2 AM and 11 AM should not trigger the same response — urgency is contextual, not inherent to the incident
- A single incident and a burst of the same incident are fundamentally different signals, and routing rules that treat them the same will over-page your team
- Vague incident titles are the silent killer of routing setups — you can't route what you can't identify

## A compass for setting up your escalation policy

- Escalation policies break in the definitions, not the configuration — if the team can't agree on what's critical, no tool will fix it
- The notification channel is an escalation decision on its own — a phone call at midnight communicates urgency in a way a Slack message never will
- The best first escalation policy is a simple one you refine after seeing real incidents, not a perfect one you spend a month designing
