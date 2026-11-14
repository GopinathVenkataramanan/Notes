# Discovery Workshop Readiness Meeting: Facilitator Script

| Field | Value |
|---|---|
| Facilitator | Client Solution Architect |
| Duration | 90 minutes |
| Attendees | Leads of: BA team, Technical BA, Technical team, Test team, Project team |
| Slide deck | `Discovery-Readiness-Meeting.pptx` (slide numbers below match the deck) |
| Basis | Gate 1 of the [SA Review Gates Checklist](../Client%20SA%20Discovery%20Pack/14-SA-Review-Gates-Checklist.md) |

> Dates, names and RAG values are placeholders. Fill them in before the meeting. Lines in *italics* are what to say. Lines marked **Ask** are questions to put to the room.

## 0. Before the meeting (T-3 days to T-0)

- [ ] Send the invite with the agenda and the pre-read (slides 2, 5, 6 and the readiness template).
- [ ] Ask each lead to pre-fill their own slide (7 to 12): status, evidence link, blockers, ETA. Deadline: 24 hours before the meeting.
- [ ] Pull the latest Element Register (13) and check for IDs missing a Technical BA catalogue entry.
- [ ] Prepare the heat map (slide 13) from the pre-filled responses so you can show it live.
- [ ] Book a note-taker. Open an actions log and a decisions log.
- [ ] Confirm the workshop date, attendees and format with the client so the "days to workshop" number is correct.

## 1. Run sheet

| Time | Min | Slide | Topic | Lead |
|---|---|---|---|---|
| 0:00 | 5 | 1 to 4 | Welcome, purpose, agenda, ground rules | Client SA |
| 0:05 | 5 | 5 to 6 | Where we are and how we rate readiness | Client SA |
| 0:10 | 45 | 7 to 12 | Team readiness round (about 7 to 8 min each) | Each lead |
| 0:55 | 10 | 13 to 14 | Heat map and cross-team dependencies | Client SA |
| 1:05 | 8 | 15 | Risks, blockers and asks | All |
| 1:13 | 7 | 16 | Workshop plan: agenda, roles, logistics, rehearsal | Client SA, Project |
| 1:20 | 7 | 17 | Actions, owners and dates | Note-taker |
| 1:27 | 3 | 18 | Go / conditional go / no-go and close | Client SA |

## 2. Script

### Slide 1: Title (1 min)

*Good morning, everyone. Thanks for making time. This is our readiness check before the discovery workshop with the client. By the end we will know what is ready, what is not, who owns the gap and whether we go ahead on the planned date.*

### Slide 2: Purpose and outcomes (2 min)

*We have three outcomes today.*
1. *An honest readiness position for each team.*
2. *Named owners and dates for every gap.*
3. *A go, conditional go or no-go call for the workshop.*

*This is not a status report. I want evidence and blockers, not activity.*

### Slide 3: Agenda (1 min)

*Walk through the run sheet. Point out that the team round is the main block and that each lead has about 7 minutes.*

### Slide 4: Ground rules (1 min)

- *Each lead speaks to their own slide for no more than 7 minutes, then we take questions.*
- *Use red, amber and green against the definitions on slide 6. No "amber-green".*
- *Raise blockers early. Nobody gets blamed for a red here. A hidden red on workshop day costs more.*
- *Detailed fixes go offline. We log the action and move on.*
- *Anything that needs a decision goes on the decision log.*

### Slide 5: Where we are (2 min)

*Each team feeds the consolidated discovery pack. The pack goes to the client for the workshop and later to vendor validation and estimation. The estimate is only as good as what goes in.*

*Show the flow: BA, Technical BA, Client SA, Test, Project, then the consolidated pack.*

*The thing that ties our work together is the shared IDs: SYS, INT, DATA and ENV. If a BA process, a Technical BA interface and an architecture diagram do not use the same ID, the client will spot the gap in the workshop.*

### Slide 6: How we rate readiness (3 min)

*Read the definitions out loud.*
- **Green:** complete, reviewed and the evidence is in the shared pack folder.
- **Amber:** content exists but is incomplete or unreviewed. There is a dated plan to close it before the workshop.
- **Red:** missing, or no credible plan to close before the workshop.

*A deliverable is not green until someone other than the author has reviewed it.*

### Slides 7 to 12: Team readiness round (45 min)

Use the same pattern for every team:

1. *The lead gives a 2-minute headline: overall RAG, the top gap, the top risk.*
2. *Walk the table: deliverable, status, evidence, ETA.*
3. *Facilitator probes with the team's questions (below).*
4. *Log actions. Move on at 7 minutes even if unresolved.*

Suggested order follows how the pack builds: BA first (what the business needs), Technical BA (what exists), Technical team (how it should be built and secured), Test, then Project (constraints and governance). The Client SA slide goes first or last depending on preference. We suggest first, to set an example of how to report.

#### Slide 7: Client SA (architecture pack)

*I will go first so you can see the level of detail I am looking for.*

Cover: diagrams 01 to 08 complete, Element Register coverage, EA standards confirmed, NFR values agreed, shared responsibility reviewed, any *(example)* values still to replace.

**Ask (self):** *What would the client challenge first in my pack?*

#### Slide 8: BA team

Probe:
- **Ask:** *Is the Product Fit-Gap Matrix complete against the in-scope requirements? How many requirements are still unclassified?*
- **Ask:** *Which processes are the business expecting to see demonstrated in the workshop?*
- **Ask:** *Are the requirement IDs and MoSCoW priorities agreed with the business?*
- **Ask:** *Which stakeholders must attend and have they been confirmed?*

#### Slide 9: Technical BA

Probe:
- **Ask:** *Does every current-state interface have an INT-ID and a catalogue entry?*
- **Ask:** *Do we have migration volumes, entities, data quality findings and retention rules?*
- **Ask:** *Where does the catalogue differ from the Element Register? Who resolves it?*
- **Ask:** *Which interface specs are still unverified with the system owners?*

#### Slide 10: Technical team

Probe:
- **Ask:** *Are the enterprise standards confirmed with Enterprise Architecture?*
- **Ask:** *Has Security reviewed the security requirements and confirmed the data classification?*
- **Ask:** *Has the network team reviewed the connectivity needs (allowlisting, private connectivity, DNS)?*
- **Ask:** *Do we have an owner for the identity integration (SSO, MFA, provisioning)?*
- **Ask:** *Are integration and test environments available and mapped to ENV-IDs?*

#### Slide 11: Test team

Probe:
- **Ask:** *Is the test strategy drafted, including migration validation and performance and security testing?*
- **Ask:** *What do you need from the vendor and the client in the workshop to size testing?*
- **Ask:** *Are test environments and test data assumptions stated?*
- **Ask:** *Do the NFR targets have measurable acceptance criteria?*

#### Slide 12: Project team

Probe:
- **Ask:** *Are scope, roadmap, governance and cutover constraints documented?*
- **Ask:** *Is the RAID log current and does it reflect the architecture risks and assumptions?*
- **Ask:** *Are the workshop logistics, invites and pre-reads in place?*
- **Ask:** *Do we have budget and timeline boundaries we can share with the vendor?*

### Slide 13: Readiness heat map (5 min)

*Here is the combined view. Look at the reds first, then the ambers that have no date.*

- Confirm each cell with the owner. Change a RAG only on evidence.
- Count the Must items that are not green. This number feeds the go / no-go call.

### Slide 14: Cross-team dependencies (5 min)

*Most of our risk sits between teams, not inside them.*

Walk each dependency and confirm the giver, receiver and date:
- BA fit-gap needs Technical BA integration and data scope.
- Technical BA catalogue and Element Register must match on IDs.
- Test strategy needs NFR targets from the Technical team and Client SA.
- Project RAID needs risks and assumptions from every team.
- Workshop agenda needs input from all teams.

### Slide 15: Risks, blockers and asks (8 min)

*What could stop us running a useful workshop? Let us go round the room.*

- Capture each risk with an owner and a mitigation.
- Take clear asks: what do you need from another team or from the client?
- Escalate anything that needs a sponsor decision. Name who will escalate and by when.

### Slide 16: Workshop plan (7 min)

*Now let us agree how we will run the workshop.*
- Draft agenda and topics per session.
- Roles: lead, scribe, subject-matter responders, demo owner.
- Logistics: date, venue or call, pre-reads, who attends from the client side.
- Rehearsal: a dry run at T-2 days.
- Pre-read issue date to the client.

**Ask:** *Who needs to be in the room for which session, and who is on call?*

### Slide 17: Actions, owners and dates (7 min)

*The note-taker reads back every action: what, who, when. If any has no owner or date, we fix it now.*

### Slide 18: Go / no-go and close (3 min)

*Based on what we heard, my proposal is: [go / conditional go / no-go].*

| Call | Meaning |
|---|---|
| Go | All Must items green, or amber with a dated plan that lands before the workshop |
| Conditional go | Named reds with an owner and date. Re-check at the checkpoint |
| No-go | Reds with no credible plan. Re-plan the workshop date |

*Ask for any objection. Confirm the next checkpoint date.*

*Thank you. Minutes and the action log go out within 24 hours.*

## 3. Facilitation tips

- Start on time. If a lead is late, take their slide last.
- If a discussion runs over, say: *"Let me park that. Who owns the action?"*
- Do not accept "nearly done." Ask for the percentage, the evidence and the date.
- If two teams disagree on an ID, scope or date, log a decision and assign an owner. Do not settle it live.
- Protect the last 10 minutes. Actions and the go / no-go call matter more than the final detail of any one team.

## 4. After the meeting (within 24 hours)

- [ ] Send minutes, the final heat map, actions and the go / no-go outcome.
- [ ] Update the Gate 1 checklist (14) with status and evidence links.
- [ ] Update the RAID log with new risks.
- [ ] Set the checkpoint meeting (15 minutes) for T-3 days before the workshop.
- [ ] Schedule the dry run.

## 5. Assumptions

- "Technical team" means the architecture, security, network, integration, infrastructure and environments leads. Adjust slide 10 if your team differs.
- The workshop is the discovery workshop where the consolidated pack is presented to the client for validation and estimation.
- The meeting is 90 minutes. If you have 60, run the team round at 5 minutes each and merge slides 13 and 14.
