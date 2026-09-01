# E1b — every change to the AutoBio scene, and why

**Upstream is not modified.** `upstream/AutoBio/` is read-only in this
experiment; nothing in it was edited. The forked files live here, in
`experiments/e1b/scene/`, and reach back into the upstream tree for every asset
they do not change.

The rule for this fork: *change only what makes the experiment possible, and
list every change*. If a change is not in this document, it was not made.

---

## Forked files

| File | Forked from | Why |
|---|---|---|
| `scene/e1b_grasp.xml` | `model/scene/mani_pipette.xml` | free pipette; points at the forked robot |
| `scene/ur5e_dexhand021_right_e1b.xml` | `model/robot/ur5e_dexhand021_right.xml` | points at the forked hand |
| `scene/dexhand021_right_e1b.xml` | `model/hand/dexhand021_right.xml` | fingertip touch sensors enabled |

Everything else — table, second arm and its 2F85 gripper, centrifuge rack, 50 ml
tube, pipette model, lights, cameras, meshes, and the entire `<option>` block
(`implicitfast`, `impratio=10`, `cone=elliptic`, `noslip_iterations=2`,
`multiccd`) — is loaded unchanged from upstream.

---

## Change 1 — fingertip tactile sensors (Phase 4)

`dexhand021_right_e1b.xml`. **Nothing was invented.** AutoBio ships these
sensors and their sites, commented out; the fork uncomments them and changes
nothing else about the hand.

Six edits, at these upstream line numbers:

| Line | Was | Now |
|---|---|---|
| 55 | `<!-- <site name="rh_thdistal" pos="0.025 0.003 0" size="0.01" type="sphere"/> -->` | uncommented |
| 78 | `<!-- <site name="rh_ffdistal" ... /> -->` | uncommented |
| 100 | `<!-- <site name="rh_mfdistal" ... /> -->` | uncommented |
| 123 | `<!-- <site name="rh_rfdistal" ... /> -->` | uncommented |
| 146 | `<!-- <site name="rh_lfdistal" ... /> -->` | uncommented |
| 222–228 | `<!-- <sensor> … five <touch> … </sensor> -->` | uncommented |

Plus one path fix, forced by the fork living outside the AutoBio tree:
`meshdir="../../assets"` → `meshdir="../../../upstream/AutoBio/autobio/assets"`.

**Verified after load:** the model reports 5 sensors —
`1/ur:dh:touch_rh_{th,ff,mf,rf,lf}distal` — and they read `[0 0 0 0 0]` with the
hand away from the object, which is the correct no-contact reading.

## Change 2 — the pipette becomes a free body (Phase 2)

Upstream never places a pipette in the scene at all. It is created in Python, in
`Pipette.prepare()`, and welded to the hand:

```python
frame = hand_body.add_frame(pos=[0.05022559, -0.18, 0.16], quat=[0,0,.7071,.7071])
frame.attach_body(pipette_body, "tl/", "")   # hand_body = 1/ur:dh:rh_base
```

E1b removes that weld and puts the pipette in the world instead, added to
`e1b_grasp.xml`:

```xml
<body name="e1b_pipette_root" pos="0.04 -0.40 0.836" quat="0.70710678 0.70710678 0 0">
    <freejoint name="e1b_pipette_free"/>
    <attach model="pipette" body="pipette" prefix="tl/"/>
</body>
```

The `tl/` prefix is kept deliberately, so every site name the upstream code
already knows — `tl/tip_site` above all — still resolves.

**Mass and inertia are not invented either.** They come from the unchanged
pipette mesh and MuJoCo's default density: **91.5 g**, inertia
`[1.34e-4, 1.30e-4, 7.33e-6]`. Long and thin, as a pipette should be.

**Placement is measured, not guessed.** The pipette model carries an internal
offset of `(0.06, 0, -0.15)` from its attach frame, which rotates with the root
body; the root pose above is solved backwards from a desired world pose of
`(0.10, -0.25, 0.836)`, inside arm 1's workspace, on the table between the arm
base `(0, -0.5, 0.824)` and the tube `(-0.072, -0.018, 0.829)`.

### Physics verification (Phase 2 gate)

Dropped with no control, 3 s:

```
t=0.25 → 3.00 s   position static at (0.1001, -0.2500, 0.8323)
settling drop     3.7 mm                (contact resolving)
deepest penetration  -0.088 mm
contacts             11 (resting on the table)
tactile              [0 0 0 0 0]
finite               yes
```

Residual velocity is ~2e-4 m/s and ~1e-2 rad/s, alternating between two values —
solver jitter, not motion: the position does not move by 0.1 mm over 2.75 s.
**Recorded rather than rounded to zero**, because E1b will measure slip in
millimetres and this is the noise floor it has to be read against.

An earlier placement put the pipette below the table surface; it was ejected and
fell to the floor (`z = 0.0073`). That run is kept in this note because it is
the reason placement is now solved from measured coordinates instead of chosen
by eye.

## Change 3 — the IK end-effector has to move (Phase 3, consequence)

Upstream sets arm 1's IK site to **the pipette tip**:

```python
self.site_name = 'tl/tip_site'      # UR5eArm, for the dexhand arm
```

That only works while the pipette is welded to the hand. With a free pipette the
IK target is no longer on the arm's kinematic chain, and IK on it is meaningless.
E1b retargets arm 1's IK to a site that is genuinely part of the hand and that
AutoBio already ships:

```
1/ur:dh:rh_precision   at world (0.672, -0.296, 1.312) in the home pose
```

This is a consequence of Change 2, not an independent choice, and it is the one
change that alters how the arm is *commanded* rather than what the scene
contains.

## Change 4 — gravity compensation is removed (Phase 5)

*Pending — not yet applied.* Upstream calls `set_gravcomp(body1)` and
`set_gravcomp(body2)` in `Pipette.prepare()`, which sets `gravcomp = 1`
recursively on both arms. An arm that never feels its own weight, or the weight
of what it holds, cannot be the subject of a grasp experiment. This will be
removed and the arm's numerical stability re-verified before any grasp is
scored.

---

## Reproduce

```bash
cd experiments/e1b/scene
MUJOCO_GL=osmesa ../../../.venv-autobio/bin/python -c "
import mujoco, os
mujoco.mj_loadPluginLibrary(os.path.abspath('../../../upstream/AutoBio/autobio/libmjlab.so.3.3.0'))
m = mujoco.MjModel.from_xml_path('e1b_grasp.xml')
print(m.nq, m.nv, m.nu, m.nsensor)"
# expects: 56 54 25 5
```
