# Example First-Use Walkthrough

This is a synthetic acceptance test for PEGO's first-use experience. It shows
what a normal user should experience from discovering PEGO through receiving
and completing a first meaningful directive.

The walkthrough is intentionally concrete. It is not a promise that every
adapter, provider, OAuth flow, command name, or directive will work exactly this
way. Product implementations may differ, but they should preserve the same
governance lifecycle.

## Test Persona

Name:

```text
Jordan
```

Situation:

```text
Jordan has a demanding job, vague financial anxiety, inconsistent food defaults,
several venture ideas, a cluttered home environment, and not enough confidence
that ordinary productivity tools will choose the right next action.
```

Goal of the test:

```text
Jordan should move from awareness to one completed directive without needing to
understand PEGO internals.
```

## Step 1: Awareness

### User Action

Jordan finds:

```text
usepego.com
```

### Page Experience

The first screen says:

```text
PEGO
Personal Executive Governance OS for agent-directed life decisions.

PEGO turns goals, constraints, current state, and feedback into governed
directives: what to do next, what to defer, what to escalate, and what to
review.
```

The page shows a short lifecycle:

```text
Goal or concern
-> domain-agent recommendation
-> council decision
-> directive candidate
-> next directive
-> outcome review
```

### User Understanding

Jordan should understand that PEGO is not:

- A habit tracker.
- A notes app.
- A generic assistant.
- A financial, medical, or legal execution bot.

Jordan should understand that PEGO is:

- A governed agent framework.
- A system for deciding what should happen next.
- Constrained by privacy, authority, reversibility, dissent, and review.

### Pass Condition

Jordan can say:

```text
This helps me delegate life tradeoff decisions, not just organize tasks.
```

## Step 2: Install

### User Action

The site gives a direct install command:

```sh
uv tool install usepego
```

Fallback:

```sh
pipx install usepego
```

Then:

```sh
pego start
```

or:

```sh
pegoctl start
```

### Product Requirement

The site should make clear whether the command is currently available,
pre-alpha, or illustrative. The user should not discover package maturity by
trial and error.

### Adapter Behavior

The installer:

- Installs the PEGO framework package.
- Creates or locates a protected private instance.
- Explains where private data will live.
- Runs readiness checks internally.
- Does not print private contents.
- Does not ask the user to read framework files.

### Pass Condition

Jordan sees a PEGO start surface, not a stack trace or framework tutorial.

## Step 3: Connect LLM Runtime

### User Action

PEGO says:

```text
PEGO needs an LLM runtime to operate. Choose a provider.
```

Options:

```text
OpenAI
Anthropic
Local model
Hosted PEGO runtime
Configure later
```

Jordan chooses:

```text
OpenAI
```

### Authentication Flow

If the adapter supports OAuth, PEGO opens the provider authorization flow.

If the adapter uses an API key, PEGO asks for the key and explains where it is
stored.

### User Sees

```text
PEGO will use your selected model provider to reason over your protected
private instance. PEGO does not need authority to execute financial, medical,
legal, relationship, or career-risking actions.
```

### Product Requirement

PEGO must distinguish:

- Model access.
- Private data storage.
- Tool access.
- Execution authority.

Connecting an LLM does not grant PEGO authority to execute life decisions.

### Pass Condition

Jordan understands:

```text
The LLM powers reasoning. PEGO's constitution controls authority.
```

## Step 4: Private Instance Boundary

### PEGO Asks

```text
Where should PEGO store your protected private instance?
```

Default:

```text
Use a local private folder with backup reminders.
```

Other choices:

```text
iCloud Drive
Dropbox
OneDrive
Encrypted local folder
Advanced custom path
```

### PEGO Explains

```text
The reusable PEGO framework contains protocols and schemas. Your private
instance contains your real goals, constraints, directives, and outcomes.
```

### PEGO Asks

```text
Before PEGO starts directing you, what is one thing PEGO must not disturb or
override?
```

### Example User Answer

```text
Do not disturb evening family time unless there is a safety issue.
```

### Behind The Surface

PEGO records:

- Protected time constraint.
- Default authority: Level 1 Recommend.
- Stop rule candidate.

### Pass Condition

The first sensitive prompt is about boundary, not account balances, health
metrics, or private details.

## Step 5: Explain What To Expect

### PEGO Says

```text
PEGO will ask a few targeted questions, then issue one directive. It will not
ask you to design a full life plan.

Domain agents will evaluate health, money, work, venture creation, home,
relationships, exploration, happiness, and governance. The council will select
one next directive or ask one missing question.
```

### Product Requirement

This explanation should be short. It should orient the user without turning
onboarding into documentation.

### Pass Condition

Jordan understands that PEGO may ask questions across domains because the
council needs enough state to choose well.

## Step 6: Aim

### PEGO Asks

```text
What future state would make life clearly better, and what should PEGO preserve
even while pushing toward it?
```

### Example User Answer

```text
I want more financial freedom, better energy, and a path toward independent
work. Preserve my relationship time and do not push me into reckless money or
career moves.
```

### Behind The Surface

PEGO updates:

- Life aim.
- Happiness constraints.
- Governance constraints.
- Candidate active programs:
  - Financial trajectory.
  - Health and energy.
  - Venture or independent work.
  - Relationship protection.

### Pass Condition

PEGO now has enough aim context to avoid optimizing only for productivity or
money.

## Step 7: Current Circumstance

### PEGO Asks

```text
Where are you, how much time is available, what is your current energy, and
what is the next hard stop?
```

### Example User Answer

```text
Home. 45 minutes. Medium energy. I need to stop before dinner.
```

### Behind The Surface

Operations records:

- Location: home.
- Available time: 45 minutes.
- Energy: medium.
- Hard stop: before dinner.

### Pass Condition

The first directive must fit this real window.

## Step 8: Domain Scan

### PEGO Asks

```text
What is the main pressure PEGO should govern first: health/energy,
money/runway, career/work, venture creation, home, relationships, exploration,
or something else? Include what is true now and what must not be disturbed.
```

### Example User Answer

```text
Health and money are both active. I have been eating reactively and I keep
avoiding financial clarity. Do not ask me to move money today.
```

### Behind The Surface

Agents form initial positions:

- Health: improve next food default before energy degrades.
- Finance: do not execute; first clarify accounts, obligations, unknowns, or
  one safe educational step.
- Career/Venture: independent work matters, but no deep strategy directive
  should displace immediate energy or dinner boundary.
- Relationships: preserve dinner boundary.
- Happiness: avoid turning the first session into anxiety management or
  administrative overload.
- Governance: no financial execution authority; Level 1 only.
- Operations: choose one low-risk directive that fits the window.

### Pass Condition

The user has exposed enough cross-domain pressure for the council to make a
selection.

## Step 9: Council Synthesis

### Internal Council Decision

The council compares:

```text
Health directive: establish next-meal protein/fiber default.
Finance directive: read one public-safe finance primer or list financial unknowns.
Venture directive: spend 25 minutes naming one customer pain.
Home directive: clear visible friction before dinner.
```

Council result:

```text
Select health directive now.
Defer finance into a safe clarity block.
Defer venture and home.
Protect dinner boundary.
No execution authority granted.
```

### Why This Is Better Than A Random Suggestion

The yogurt directive should not be arbitrary. It should come from:

- The user's energy aim.
- The stated reactive eating pattern.
- The available time and home/grocery context.
- The dinner hard stop.
- Finance/career deferral because execution risk or cognitive load is higher.

### Pass Condition

The first directive is visibly governed, even if the full council transcript is
not shown.

## Step 10: First Directive

### PEGO Says

```text
State update: PEGO has enough current state to begin at Level 1.

Next directive: Protein/fiber anchor for the next meal.

Time box: next meal only.

Start condition: when you choose or prepare food next.

Do this: make the meal include one clear protein plus one fiber item. Examples:
Greek yogurt + berries, eggs + fruit, chicken/fish + vegetables, or
beans/lentils + vegetables.

Reason: this improves the active energy constraint without turning day one into
a full plan.

Fallback: if the meal is already fixed, add the smallest available
protein/fiber side.

Deferred: finance clarity, venture work, and home reset.

Stop condition: stop before dinner boundary or if the directive conflicts with
a medical or dietary constraint.

Next check-in: after the meal, send: Meal done: __. Available: __ minutes.
```

### Alternative If Food Is Not Available

If PEGO knows the user lacks the food default and grocery access fits the
window:

```text
Next directive: buy one protein/fiber default for the next two meals.

Do this: go to the nearest normal grocery source and buy one plain Greek yogurt
or equivalent protein default plus one fruit or fiber item. Do not expand the
trip into a full grocery run.
```

### Pass Condition

The directive is concrete, low-risk, reversible, and tied to the user's stated
state.

## Step 11: Finance Follow-Up Without Overreach

### PEGO May Later Say

```text
Next directive: finance clarity block.

Time box: 20 minutes.

Do this: list the accounts, obligations, and unknowns PEGO needs to model your
financial trajectory. Do not move money, open accounts, trade, cancel, or
subscribe to anything.

Reason: financial anxiety requires a map before recommendations can be trusted.

Fallback: if account details are unavailable, list only the unknowns.

Deferred: investment execution and career-risking moves.
```

### Blog Or Reading Directive Requirement

If PEGO recommends reading an external finance blog or article, it must explain
why that source is selected and keep the directive low-risk:

```text
Do this: read this one public explanation only to understand a concept. Do not
take financial action from it.
```

PEGO should not send the user to an unfamiliar finance source as the first
finance directive unless the source is relevant, trustworthy, and clearly
bounded.

### Pass Condition

Finance education can happen, but PEGO does not create accidental investment,
tax, legal, or account-action authority.

## Step 12: Outcome Capture

### User Reply

```text
Meal done: Greek yogurt and berries. Available: 25 minutes.
```

### PEGO Records

- Directive completed.
- Food default worked.
- Time remaining.
- Next candidate window.
- Health evidence for future directives.

### PEGO Responds

```text
State update: meal anchor completed; 25 minutes available.

Next directive: finance clarity list.

Time box: 20 minutes.

Start condition: stay at the computer.

Do this: list the financial unknowns PEGO needs before it can model runway,
risk, or freedom path. Do not move money or log into accounts unless already
available.

Reason: the energy correction is complete and finance pressure remains active
without requiring execution.

Fallback: if details are not available, write only the unknowns.

Deferred: venture and home.

Next check-in: send: Finance list done/blocked: __.
```

### Pass Condition

The next directive changes because the user reported an outcome. PEGO is now
operating a loop, not issuing isolated advice.

## Step 13: Day-One Success

Day one succeeds if:

- Jordan installs or starts PEGO without learning internals.
- Jordan connects an LLM runtime or selects a hosted runtime.
- PEGO establishes privacy and authority before sensitive intake.
- PEGO asks about aim, circumstance, and domain pressure.
- Domain agents form initial positions behind the surface.
- Council selects one directive and defers others.
- Jordan completes or blocks the directive.
- PEGO records the outcome and chooses a better next move.

Day one fails if:

- Jordan sees setup logs, diffs, stack traces, or file paths as the main
  experience.
- PEGO asks for too much private detail before explaining authority.
- PEGO gives a random grocery, blog, finance, or productivity suggestion with
  no connection to stated goals.
- PEGO recommends financial, medical, career, relationship, or privacy-impacting
  action without governance review.
- PEGO ends with "setup complete" but no meaningful directive.

## Test Assertions

An automated or manual UX test should assert:

- The first visible product output is not adapter telemetry.
- The LLM-provider connection does not imply execution authority.
- The private instance boundary is explained before sensitive questions.
- The first directive is derived from stated aim and current circumstance.
- The first directive includes a time box, start condition, concrete action,
  reason, fallback, deferral, stop condition, and next check-in.
- Finance or health content stays within Level 1 unless authority is granted
  and governance review passes.
- The first outcome changes the next PEGO response.
