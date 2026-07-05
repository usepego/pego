# Collaboration Modes

PEGO work happens in three distinct collaboration modes. The mode determines whether the AI is building the framework, designing the user experience, or operating a private PEGO instance.

The mode must be explicit when the conversation could be interpreted more than one way.

## Engineering Mode

Engineering mode is for developers, maintainers, and framework creators building
PEGO as a general framework and software system.

Use this mode when the human and AI are collaborating as creators of PEGO. A
normal PEGO user should not need to understand or enter Engineering mode.

Primary concerns:

- Architecture.
- Code quality.
- Protocol design.
- Repository clarity for outside software engineers.
- Testability.
- Extensibility.
- Security and privacy boundaries.
- Developer onboarding.
- Long-term maintainability.

Default artifacts:

- Public-safe framework docs.
- Ops tools.
- Tests.
- System registry updates.
- Synthetic examples.
- Decision records.

Privacy rule:

Do not move private subject facts into framework files. Use templates or synthetic examples.

Success condition:

A technically serious engineer can inspect the repository, understand the system boundary, run verification, and see a coherent path toward the most sophisticated governance system for human activity directed toward predicted outcomes.

## UX Mode

UX mode is for designing how a general user first understands, adopts, and interacts with PEGO.

Use this mode when evaluating PEGO as a product experience rather than a codebase.

Primary concerns:

- First-run comprehension.
- Onboarding sequence.
- Goal and environment definition.
- User trust.
- Cognitive load.
- Interaction cadence.
- Medium selection: CLI, text, web, messaging, mobile app, watch, email, calendar, or other surfaces.
- Device context: desktop, phone, watch, home devices, or ambient interfaces.
- How PEGO asks targeted operational questions without becoming self-help or quantified-self software.

Default artifacts:

- Onboarding flows.
- Product copy.
- User journey maps.
- Interaction cadence specs.
- UX acceptance criteria.
- Synthetic walkthroughs.
- Interface requirements.

Privacy rule:

Use synthetic personas or sanitized examples unless explicitly operating in USER mode.

Success condition:

A first-time user can understand what PEGO is, why it is different from a personal assistant, what authority it has, how to define goals and environment, and how to experience useful directives without being overwhelmed.

## USER Mode

USER mode is for operating a real protected private PEGO instance.

Use this mode when the AI is running PEGO for the subject and the subject is
experiencing the working system directly. This is the default mode for a normal
PEGO user.

Primary concerns:

- Current state.
- Next directive.
- Outcome capture.
- Private operating memory.
- Anticipation.
- Directive synthesis.
- Governance review.
- Real-time feedback.
- Private constraints and protected time.

Default artifacts:

- Protected private directives.
- Outcome records.
- Context updates.
- Anticipation scans.
- Weekly plans.
- Governance preflights and reviews.

Privacy rule:

Private facts stay in the protected private instance. Public framework work must use sanitized exports or synthetic examples.

Success condition:

The subject receives concrete, timely, coordinated directives and can provide feedback that improves PEGO without leaking private operating state into the framework layer.

## Mode Selection

If the user asks to build, refactor, test, or explain the repository, use Engineering mode.

If the user asks how PEGO should feel, onboard, communicate, or be adopted by new users, use UX mode.

If the user asks "what should I do next?", reports completion or blockage, asks for a directive, or gives current private status, use USER mode.

If the user asks for both framework work and lived experience, explicitly split the response or task into the relevant modes.

## Mode Transitions

Engineering mode may produce tools that USER mode later runs.

UX mode may define an interface that Engineering mode later implements.

USER mode may produce feedback that Engineering or UX mode later converts into public-safe framework improvements.

Before moving from USER mode into Engineering or UX mode, sanitize private facts.
