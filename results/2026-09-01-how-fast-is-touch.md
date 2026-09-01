# How fast does touch actually change? — 2026-09-01

**The first number this study measured itself.** Everything before this was
inventory: what exists, what runs, what other people published. This is ours.

## The question

The claim under audit rests on a premise: that a policy fails because it
*"commits to a full motion from stale sensor data"*, and improves when it keeps
updating from *"fresh fingertip tactile feedback"*. That premise is testable
without reproducing the method at all. Either tactile changes fast enough that
staleness costs you something, or it does not.

## Method

[`zekaiwang/trex_dataset`](https://huggingface.co/datasets/zekaiwang/trex_dataset)
(MIT), 4 of 50 parquet shards = **459,560 frames at 30 fps**, real bimanual
teleoperation. Channel `observation.tactile_force`: 60 values per frame, 10
fingertips × 6-axis wrench. Compared against `observation.state` (58-D
proprioception) as a reference for "how fast does anything here move."

Video was not downloaded — the full dataset is **1,526 GB of mp4** against
**3.35 GB of parquet**, and the force channel lives in the parquet.

## What the signal looks like

```
|force|   median 6.05   p95 18.33   max 40.38      (sensor units)
20% of frames sit below 0.95 — plausibly no-contact
```

## 1. On average, touch is slow

Autocorrelation, 1.00 = unchanged:

| lag | 33 ms | 133 ms | 267 ms | 1.07 s | 4.27 s |
|---|--:|--:|--:|--:|--:|
| **tactile** | 0.997 | 0.989 | 0.976 | 0.893 | 0.655 |
| proprioception | 0.999 | 0.996 | 0.991 | 0.947 | 0.731 |

Tactile decorrelates only slightly faster than joint state. Holding the last
reading stale:

| held for | mean error | p99 | as % of signal |
|---|--:|--:|--:|
| 67 ms | 0.0075 | 0.118 | 1.3% |
| **133 ms** | **0.0165** | **0.296** | **2.8%** |
| 267 ms | 0.0297 | 0.578 | 5.0% |
| 1.07 s | 0.0855 | 2.029 | 14.4% |

**Read on averages alone, the premise looks weak.** A policy that re-reads touch
only every 133 ms is wrong by under 3% of signal magnitude. That is not the
picture of a channel going stale between control ticks.

## 2. But the average is the wrong statistic

Contact onsets — force crossing the median magnitude from below — occur
**4.9 times per minute**, and when one happens the force reaches **90% of its
peak in a median of 3 frames: 100 ms.**

So the signal is flat almost everywhere and a near-step function exactly where
it matters. A 133 ms stale hold is under 3% wrong on average and can miss an
entire contact transition. The p99 column is 18x the mean for the same reason:
the error is not spread out, it is concentrated in the onsets.

**This is the honest form of the claim.** It is not that tactile drifts away
from its last reading; it is that contact is an event, and events are what a low
control rate aliases. T-Rex's own design — four fast tactile ticks per slow
visuomotor tick, i.e. one tactile read per ~33 ms against a ~133 ms action tick
— lands exactly on the timescale we measure the onsets to occupy. That is a
coherent engineering reason. It is a different reason from the one the viral
post gives.

## Limits, stated

- **4 shards of 50**, mixed tasks, no per-task breakdown. Nothing here is
  weighted by which task the frames came from.
- **The contact-onset threshold is crude** — the median of `|force|` across all
  frames, not a calibrated contact detector. A different threshold moves the
  4.9/min and could move the 100 ms.
- **Units are unknown.** The dataset does not state whether the wrench is in
  newtons or raw sensor counts, so the percentages are relative and the
  absolute magnitudes are not interpretable.
- **This says nothing about whether TacForcing works.** It tests the premise the
  claim is argued from, on somebody else's data, and finds the premise true for
  a reason the claim does not give.

## Reproduce

The script is inline in this repository's history; the inputs are the four
shards `data/chunk-000/file-00{0..3}.parquet` of the dataset above at
`codebase_version` v3.0.
