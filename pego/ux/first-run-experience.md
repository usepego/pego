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
| Health | Capture food, movement, sleep, medical boundaries | Health baseline |
| Voice | Capture communication style, taste signals, influences, and public positioning constraints | Voice and taste model |
| Authority | Capture grants, approvals, stop rules | Constitution authority section |

Each phase should fit in one short session.

The voice phase should avoid asking the user to describe their entire personality. Prefer targeted prompts that collect evidence:

- Link or paste one private writing sample that feels like you.
- Name one piece of writing, film, talk, software, object, or place that captures your taste.
- What would make a public essay about PEGO sound embarrassing or wrong?
- What kind of opportunity should public writing attract?
- What should never be used publicly without review?

## Interaction Cadence

Initial onboarding should work through text or CLI because those are easiest to audit and version locally.

Future product surfaces may include:

- Web app for constitution, goals, and review.
- Mobile app for next directive and outcome capture.
- Watch for brief directive prompts, timers, and completion.
- Calendar integration for anticipation.
- Slack or SMS for command-response interaction.
- Email for weekly review packets.

PEGO should not require all surfaces. The minimal viable experience is:

- Local protected private instance.
- Text-based onboarding packets.
- One next-directive command.
- Outcome capture.
- Weekly review.

## Acceptance Criteria

A first-time user should be able to:

- Understand PEGO's premise in under five minutes.
- Know what information stays private.
- Complete one intake phase without answering a giant questionnaire.
- See how their answers become protected operating state.
- Receive either one targeted question or one first directive candidate.
- Understand that PEGO owns strategy modeling, not the user.
