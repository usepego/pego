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
