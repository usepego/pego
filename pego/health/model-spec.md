# PEGO Health Model Spec

Reusable specification for PEGO health planning.

This file must not contain private health records or personal medical details.

## Purpose

The PEGO health model converts desired health states into daily food, movement, sleep, and recovery directives that preserve long-term execution capacity.

## Inputs

- Current weight.
- Target weight.
- Medical constraints.
- Sleep baseline.
- Exercise baseline.
- Food preferences.
- Food triggers.
- Time availability.
- Environment.
- Equipment.
- Protected time.
- Motivation and friction profile.
- Optional biomarkers and health metrics.

## Evidence Levels

The health model should support different evidence burdens. More data is not automatically better if it makes the system annoying, fragile, or obsessive.

### Level 0: Minimal Reported State

Use when the person wants useful health governance without quantified-self overhead.

Examples:

- Weight estimate or trend.
- Sleep report.
- Energy report.
- Hunger, craving, and sweet-trigger reports.
- Movement completion.
- Injuries, symptoms, or medical constraints.

### Level 1: Periodic Metrics

Use when labs, clinical measurements, or occasional home measurements are available.

Examples:

- Blood pressure.
- Resting heart rate.
- Weight and waist trend.
- A1C.
- Fasting glucose or other blood-sugar measurements.
- Lipids and metabolic labs.
- Clinician advice.

These metrics should inform risk awareness, directive selection, and escalation. PEGO must not diagnose, treat, or set clinical targets unless the private constitution and a qualified professional have supplied that guidance.

### Level 2: Continuous Telemetry

Use only when the person has opted in and the data improves decisions.

Examples:

- Wearable sleep, heart-rate, HRV, and activity data.
- Continuous glucose monitor data.
- Exercise logs.
- Nutrition logs.

Continuous telemetry should be summarized into actionable signals. It should not create constant monitoring obligations by default.

## Measurement Governance

PEGO should collect the least health evidence needed to improve directive quality.

Before asking for a new metric, the Health Agent should answer:

- What directive or strategy decision could this metric change?
- Is the metric required for safety, or only useful for precision?
- Can the same decision be made from lower-burden evidence?
- How often does the value need to change before PEGO should care?
- Does the metric require clinician interpretation?
- Could tracking the metric create anxiety, obsession, or avoidant behavior?

If the metric will not change a directive, risk classification, escalation, or strategy review, PEGO should not ask for it yet.

## Metric Tiers

Health metrics are organized by operating burden and decision value.

### Default Operating Signals

These are the normal health inputs PEGO can ask about without pushing the person into quantified-self mode.

- Body weight estimate or trend.
- Sleep duration and sleep quality.
- Energy level.
- Hunger, craving, and sweet-trigger exposure.
- Movement completion.
- Pain, injury, illness, symptoms, or medical constraints.
- Meal adherence to approved defaults.

These signals can drive daily food, movement, sleep, and recovery directives.

### Optional Periodic Metrics

These are useful when already available, when a goal needs more evidence, or when a risk condition makes them relevant.

- Waist or body composition trend.
- Blood pressure.
- Resting heart rate.
- A1C.
- Fasting glucose or other blood-sugar measurements.
- Lipids and metabolic labs.
- Clinician-supplied constraints or targets.

PEGO may ask for periodic metrics during onboarding, monthly review, or when a strategy is not working. It should not ask for them every day unless the person explicitly chooses that operating mode.

### Optional Continuous Signals

These should remain opt-in.

- Wearable activity, sleep, HRV, and heart-rate telemetry.
- Continuous glucose monitor summaries.
- Nutrition logs.
- Exercise logs.

Continuous signals should be summarized into decisions such as "sleep debt is high", "movement baseline is improving", or "food default appears to reduce cravings." PEGO should avoid presenting raw telemetry as a daily obligation.

## Blood Sugar Handling

Blood sugar is a valid PEGO health signal, but it is not mandatory for every user.

PEGO should consider asking about blood sugar when:

- The person has diabetes, prediabetes, metabolic syndrome, clinician guidance, or a family/risk context that makes glucose relevant.
- Weight-loss, energy, hunger, or craving strategy is not improving after lower-burden food and movement changes.
- The person already has A1C, fasting glucose, CGM, or clinician-provided glucose targets.
- A food strategy may need to be evaluated for adherence, hunger stability, or medical safety.

PEGO should treat glucose data as context for conservative food, movement, sleep, and escalation decisions. It must not diagnose, set clinical targets, recommend medication changes, or prescribe aggressive dietary protocols without qualified medical guidance.

## Biomarker Policy

Biomarkers such as blood sugar, A1C, blood pressure, lipids, resting heart rate, and sleep/recovery measures are optional evidence inputs.

PEGO may use them to:

- Notice health risk that should change directive conservatism.
- Decide when to prefer low-risk food, movement, sleep, or recovery defaults.
- Identify when medical review is needed.
- Track whether a strategy is plausibly improving the person’s health.

PEGO must not:

- Diagnose disease.
- Interpret abnormal results as medical advice.
- Recommend medication, supplement, fasting, aggressive dieting, or clinical intervention without escalation.
- Require daily tracking unless the person explicitly chooses that mode.

## Outputs

- Daily movement directive.
- Daily food directive.
- Sleep directive.
- Directive candidate table for synthesis.
- Weekly review.
- Minimum viable habit.
- Stop conditions.
- Escalation triggers.

## Executable Engine

The reference local health candidate runner lives at:

```text
ops/health/generate_candidates.py
```

It reads a protected health baseline and writes conservative Level 1 directive candidates for food, movement, sweets control, and sleep protection.

The protected baseline should follow:

```text
pego/schemas/health-baseline.schema.json
```

The output should feed directive synthesis, not bypass governance or medical review.

## Principles

- Start with adherence.
- Keep first actions small.
- Prefer defaults over willpower.
- Respect protected time.
- Avoid medical overreach.
- Escalate clinical questions.
- Treat subjective energy and mood as valid signals.

## Scenario Types

- Baseline.
- Minimum viable.
- Weight-loss focus.
- Travel.
- Illness/recovery.
- High-workload week.

## Review Cadence

- Daily directive.
- Weekly trend review.
- Monthly strategy review.
