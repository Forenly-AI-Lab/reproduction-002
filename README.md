# Reproduction 002 — Tactile-in-the-loop lab-bench manipulation

**A humanoid pipettes on a lab bench in a 20-second clip. What of that is
actually established, and what of it could we reproduce here?**

The subject is a social-media claim about a method called **TacForcing**: that a
policy which keeps updating its actions from *fresh fingertip tactile feedback*
during contact reaches **69% average success** across three tasks — bottle
standing, liquid transfer, whiteboard wiping.

This repository does what [reproduction-001](../reproduction-001) did for the
`diffusion_pusht` model card: take the claim at face value, then find out how
much of it survives contact with a machine that is not the one it was measured
on.

---

**Study page:** <https://forenly.ai/lab-study/reproduction-002>

---

## Status

| Question | Answer |
|---|---|
| Is there a primary source (paper, code, project page)? | **Not located.** The post names "an August 26 arXiv preprint" but links none; two searches by title and by the distinctive task triple returned nothing matching. See [`evidence/source.md`](evidence/source.md) |
| What does the video actually show? | **One task, one trial, one success** — a pipette transfer. Not the three tasks, not the 69% |
| Does the video show tactile sensing? | **No.** No sensor overlay, no contact visualisation, no failure/recovery segment |
| Is the playback speed known? | **No.** The post itself says official project videos run at **5×**; whether this clip is one of them is unstated |
| Can we reproduce the *method* here? | **No — blocked at the sensor.** Our G1+Inspire model has no tactile channel at all |
| Can we reproduce the *task* here? | **Partially.** [AutoBio](https://github.com/autobio-bench/AutoBio) ships a pipetting scene that **runs on this host at 19.2x real time** ([bring-up](results/2026-09-01-autobio-bringup.md)) — but its liquid is a plane-vs-mesh volume model in Python, not fluid dynamics, and it never feeds back into the solver |
| Is that task the one in the video? | **No.** AutoBio's cell is UR5e + dexterous hand and UR5e + 2F85 gripper over centrifuge tubes. The overlap is the pipette and the liquid, not the robot or the glassware |

**One number has been measured, and it is not the study's number.** E1a ran
AutoBio's scripted expert 100 times: **100/100**, bit-deterministic across
processes, 11.6 s per episode
([record](results/2026-09-01-e1a-harness-baseline.md)). That is a *harness and
positioning* sanity baseline — the pipette is welded to the hand, so there is no
grasp in it — and it is not comparable to AutoBio's published π₀ score of 42.7 %,
which is a learned policy rather than an oracle.

**No grasp or tactile success rate has been measured yet.** What has been measured is the
harness: the stack runs here, at a known speed, on a known embodiment — see
[`results/2026-09-01-autobio-bringup.md`](results/2026-09-01-autobio-bringup.md).
No claim about the source's 69% is made or implied.

---

## What the clip shows

Full frame-by-frame reading: [`evidence/video-analysis.md`](evidence/video-analysis.md).
Contact sheets: [`evidence/frames/`](evidence/frames/).

A fixed camera on a wooden bench. Two anthropomorphic five-finger hands enter
from above; only the left-of-frame hand acts, the other is static for all 20
seconds. On the bench: an Erlenmeyer flask of blue liquid with a pipette
standing in it, and an empty beaker.

```
0–6 s    hand hovers above the flask, fingers open, no contact
7–9 s    grasps the pipette, lifts it clear of the flask
10–14 s  transports it over the beaker, lowers, dispenses
15–19 s  releases; the pipette comes to rest across the beaker, hand withdraws
```

It is a clean run. It is also **a single trial with no baseline, no failure
case, and no visible tactile signal** — which is to say it is a demonstration,
not evidence for 69%. That distinction is the whole point of this repository.

---

## The gate: why the method cannot be reproduced here as stated

Three hard blocks, in the order they bite:

**1. There is no tactile channel in our model.** The claim is specifically about
*fingertip tactile feedback closing the loop during contact*. Our G1+Inspire
physical contract records tactile as absent from the model — the Inspire hand's
mimic coupling resolves at contact, but no per-fingertip tactile signal is
exposed. A policy conditioned on a sensor we do not simulate cannot be
evaluated, only imitated. **This blocks the method, not the task.**

**2. MuJoCo does not simulate liquid.** "Liquid transfer" as filmed — aspirate,
transport, dispense — has no physical counterpart in our simulator. What
survives is the manipulation skeleton: grasp a thin cylinder, lift it clear,
transport it, hold orientation, release at a target. That is measurable.

**3. No GPU on this host.** Measured, not assumed: see [`COMPUTE.md`](COMPUTE.md).
Any learning here is CPU-bound; the first experiment is deliberately sized to
that.

---

## The first experiment

You cannot measure what touch adds until you know what sight alone does. So the
first run is not a tactile experiment at all — it is the **no-tactile baseline**
that any later tactile claim would have to beat.

**E1 — Can our hand grasp and transport a pipette-shaped body at all, without
tactile feedback?**

Falsifiable, and cheap: [`experiments/E1-no-tactile-baseline.md`](experiments/E1-no-tactile-baseline.md).

If E1 fails, the tactile question is premature and this repository says so. If
E1 succeeds at some rate, that rate becomes the floor every "touch matters"
claim — theirs or ours — has to clear.

---

## What this repository will not do

It will not report a success rate it did not measure, will not treat a
20-second clip as a result, and will not describe the claim as refuted. A
missing paper and a single demo video mean *unverified*, which is a different
and more honest word.
