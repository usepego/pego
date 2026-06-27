# Attention Governance

Attention governance decides what deserves the person's live attention.

PEGO should not treat leisure, sports, news, world events, culture, or enjoyable idling as noise by default. A successful life includes recovery, shared culture, curiosity, taste, play, and sometimes watching something simply because it is live and enjoyable.

The question is not "is this productive?" The question is "what is the best use of this attention window, given goals, obligations, happiness, recovery, rarity, and opportunity cost?"

## Scope

Attention governance covers:

- Live sports.
- World events.
- News.
- Cultural events.
- Movies, shows, music, and streams.
- Social media and feeds.
- Learning media.
- Ambient watching while doing chores or admin.
- Intentional rest.
- Unplanned distractions.

## Decision Modes

PEGO may choose:

- Watch live with full attention.
- Watch live while doing low-cognitive work.
- Watch highlights or summary later.
- Check score or outcome only.
- Defer to a scheduled leisure block.
- Skip.
- Escalate if the event creates safety, family, work, or civic implications.

## Inputs

- Current directive queue.
- Protected time.
- Work obligations.
- Energy and fatigue.
- Event rarity.
- Event personal importance.
- Social or relationship value.
- Cultural/world relevance.
- Recovery value.
- Risk of time sink.
- Multitask compatibility.
- Cost of missing it.
- Available highlight/summary quality.

## Event Option Shape

Use `pego/templates/attention-option.md`.

Structured implementations should preserve attention options using `pego/schemas/attention-option.schema.json`.

## Attention Decision Shape

Use `pego/templates/attention-decision.md`.

Structured implementations should preserve attention decisions using `pego/schemas/attention-decision.schema.json`.

The reference local decision runner lives at:

```text
ops/attention/decide_attention.py
```

The local wrapper command is:

```sh
python3 pegoctl attention --option private/attention/options/options.json
```

## Decision Rules

PEGO should:

1. Protect obligations and hard commitments.
2. Protect sleep, meals, and relationships from low-value drift.
3. Allow full attention when the event is rare, meaningful, restorative, or socially valuable.
4. Prefer highlights later when live value is low and opportunity cost is high.
5. Prefer multitask only when the other task is low-cognitive and safe.
6. Avoid pretending leisure has zero value.
7. Avoid letting low-intent media consume high-value focus blocks.
8. Record outcome if the choice affects energy, mood, connection, or goal progress.

## Governance

Most attention decisions are Level 1 recommendations.

Level 4 escalation may be required when:

- The event affects safety.
- The event materially affects work, legal, financial, or family obligations.
- The recommendation would violate protected time.
- The pattern suggests compulsive, avoidant, or harmful behavior.

## Review

After attention decisions, PEGO may ask:

- Was it worth watching live?
- Did it restore energy or create drift?
- Was multitasking actually compatible?
- Would highlights have been enough?
- Should similar future events be pre-classified?
