"""Stage 0 — archive what the robot actually looks like, with the numbers beside it."""
import json, os, numpy as np, mujoco, e1b_scene as S

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
m, d = S.load(gravcomp=False)
I = S.ids(m)
S.settle(m, d, 1.0)

r = mujoco.Renderer(m, height=720, width=960)
for cam in ("e1b_grasp_cam", "e1b_close_cam", "table_cam_front"):
    r.update_scene(d, camera=cam)
    img = r.render()
    import imageio.v3 as iio
    iio.imwrite(os.path.join(OUT, f"stage0_{cam}.png"), img)
    print("  yazildi:", f"stage0_{cam}.png")

pb, pj = I["pipette_body"], I["pipette_jnt"]
dadr = m.jnt_dofadr[pj]
metrics = dict(
    stage=0, name="initial scene", gravcomp=False,
    model=dict(nq=int(m.nq), nv=int(m.nv), nu=int(m.nu), nsensor=int(m.nsensor),
               nbody=int(m.nbody), timestep=float(m.opt.timestep)),
    pipette=dict(mass_g=round(float(m.body_mass[pb])*1000, 2),
                 pos=[round(float(x),5) for x in d.xpos[pb]],
                 quat=[round(float(x),5) for x in d.xquat[pb]],
                 lin_vel=[round(float(x),6) for x in d.qvel[dadr:dadr+3]],
                 ang_vel=[round(float(x),6) for x in d.qvel[dadr+3:dadr+6]],
                 is_free=bool(m.jnt_type[pj] == mujoco.mjtJoint.mjJNT_FREE)),
    contacts=dict(total=int(d.ncon),
                  deepest_penetration_mm=round(float(min([d.contact.dist[i] for i in range(d.ncon)], default=0.0))*1000, 4)),
    tactile={n: round(float(d.sensordata[i]), 6) for n, i in zip(S.TOUCH, [m.sensor_adr[j] for j in I["touch"]])},
    sites=dict(ik_site=[round(float(x),5) for x in d.site_xpos[I["ik_site"]]],
               pipette_tip=[round(float(x),5) for x in d.site_xpos[I["tip_site"]]]),
    finite=bool(np.isfinite(d.qpos).all() and np.isfinite(d.qvel).all()),
)
json.dump(metrics, open(os.path.join(OUT, "stage0_metrics.json"), "w"), indent=2)
print(json.dumps(metrics, indent=2))
