# Capability: Score Tracking

`Score` (in `score.py`) tracks the player's current score for the active session and the all-time high score since the process started. It has no pygame dependency and no awareness of game state.

---

### Requirement: Score initialises to zero
A freshly constructed `Score` instance has `current == 0` and `high == 0`.

#### Scenario: New score starts at zero
- **WHEN** `Score()` is constructed
- **THEN** `score.current == 0` and `score.high == 0`

---

### Requirement: increment() adds exactly one point to the current score
`Score.increment()` increases `current` by 1. It does not affect `high`.

#### Scenario: Single increment raises current to 1
- **WHEN** `score.increment()` is called once
- **THEN** `score.current == 1`

#### Scenario: Multiple increments accumulate
- **WHEN** `score.increment()` is called N times
- **THEN** `score.current == N`

---

### Requirement: reset() saves the high score then clears the current score
`Score.reset()` sets `high = max(high, current)`, then sets `current = 0`. If the current score is lower than the existing high score, `high` is unchanged.

#### Scenario: High score is updated when current exceeds it
- **WHEN** `score.increment()` is called 5 times then `score.reset()` is called
- **THEN** `score.high == 5` and `score.current == 0`

#### Scenario: High score is not reduced on a worse session
- **WHEN** a session scores 5, `reset()` is called, then a session scores 3, `reset()` is called
- **THEN** `score.high == 5`

#### Scenario: Current score is zero after reset
- **WHEN** `score.reset()` is called after any number of increments
- **THEN** `score.current == 0`

---

### Requirement: High score persists across multiple resets within a process
`high` is a plain integer attribute on the `Score` instance. It is not persisted to disk and does not survive process restart. Within a single process, the highest score ever reached across all sessions is retained.

#### Scenario: High score survives multiple game resets
- **WHEN** a score of 5 is reached, reset, a score of 3 is reached, then reset again
- **THEN** `score.high == 5` after the second reset
