# First-Run Experience

This specification defines how a new user should first experience PEGO.

The first run should make PEGO legible without asking the user to design the system, estimate timelines, or solve strategy. PEGO needs enough facts to begin governing toward outcomes; it should not turn onboarding into self-reflection homework.

## UX Goals

- Explain PEGO as executive governance, not a personal assistant.
- Establish the privacy boundary before requesting sensitive facts.
- Gather the smallest useful operating state.
- Avoid asking the user to decide the path, timeline, or strategy PEGO is supposed to model.
- Produce one useful next artifact: a constitution draft, current-state draft, operating register item, or first directive candidate.
- Keep the user in control of authority grants and stop rules.
- Hide adapter mechanics, setup work, diffs, file paths, and internal planning
  from the operating surface.

## First-Run Sequence

### 1. Boundary

PEGO explains:

- What the framework layer is.
- What the protected private instance is.
- What PEGO may store.
- What PEGO will not disclose.
- Which authority level applies during onboarding.

Default authority: Level 1, Recommend.

### 2. Mode

PEGO identifies the collaboration mode:

- Engineering mode for building PEGO.
- UX mode for designing PEGO.
- USER mode for operating a private instance.

First-run onboarding for a real person is USER mode.

### 3. Aim

PEGO asks for desired states, not predicted timelines.

Good questions:

- What future state would make life clearly better?
- What should PEGO help you stop tolerating?
- What should PEGO preserve even while pushing hard?

Avoid:

- What is your 10-year goal?
- How long will this take?
- What exact strategy will you follow?

### 4. Current Operating State

PEGO gathers facts about the current environment and resources:

- Home and location context.
- Work and income context.
- Health baseline.
- Relationship and household constraints.
- Voice, taste, and communication context.
- Skills, assets, network, and obligations.
- Available time and protected time.

The question form should be concrete: "What is true now?" rather than "What do you want your best life to be?"

### 5. Operating Register

PEGO gathers known upcoming friction:

- Upcoming events.
- Recurring annoyances.
- Supply gaps.
- Wardrobe or presentation prep.
- Home and environment watchlist items.
- Strategic dependencies.
- Fears and concerns.

This is how PEGO begins anticipating weeds, missing food defaults, event clothing, appointments, and blocked strategy before they become urgent.

### 6. Authority And Stop Rules

PEGO asks only enough to operate safely:

- What may PEGO never direct?
- What requires explicit approval?
- What protected time is off limits?
- What words or signals pause PEGO?
- What domains require professional review?

### 7. First Operating Artifact

The first run should produce one of:

- Constitution draft.
- Current-state draft.
- Operating register draft.
- First directive queue.
- First targeted question.

Do not end first run with a broad list of homework.

## Intake Phases

PEGO should gather onboarding state in phases:

| Phase | Purpose | Output |
| --- | --- | --- |
| Boundary | Establish privacy, authority, and mode | Safe operating basis |
| Aim | Capture desired states and protected values | Constitution draft inputs |
| Current state | Capture resources and constraints | Current-state draft |
| Environment | Capture home, household, events, annoyances, supplies | Operating register |
| Strategy | Capture income, career, venture, skill, finance constraints | Goal-strategy inputs |
| Finance baseline | Capture income, burn, assets, debt, runway, major costs, and forbidden actions | Finance baseline and unknowns map |
| Career baseline | Capture role, income dependency, leverage, dissatisfaction, and career-risk boundaries | Career baseline and optionality map |
| Health | Capture food, movement, sleep, medical boundaries | Health baseline |
| Home baseline | Capture environment conditions, maintenance risks, disturbance limits, and major project boundaries | Home baseline and operating-register update |
| Relationships baseline | Capture protected people, obligations, disturbance limits, and approval boundaries | Relationship constraints and protected-stakeholder map |
| Exploration baseline | Capture curiosity, renewal, travel, leisure, learning, and constraints | Exploration baseline and renewal candidates |
| Voice | Capture communication style, taste signals, influences, and public positioning constraints | Voice and taste model |
| Happiness baseline | Capture positive/negative life signals and proxy-goal traps | Happiness model baseline |
| Goal reconciliation | Reconcile domain goals into council priority rules | Council priority model |
| Authority | Capture grants, approvals, stop rules | Constitution authority section |

Each phase should fit in one short session.

Use `pego/operations/domain-baseline-bootstrap.md` when a domain lacks enough
state for a specialized agent to produce a useful recommendation, dissent, or
decision-grade question.

Use `pego/operations/goal-reconciliation.md` before Council claims to select
the best directive across domains. Council should attempt to build the model
from protected private state first. If that leaves a decision-changing gap, it
should ask a targeted priority question, use a conservative temporary
assumption, or choose only low-risk information gathering.

The voice phase should avoid asking the user to describe their entire personality. Prefer targeted prompts that collect evidence:

- Link or paste one private writing sample that feels like you.
- Name one piece of writing, film, talk, software, object, or place that captures your taste.
- What would make a public essay about PEGO sound embarrassing or wrong?
- What kind of opportunity should public writing attract?
- What should never be used publicly without review?

## Interaction Cadence

Initial onboarding should work through conversation first. Text and CLI are
acceptable early adapter surfaces because they are easy to audit and version
locally, but the user should be able to start by saying `Start PEGO` or `What
should I do next?`

Future product surfaces may include:

- Web app for constitution, goals, and review.
- Mobile app for next directive and outcome capture.
- Watch for brief directive prompts, timers, and completion.
- Calendar integration for anticipation.
- Slack or SMS for command-response interaction.
- Email for weekly review packets.

The primary UX should be PEGO-initiated directive delivery, not a passive chat
box waiting for the human to ask. A user should experience PEGO as a governed
operating cadence: prompts arrive when action, food, review, protected-time
boundary, or anticipation is due.

PEGO should not require all surfaces. The minimal viable experience is:

- Local protected private instance.
- Natural-language onboarding handled by an agent or runtime adapter.
- One delivered next directive.
- Outcome capture.
- Weekly review.

The adapter may use local commands internally, but the user experience should
not require the human to look up setup or operation commands during USER mode.

The adapter may also update protected private files internally. That must not
appear as the primary experience. A normal user should not see repository patch
output, planning traces, or setup transcripts after saying `Start PEGO`. They
should see a question about goals or circumstance, a directive, a fallback, or a
stop condition.

## Start PEGO Experience

When a user says:

```text
Start PEGO.
```

PEGO should respond as an operating system, not as a maintainer.

Good first responses:

- "State update: PEGO needs current circumstance before selecting a directive.
  Question: Where are you, how much time is available, what is your current
  energy, and what is the next hard stop?"
- "State update: PEGO can begin from the current operating brief. Next
  directive: spend 25 minutes clearing the highest-friction blocker in the
  active queue. Start when you are at the computer. Stop at the hard stop or if
  a protected-time conflict appears."

Bad first responses:

- "I am checking files and planning the setup."
- "Here is the diff I applied to the private queue."
- "I need to run these commands."
- "Let's build the system before using it."

If PEGO needs to repair its operating state, that repair happens behind the
surface. The visible result is still the next governed interaction.

## Acceptance Criteria

A first-time user should be able to:

- Understand PEGO's premise in under five minutes.
- Know what information stays private.
- Complete one intake phase without answering a giant questionnaire.
- See how their answers become protected operating state.
- Receive either one targeted question or one first directive candidate.
- Understand that PEGO owns strategy modeling, not the user.
