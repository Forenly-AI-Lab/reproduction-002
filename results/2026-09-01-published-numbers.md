# The published numbers — 2026-09-01

Every candidate project's repo, dataset and reported result in one place. Read
from the papers and project pages, with the licence and size fields read from
the GitHub / Hugging Face APIs rather than from prose.

---

## T-Rex — tactile, real robot

**Repo** [ZhuoyangLiu2005/T-Rex](https://github.com/ZhuoyangLiu2005/T-Rex) · MIT · 294★ · active 2026-08-27
**Dataset** [`zekaiwang/trex_dataset`](https://huggingface.co/datasets/zekaiwang/trex_dataset) · **MIT**, ungated
· 5,464 episodes · 5,473,459 frames · 30 fps · LeRobot v3.0 · `dexmate_vega1_and_sharpa_wave`
· tactile: `observation.tactile_force` [60] + per-finger raw & deformation images 240×320×3

**Result: 65% macro-average over 12 tasks, 16 trials per task.**

| Task | % | | Task | % |
|---|--:|---|---|--:|
| Flip Page | 96 | | Extract Card | 70 |
| Split Cup | 78 | | Wipe Plate | 69 |
| **Acid-Base Neutralization** | **76** | | Apply Toothpaste | 66 |
| Transfer Egg | 75 | | Sort Mahjong | 65 |
| Deal Poker | 57 | | Open Lock | 47 |
| Refill Tablet | 41 | | Screw Lightbulb | 35 |

**Baselines** EgoScale 35 · π₀.₅ 17 · Tactile-VLA 15 · RDP 6 · π₀.₅+tactile 6 · ViTacFormer 3

**Ablation — this is the number that matters to us:** removing tactile costs
**23 points (65% → 42%)**. It is the only published measurement we have found of
what touch is actually worth.

---

## AutoBio — simulation, lab tasks (running on this host)

**Repo** [autobio-bench/AutoBio](https://github.com/autobio-bench/AutoBio) · **no LICENSE file** · ICLR 2026
**Dataset** [`autobio-bench/pipette-mujoco`](https://huggingface.co/datasets/autobio-bench/pipette-mujoco) · **MIT** · 10K–100K rows
· companion [`pipette-blender`](https://huggingface.co/datasets/autobio-bench/pipette-blender)

**Protocol** 16 tasks in 3 difficulty tiers · **100 evaluation episodes per task**
· 20 and 100 training demos · 30k steps · 3 seeded runs · 792k frames total

| Task | π₀ | RDT |
|---|--:|--:|
| Close thermal cycler lid | 99.7 ± 0.3 | 100.0 ± 0.0 |
| Open thermal cycler lid | 96.0 ± 2.1 | 99.0 ± 0.6 |
| Pick up centrifuge tube | 53.7 ± 5.9 | 57.7 ± 1.2 |
| **Aspirate with pipette** | **42.7 ± 1.8** | **0.3 ± 0.3** |
| Transfer centrifuge tube | 40.7 ± 5.4 | 2.0 ± 1.2 |
| Unscrew centrifuge tube cap | 21.3 ± 1.5 | 2.7 ± 1.2 |
| Load centrifuge rotor | 14.7 ± 1.3 | 1.0 ± 1.0 |
| Operate thermal mixer panel | 7.5 ± 0.6 | 1.6 ± 0.5 |
| Screw on centrifuge tube cap | 2.0 ± 0.6 | 8.3 ± 4.4 |

**π₀ = 42.7% on aspirate-with-pipette is this study's reproduction target.** It
is a published number on the exact scene already running here — the same shape
of claim [reproduction-001](../reproduction-001) went after.

---

## Pipette (hbhuiyou) — simulation, Isaac Sim, blocked here

**Repo** [hbhuiyou/Pipette](https://github.com/hbhuiyou/Pipette) · [paper](https://arxiv.org/abs/2606.12936) · Isaac Sim 5.1 + Isaac Lab 2.3.2 · **NVIDIA GPU required**
**Dataset** HDF5 + LeRobot on Hugging Face · **episode count not published**
**Robot** Franka Panda + gripper (also xArm7, Nero D435) — no dexterous hand

**Protocol** 12 tasks · 30 demos per task · **number of evaluation trials not published**

| Policy | Base | + sim augmentation | Δ |
|---|--:|--:|--:|
| ACT | 60.3 | — | — |
| SmolVLA | 40.4 | **71.8** | +31.4 |
| π₀ | 37.3 | 44.1 | +6.8 |

---

## TacForcing — the claim under audit

**Repo** none found · **Dataset** none · **Paper** cited as "August 26 arXiv preprint", [not located](../evidence/source.md)

**Reported** 69% average across bottle standing, liquid transfer, whiteboard
wiping. No trial count, no baseline, no ablation, no named robot, no code.

---

## What the table says

**1. 69% is not a remarkable number.** It sits inside the band everyone else
reports — T-Rex 65%, Pipette/ACT 60.3%, AutoBio/π₀ 42.7% on the closest single
task. What separates the others from TacForcing is not the score, it is that
theirs arrive with a denominator.

**2. Read the error bars carefully — they are not all the same quantity.**

| | reported | binomial SE at that n |
|---|---|---|
| T-Rex, 16 trials/task | 65% | **±11.9 points** |
| AutoBio pipette, 100 episodes | 42.7 ± 1.8 | **±4.9 points** |
| Pipette (hbhuiyou) | 60.3% | n not published — uncomputable |

AutoBio's ±1.8 is the spread across 3 seeds, **not** the sampling error of the
100 episodes; the two answer different questions and the smaller one is the one
that gets quoted. T-Rex's 16 trials per task carry a sampling error of about
±12 points, which is wider than most of the gaps between its own tasks. None of
this makes the work wrong. It does mean a 4-point difference between any two
rows in this document is noise.

**3. Only one project has measured what touch is worth: −23 points.** That is
T-Rex's ablation, on a real robot, with the dataset released under MIT. If this
study wants to say anything about tactile manipulation, that is the number to
stand next to — not the 69%.
