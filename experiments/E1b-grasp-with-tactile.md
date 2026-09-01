# E1b — grasp, with and without fingertip contact

**Status: designed, not implemented.** Nothing below has been run. No number in
this document is a result.

E1a establishes that the harness reports honestly on a *positioning* task. E1b
is the experiment the study actually set out to run: does contact information
change what the hand does, when the hand has to hold something?

---

## What has to change in the scene, and nothing more

Two facts read out of AutoBio's own model files decide the design.

**1. The pipette is not a free body.** It has no `freejoint`; it is welded into
the hand by `frame.attach_body(pipette_body, "tl/", "")` on `1/ur:dh:rh_base`
(see `results/2026-09-01-what-the-autobio-task-is.md`). To make grasping
possible at all, the pipette must become a free body in the world with a
`freejoint`, mass and inertia, starting in a rack or upright in a holder rather
than in the hand.

**2. The fingertip sensors already exist — they are commented out.**
`model/hand/dexhand021_right.xml` carries, disabled, the entire `<sensor>` block
and one site per fingertip:

```xml
<!-- <sensor>
<!-- <site name="rh_ffdistal" pos="0.025 0.003 0" size="0.01" type="sphere"/> -->
<!-- <site name="rh_thdistal" ... />  rh_mfdistal, rh_rfdistal, rh_lfdistal -->
```

All five fingers, already placed. The tactile channel is therefore a
*re-enablement*, not an invention: uncomment the sites and attach MuJoCo `touch`
sensors to them. That keeps the fork honest — we are not building a favourable
scene, we are turning on what the authors shipped and switched off.

**Also to remove: `set_gravcomp`.** Gravity compensation on both arms means the
arms never feel load. A grasp experiment in which the object's weight is
invisible to the controller is not a grasp experiment.

Everything else — robot, table, tube, liquid model, timestep, integrator — stays
untouched. Every change must be listed in the run record and justified in one
line, or it does not go in.

---

## The two conditions

| | vision / proprioception | fingertip contact |
|---|---|---|
| **E1b-control** | ✓ | ✗ |
| **E1b-tactile** | ✓ | ✓ |

Same seeds, same initial poses, same controller, same everything else. The only
difference is whether the contact channel reaches the action.

**The channel has to actually reach the action.** Adding a `touch` sensor and
logging it is not the experiment; that measures nothing. The comparison is only
meaningful if the tactile reading enters the control loop and can change the
command — otherwise E1b-tactile is E1b-control with extra logging, and any
difference between them is noise.

**What is compared** is not only final success. It is also *post-contact
correction*: after first contact, does the tactile condition change its command
in a way the control condition does not? A method that claims to "adjust during
contact" must show a difference inside the contact window, not only at the end.

---

## Checkpoint protocol

Not every episode is rendered — that would dominate the runtime on this
GPU-less host. Frames are captured at fixed stages, and numeric metrics are
recorded at every stage of every episode.

| # | Stage | Rendered | What the frame is for |
|---|---|---|---|
| 0 | Scene | ✓ once per config | Is the robot, hand, pipette and tube geometry what we think it is? |
| 1 | Approach | ✓ | Do the fingers actually align with the pipette? |
| 2 | Grasp | ✓ | Do the fingers wrap it, or pass through it? |
| 3 | Lift | ✓ | Does it stay in the hand, or slip? |
| 4 | Transport | ✓ | Is the task being performed, or approximated? |
| 5 | Contact | ✓ | What happens when the tip meets the liquid |
| 6 | Correction | ✓ both conditions | Does the tactile condition behave differently here? |
| 7 | Final | ✓ | Terminal pose beside the `check()` verdict |

### Metrics recorded at every checkpoint

Numbers, not impressions — this is what separates "the render looks right" from
"the physics did the right thing":

- finger ↔ pipette distance, per finger
- number of active contacts, hand ↔ pipette
- contact force (normal, and total wrench)
- **penetration depth** — the one that catches a fake grasp
- pipette pose, linear velocity, angular velocity
- hand joint positions and applied torques
- slip: pipette displacement in the hand frame since grasp

Reported per episode as a block that can be read at a glance:

```
GRASP
─────
contacts:        4
max penetration: 0.0 mm
pipette lifted:  ✓
pipette slip:    1.8 mm
grasp stable:    ✓
```

**Stage 0 is archived for every configuration.** We already know the robot in
the source video is not this robot. Any later reader must be able to ask "did
this number come from a real grasp by *this* hand" and answer it from an image,
not from prose.

---

## Sizing, and the honesty rules that carry over

- **100 episodes per condition**, not 20. Reproduction 001 read 80% at twenty
  episodes and 62% at five hundred on the same run.
- Both conditions share seeds, so the comparison is paired.
- Every rate is reported with its binomial standard error. At n = 100 near 50%
  that is about ±5 points, so a 6-point difference between the two conditions is
  **not** a result.
- Success is decomposed by stage — grasp / lift / transport / aspirate — never
  blended into one number, because a blended number hides which stage failed.
- Penetration and slip are reported even when success is high. A grasp that
  succeeds through mesh penetration is a simulator artefact, not a skill.

## What E1b cannot answer

It is still not the video's robot, not the video's glassware, and the liquid is
still a plane-vs-mesh model with no feedback into the solver. E1b can say
whether contact information changes this hand's behaviour on this task. It
cannot confirm or refute a 69% claim about a different system, and this study
will not pretend otherwise.
