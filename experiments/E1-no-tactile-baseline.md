# E1 — The no-tactile baseline

**Status: designed, not run.**

## Why this one first

The source claim is that fingertip tactile feedback lets a policy correct itself
*during* contact. Every version of that claim is a comparison: touch against no
touch. We do not have the touch side — our model has no tactile channel — so the
only honest first move is to nail down the other side.

If our hand cannot pick up a pipette-shaped body without touch, then "touch
helps" is untestable here and this repository should say so and stop. If it can,
at some rate, that rate is the floor. Every later claim, theirs or ours, has to
clear it.

## The question

> With vision-free, scripted control and no tactile feedback, at what rate can
> the G1 + Inspire hand grasp a pipette-shaped cylinder, lift it clear of a
> container, transport it 15 cm, and release it over a target — in MuJoCo?

## Scope, stated up front

This is **not** a reproduction of the source method. It reproduces the
*manipulation skeleton* of the filmed task with the fluid removed, because
MuJoCo has no liquid. Aspirate and dispense are out of scope and are not
silently replaced by a proxy that scores easier.

What is deliberately excluded, and why:

| Excluded | Reason |
|---|---|
| Liquid | Not simulated. Scoring a "transfer" without it would be theatre |
| Tactile conditioning | No sensor in the model. This is the gate, not a shortcut |
| Learned policy | No GPU on this host. Scripted control isolates the physics question |
| Vision | Adds a failure mode that would confound a physics answer |

## Setup

- Simulator: MuJoCo 3.12.0, `/home/ubuntu/foi/.venv-sim`
- Robot: the G1 + Inspire description in `/home/ubuntu/foi/robot_assets` —
  **record the exact file and its hash in the results, do not assume it**
- Object: a capsule/cylinder at pipette scale, mass and friction recorded, not
  defaulted
- Control: scripted joint targets through the same PD path the existing
  controllers use. If the gains come from anywhere other than the published
  contract, that is a finding, not a detail

## Protocol

1. Fix a seed. Randomise the object's start pose within a stated envelope.
2. 100 trials. Not 20 — reproduction-001 recorded 20 episodes reading 80% where
   500 read 62%, and that error is not repeating here.
3. Score four separate gates per trial, never one blended number:
   - **G1 grasp** — object held, not dropped, at lift
   - **G2 clear** — object fully out of the container
   - **G3 transport** — moved to the target region without collision
   - **G4 release** — released within the target, still in a defined pose
4. Report each gate's rate with its binomial standard error. A 100-trial rate
   carries roughly 5 points of SE near 50% — say that out loud so nobody reads
   a 6-point difference as a result.

## What would count as failure of E1

G1 below the point where the later stages have anything to run on. If the hand
cannot close on a thin cylinder at all, the finding is about the Inspire hand's
reachable aperture and mimic coupling, not about tactile sensing — and that is
a result worth writing down, because it would mean the filmed task is out of
reach for our embodiment before any policy question is asked.

## Recording

Results go in `../results/` as JSON plus a written note. The note states the
version of every moving part, and what was measured versus what was assumed.
No number enters the README until it exists in `results/`.
