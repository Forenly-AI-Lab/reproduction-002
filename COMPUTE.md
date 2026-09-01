# Compute — measured, not assumed

Recorded 2026-09-01 on the host this repository runs on.

| | |
|---|---|
| CPU | INTEL(R) XEON(R) PLATINUM 8581C CPU @ 2.30GHz |
| Cores | 8 vCPU |
| Memory | 15 GB total, 8 GB available |
| Disk | 100G free of 242G on /home/ubuntu |
| GPU | **none** — `nvidia-smi` reports no device |
| Simulator | MuJoCo 3.12.0 |
| Python | Python 3.12.3 (`/home/ubuntu/foi/.venv-sim`) |

## What this rules in and out

**Out: training anything tactile.** No GPU, and the memory headroom is shared
with the other services on this host. Any policy learning at the scale the
source claim implies belongs on rented compute, not here.

**In: physics evaluation.** MuJoCo on CPU is enough to answer whether a grasp
and transport is even kinematically and dynamically available to our hand. That
is what E1 asks, and it is sized to run here.

## Environments on this host

Three venvs carry MuJoCo 3.12.0: `.venv-sim`, `.venv-lerobot`,
`.venv-lerobot-dataset`, all under `/home/ubuntu/foi`. E1 uses
`.venv-sim` — the one without an editable install to drag in, so a failure
there is a physics failure and not a packaging failure.

Robot assets live in `/home/ubuntu/foi/robot_assets`. Which G1+Inspire
description E1 binds to is recorded in the experiment note, not guessed here.
