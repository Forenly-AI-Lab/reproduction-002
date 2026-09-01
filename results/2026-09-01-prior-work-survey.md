# Prior work: what already exists — 2026-09-01

The question was whether anyone has already built the thing this study is
circling. Answer: **nobody has built all of it, but the two halves both exist,
released and openly licensed** — and one of them is a sharper version of the
very claim we are auditing.

Every licence and size below was read from the Hugging Face / GitHub API on
2026-09-01, not from a paper.

## The find: T-Rex

[Project](https://tactile-reactive-dexterous.github.io/) ·
[code](https://github.com/ZhuoyangLiu2005/T-Rex) ·
[dataset](https://huggingface.co/datasets/zekaiwang/trex_dataset)

| | |
|---|---|
| Robot | `dexmate_vega1_and_sharpa_wave` — bimanual, 2 × 7-DoF arms, 2 × **22-DoF** hands |
| Tactile | **5 fingertip sensors per hand.** `observation.tactile_force` shape **[60]** (10 fingertips × 6-axis wrench) plus per-finger raw and deformation images at 240×320×3 |
| Size | **5,464 episodes · 5,473,459 frames · 30 fps** |
| Format | **LeRobot codebase v3.0** — the format our own `.venv-lerobot` already reads |
| Licence | **MIT**, not gated, 47k downloads |
| Code | MIT, active (pushed 2026-08-27) |
| Sim | **None.** Real robot only |

Its 12-task benchmark includes an *Acid-Base Neutralization* task, so lab
chemistry is inside its scope.

**Why this matters here.** Gate block 1 says we cannot evaluate the method
because our model has no tactile channel. That is true *in simulation*. T-Rex
routes around it from the other side: real per-fingertip tactile, already
recorded, openly licensed, in a format we can load on CPU today. The question
"does fingertip feedback during contact change anything" becomes answerable from
data without a tactile simulator.

**And the comparison is itself a finding.** T-Rex is what the TacForcing post is
not: a named robot, a released benchmark, released code, an MIT dataset of 5,464
episodes. Same research question, opposite standard of evidence. Any writing
this study does about the claim should say so.

## The task half: AutoBio's own data

[`autobio-bench/pipette-mujoco`](https://huggingface.co/datasets/autobio-bench/pipette-mujoco) —
**MIT**, ungated, 10K–100K rows, parquet + video. There is a
[`pipette-blender`](https://huggingface.co/datasets/autobio-bench/pipette-blender)
companion.

This is the recorded data for **the exact scene already running here**. It means
E1a does not have to generate its own episodes before it can check anything: the
authors' own rollouts are downloadable, so our harness can be checked against
them rather than only against itself.

Note the licence asymmetry: the datasets are MIT, but the AutoBio **code** ships
no LICENSE file at all. Data and code are not covered by the same terms.

## Also found, and why they are not the path

| Project | What it is | Why not |
|---|---|---|
| [Pipette](https://github.com/hbhuiyou/Pipette) ([paper](https://arxiv.org/pdf/2606.12936)) | Wet-lab platform, 12 tasks, 43+ re-editable lab assets, HDF5 + LeRobot datasets | **Isaac Sim 5.1 + Isaac Lab 2.3.2, NVIDIA GPU required.** Blocked on this host. Franka + gripper, not a dexterous hand |
| [TactiDex](https://arxiv.org/html/2607.09190v1) | Tactile-rich bimanual hand–object dataset, whole-hand signals + object 6D | Release not verified; T-Rex covers the same need with a confirmed MIT licence |
| [`Cyril08000/record-pipette-flacon`](https://huggingface.co/datasets/Cyril08000/record-pipette-flacon) | Real-robot pipetting into a flacon | **No licence stated** — unusable for anything we would publish |
| `cyberorigin/pipette`, `lerobotForScienceEdu/Pipette_Squeeze-*` | Small pipetting recordings | Small, and not aimed at the tactile question |
| [Chemistry3D](https://github.com/huangyan28/Chemistry3D) | Chemistry sim with fluids, pouring, stirring | Isaac Sim / Omniverse, GPU required |

## What this changes

Two independent lines are now open, and they need different resources:

- **Simulation line** (AutoBio, CPU, running today) — has the lab task, has no
  grasp and no tactile.
- **Data line** (T-Rex, CPU to load, MIT) — has the grasp and the tactile, on a
  real robot, and has no simulator.

Neither is the video. Together they cover it, and the seam between them is where
an honest contribution would sit. Nothing here has been run yet; this note
records what exists, not what works.
