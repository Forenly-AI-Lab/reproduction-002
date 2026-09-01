# AutoBio bring-up on this host — 2026-09-01

**First measurement of this study.** The question was narrow: does a ready-made
pipetting task exist, and does it run here? Both answers are yes. The third
answer, which we did not ask for, is the useful one: **it is not the task in the
video.**

## What was done

`AutoBio` ([autobio-bench/AutoBio](https://github.com/autobio-bench/AutoBio),
ICLR 2026) vendored under `upstream/AutoBio` at commit `0850421`, with its own
environment at `.venv-autobio` — a separate venv, because AutoBio pins
`mujoco==3.3.0` and ships a plugin binary (`libmjlab.so.3.3.0`) built against
it, while the rest of this machine runs MuJoCo 3.12. The two coexist; they do
not share a venv.

## The physics engine is MuJoCo 3.3.0, and the liquid is not physics

An early reading of this repository recorded that AutoBio "ships a liquid
plugin." **That was wrong, and the correction matters more than the error.**

`libmjlab.so.3.3.0` is a real MuJoCo plugin library, but what it registers is
`MJLAB_DETENT_PLUGIN`, `MJLAB_THREAD_PLUGIN` and `MJLAB_GRID_PLUGIN` — click
stops, screw threads and an SDF grid, i.e. the *mechanisms* of lab instruments.
None of it concerns liquid. `meshplane.so` is not a MuJoCo plugin at all; it is
a separate Python extension exposing `Mesh`, `MeshPlane`, `SurfaceDynamics`.

The liquid is a **plane cutting the container's interior mesh**, with volume
kept in Python (`initial_volume = uniform(15e-6, 45e-6)`). Height is a plane
distance:

```python
return container.liquid.surface.distance - body_pos_in_container @ surface_normal
```

It updates *after* each step, from Python, and does not feed back into the
solver — no `body_mass` or `body_inertia` is touched, so a full pipette weighs
exactly what an empty one does.

**So block 2 of the gate still stands.** AutoBio does not remove "MuJoCo has no
liquid"; it routes around it with geometry good enough to *score* a pipetting
task — how much was drawn, transferred, spilled — while sloshing, dripping and
viscosity are absent. Anything this study later says about liquid handling must
carry that qualifier.

Two traps, both real:
- The plugin is loaded by **relative path** (`mujoco.mj_loadPluginLibrary('./libmjlab.so.3.3.0')`).
  The process must start in `upstream/AutoBio/autobio`, or the scene will not load.
- `AutoBio` ships **no LICENSE file**. Research use is one thing; anything
  commercial needs a word from the authors first.

## Measured

Scene `model/scene/mani_pipette.xml` loads and steps. Pinned to two cores at
`nice -n 15`, with the rest of the machine untouched:

| | |
|---|---|
| Model | nq 46 · nv 45 · nu 25 · 61 bodies · 217 geoms |
| Timestep / integrator | 0.002 s · implicitfast |
| Throughput | **9,592 steps/s** = **19.2x real time** |
| Stability | qpos finite over 48k steps |

## The embodiment is not the video's

| | Video (the claim) | AutoBio `mani_pipette` |
|---|---|---|
| Arms | two five-finger anthropomorphic hands | **UR5e + dexterous hand** (18 act.) and **UR5e + Robotiq 2F85 gripper** (7 act.) |
| Acting hand | one five-finger hand | one dexterous hand, one parallel gripper — asymmetric |
| Vessels | Erlenmeyer flask -> glass beaker | centrifuge tubes, 50 ml, 10-slot rack, Vention table |
| Platform | unidentifiable (no torso in frame) | fixed bimanual cell, not a humanoid |

So the overlap with the source clip is **the pipette and the liquid**, not the
robot and not the glassware. That is worth stating plainly before anyone reads a
number from one and applies it to the other.

## What this changes about E1

E1 was written to build a pipette scene from scratch. It should not. Two paths
now exist and they answer different questions:

- **E1a — AutoBio as given.** Run its own expert on its own embodiment. Produces
  a number that is comparable to a published benchmark, and costs almost nothing
  now that the stack runs. It says nothing about our robot.
- **E1b — our embodiment in their task.** Swap G1 + Inspire into the pipette
  scene. Says something about our robot, and is the harder job: different
  kinematics, different hand, and our hand's reachable aperture is narrower than
  its datasheet suggests.

Run E1a first. It is cheap, it establishes that the harness is honest before we
change anything inside it, and a broken port is much easier to spot against a
working baseline than against nothing.

## Reproduce

```bash
cd upstream/AutoBio/autobio          # relative plugin path: cwd matters
MUJOCO_GL=osmesa nice -n 15 taskset -c 6,7 ../../../.venv-autobio/bin/python -c "
import mujoco; mujoco.mj_loadPluginLibrary('./libmjlab.so.3.3.0')
m = mujoco.MjModel.from_xml_path('model/scene/mani_pipette.xml')
print(m.nq, m.nv, m.nu)"
```
