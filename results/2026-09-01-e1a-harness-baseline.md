# E1a — harness / positioning sanity baseline

> ## This is NOT a grasp baseline, and NOT a tactile reproduction.
>
> The pipette is welded to the hand in this task; there is no grasp in it to
> measure. The number below is the **scripted expert's** own success on a
> position-and-press task. It must never be quoted as a tactile-grasp result,
> and it is **not** comparable to AutoBio's published π₀ score of 42.7%, which
> is a *learned policy* on the same scene. An oracle and a policy are different
> quantities.

Run 2026-09-01. AutoBio unmodified, `mujoco 3.3.0`, two pinned cores at
`nice -n 19`.

## Result

| | |
|---|---|
| Episodes | **100** (seeds 0–99) |
| Success | **100 / 100** |
| Stage: tip entered liquid with plunger pressed | 100 % |
| Stage: liquid drawn (plunger released while submerged) | 100 % |
| Wall clock | 1,290 s total · **11.6 s per episode** |
| Simulated time | 14.23 s mean (13.79 – 14.99) |

**On reporting 100 %.** The binomial standard error at 100/100 is 0, which is an
artefact, not a fact. The honest statement is a one-sided bound: with 0 failures
in 100 trials the true success rate is **≥ 97.0 % at 95 % confidence** (rule of
three: the failure rate could still be as high as ~3 %). A run of 100 cannot
distinguish a perfect expert from one that fails 1 in 50.

## Determinism — the property worth having

The 3-episode smoke run and the 100-episode run were separate processes at
separate times. Their overlapping seeds agree exactly:

| seed | run A sim_time | run B sim_time | Δ | t_success A | t_success B |
|---|--:|--:|--:|--:|--:|
| 0 | 14.440000 | 14.440000 | **0** | 13.946000000001327 | 13.946000000001327 |
| 1 | 13.974000 | 13.974000 | **0** | 13.480000000001171 | 13.480000000001171 |
| 2 | 14.058000 | 14.058000 | **0** | 13.566000000001200 | 13.566000000001200 |

**Bit-deterministic**, to full float precision, across processes. That matters
more than the success rate: E1b compares two conditions on shared seeds, and a
paired comparison is only valid if the environment repeats. It does.

## Throughput — where the time actually goes

Raw physics on this scene runs at **19.2× real time**
([bring-up](2026-09-01-autobio-bringup.md)). With the expert in the loop it runs
at **1.23×** — 14.23 s of simulated time in 11.6 s of wall clock. So IK and
trajectory planning cost about **16× the physics**, and any budget for E1b
should be drawn from the 11.6 s figure, not the 19.2×.

At this rate, E1b's two conditions × 100 episodes ≈ **39 minutes** of wall clock
before rendering. That is affordable on this host.

## What this run proves, and only this

1. The harness runs end to end and the task completes.
2. `check()` latches correctly through all three of its stages — the flags are
   not silently stuck, which a single end-of-episode call would not have shown.
3. The environment is **bit-deterministic across processes**, so paired
   comparisons are sound.
4. Throughput is measured, not assumed: 11.6 s per episode with the expert.

It proves nothing about grasping, nothing about tactile feedback, and nothing
about the claim under audit. That was the point of running it first: a broken
port is far easier to spot against a harness already known to be honest.

## Method note

The only thing added to AutoBio's code path is polling. `check()` is a state
machine — `below_liquid` → `liquid_drawn` → lifted clear — and its flags never
latch unless it is evaluated every step. Calling it once at the end would have
reported 0 % on a run that in fact succeeded 100 times, which is a failure mode
worth naming: **an evaluation harness can report a wrong number without any
error being raised.** Polling an existing predicate is evaluation, not
modification; the task file was not touched.

Runner: [`experiments/e1a/run_e1a.py`](../experiments/e1a/run_e1a.py).
Per-episode records: `results/e1a-n100.json` (not committed — regenerate with
the runner; the run is deterministic).
