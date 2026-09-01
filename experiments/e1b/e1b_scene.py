"""E1b scene loader — free pipette, fingertip touch sensors, no gravity compensation.

Loads the forked scene directly.  Deliberately does NOT go through
Pipette.prepare(), because that is where upstream welds the pipette to the hand
and switches gravity compensation on.  Every difference from upstream is listed
in MODIFICATIONS.md.
"""
import os, numpy as np, mujoco

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, "scene", "e1b_grasp.xml")
PLUGIN = os.path.abspath(os.path.join(HERE, "..", "..", "upstream", "AutoBio", "autobio", "libmjlab.so.3.3.0"))

TOUCH = [f"1/ur:dh:touch_rh_{f}distal" for f in ("th", "ff", "mf", "rf", "lf")]
TIPS  = [f"1/ur:dh:rh_{f}distal" for f in ("th", "ff", "mf", "rf", "lf")]

_loaded = False
def _plugin():
    global _loaded
    if not _loaded:
        mujoco.mj_loadPluginLibrary(PLUGIN); _loaded = True

def _set_gravcomp(body):
    """Upstream's own helper, verbatim -- operates on an MjsBody, i.e. the SPEC."""
    body.gravcomp = 1
    for child in body.bodies:
        _set_gravcomp(child)

def load(gravcomp: bool = False):
    """Returns (model, data).  gravcomp=False is E1b; True reproduces upstream's assist.

    Gravity compensation MUST be set on the spec before compile.  Assigning
    model.body_gravcomp after compile is a SILENT NO-OP: the field reads back the
    value you wrote, and the simulation ignores it.  Measured, not assumed --
    under 10x gravity the arm sags 922.88 mm with runtime assignment, exactly as
    it does with gravcomp off, and 0.00 mm when it is set on the spec.
    """
    _plugin()
    spec = mujoco.MjSpec.from_file(SCENE)
    if gravcomp:
        _set_gravcomp(spec.body("1/ur5e:"))
        _set_gravcomp(spec.body("2/ur5e:"))
    m = spec.compile()
    d = mujoco.MjData(m)
    if m.nkey:
        mujoco.mj_resetDataKeyframe(m, d, 0)
    mujoco.mj_forward(m, d)
    return m, d

def settle(m, d, seconds=1.0):
    t0 = d.time
    while d.time - t0 < seconds:
        mujoco.mj_step(m, d)
    return d

def ids(m):
    g = lambda k, n: mujoco.mj_name2id(m, k, n)
    return dict(
        pipette_body = g(mujoco.mjtObj.mjOBJ_BODY, "tl/pipette"),
        pipette_jnt  = g(mujoco.mjtObj.mjOBJ_JOINT, "e1b_pipette_free"),
        tip_site     = g(mujoco.mjtObj.mjOBJ_SITE, "tl/tip_site"),
        ik_site      = g(mujoco.mjtObj.mjOBJ_SITE, "1/ur:dh:rh_precision"),
        hand_base    = g(mujoco.mjtObj.mjOBJ_BODY, "1/ur:dh:rh_base"),
        tube_body    = g(mujoco.mjtObj.mjOBJ_BODY, "5/centrifuge_50ml_screw_body"),
        touch        = [g(mujoco.mjtObj.mjOBJ_SENSOR, n) for n in TOUCH],
        tips         = [g(mujoco.mjtObj.mjOBJ_BODY, n) for n in TIPS],
    )
