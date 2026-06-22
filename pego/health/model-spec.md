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
