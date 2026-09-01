# What AutoBio's pipette task actually is — 2026-09-01

Read off `upstream/AutoBio/autobio/mani_pipette.py`, not off the paper.

## Definition

| | |
|---|---|
| Scene | `model/scene/mani_pipette.xml` |
| Arms | UR5e + dexterous hand (`1/ur:`) · UR5e + Robotiq 2F85 (`2/ur:`) |
| Vessel | 50 ml screw-cap centrifuge tube (`5/centrifuge_50ml_screw_body`) |
| Randomised | initial liquid volume, uniform 15–45 mL; tube placement |
| Time limit | 30 s, early stop |

**Expert sequence.** Arm 2 moves the tube to a randomised pose. Arm 1 brings the
pipette above it, pushes the plunger, descends to `liquid_height - 0.01`,
aspirates, lifts.

**The plunger is one joint.** `ctrl[thj3]` — a thumb joint of the dexterous
hand. Push holds 0.8 for 150 steps; pull ramps 0.8 → 0.4 over 1600 steps.

**Success** (`check()`) is three simultaneous conditions:

```
horizontal distance tip ↔ tube  < 6.5 mm
tip below the liquid surface    > 5 mm
plunger control                 > 0.70
```

i.e. *did the tip actually enter the liquid while the plunger was depressed.*

## Two things the task does not do

**The pipette is bolted to the hand, not grasped.**

```python
frame = hand_body.add_frame(pos=[0.05022559, -0.18, 0.16], quat=[0,0,.7071,.7071])
frame.attach_body(pipette_body, "tl/", "")     # hand_body = 1/ur:dh:rh_base
```

It is attached to the hand's base body by a fixed frame. There is no pick-up, no
regrasp, no release. The five-finger hand is, for this task, a mount with one
moving thumb joint.

**Gravity is compensated on both arms** (`set_gravcomp`), so neither arm carries
its own weight.

## Why this matters to this study

The source clip's act is **grasp → transport → dispense → release**. AutoBio's
act is **position → press**. The part of the video the tactile claim is
specifically about — correcting *during contact*, while holding an object — is
the part AutoBio removed. With the pipette bolted on and gravity compensated,
what remains is a positioning problem, not a contact-rich manipulation one.

**Consequence for E1.** E1 was written to measure a no-touch grasp floor. E1a
cannot be that: there is no grasp in it to measure. E1a is still worth running,
for one narrow reason — it proves the harness reports honestly before we change
anything inside it. But its number is a positioning number and must never be
quoted as a manipulation baseline.

The grasp floor now has to come from E1b (our embodiment, our scene) or from a
modified AutoBio scene where the pipette is released into the world and picked
up. Which of those is cheaper is the next thing to find out — and either way,
the honest headline stands: **nobody has yet measured what we set out to
measure.**
