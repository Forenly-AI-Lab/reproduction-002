"""E1a — harness / positioning sanity baseline.  NOT a grasp baseline.

Runs AutoBio's own scripted pipette expert, unmodified, and records what its own
check() reports.  The task is position-and-press: the pipette is rigidly attached
to the hand, so nothing here measures grasping.  See
results/2026-09-01-what-the-autobio-task-is.md.

The only thing added is polling: check() is a state machine that has to be
evaluated every step or its flags never latch.  Polling an existing predicate is
evaluation, not modification of the task.
"""
import argparse, json, os, sys, time
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("--episodes", type=int, default=3)
p.add_argument("--start-seed", type=int, default=0)
p.add_argument("--out", default="e1a-smoke.json")
a = p.parse_args()

import mujoco
mujoco.mj_loadPluginLibrary("./libmjlab.so.3.3.0")
sys.path.insert(0, os.getcwd())
from mani_pipette import Pipette, PipetteExpert

class Polled(PipetteExpert):
    """Same expert; check() polled each step so its flags can latch."""
    def step_and_log(self, info):
        super().step_and_log(info)
        if self._done:
            return
        if self.check():
            self._done = True
            self._t_success = float(self.data.time)

spec = Pipette.load()
rows = []
t_all = time.time()
for i in range(a.start_seed, a.start_seed + a.episodes):
    ex = Polled(spec)
    ex._done = False
    ex._t_success = None
    ex.reset(i)
    ex.set_serializer(log_root=os.path.join(os.getcwd(), "..", "..", "..", "results", "e1a-logs"))
    t0 = time.time()
    ex.execute()
    wall = time.time() - t0
    rows.append(dict(seed=i, success=bool(ex._done), t_success=ex._t_success,
                     sim_time=float(ex.data.time), wall_s=round(wall, 2),
                     below_liquid=bool(ex.below_liquid), liquid_drawn=bool(ex.liquid_drawn)))
    r = rows[-1]
    print(f"  seed {i:>3}  success={str(r['success']):<5} "
          f"below={str(r['below_liquid']):<5} drawn={str(r['liquid_drawn']):<5} "
          f"sim={r['sim_time']:>5.1f}s  wall={r['wall_s']:>6.1f}s", flush=True)

n = len(rows); k = sum(r["success"] for r in rows)
se = (k/n*(1-k/n)/n) ** 0.5 * 100 if n else 0
summary = dict(
    label="E1a — harness / positioning sanity baseline; NOT a grasp baseline",
    episodes=n, successes=k, success_rate_pct=round(k/n*100, 1),
    binomial_se_pct=round(se, 1),
    below_liquid_rate_pct=round(sum(r["below_liquid"] for r in rows)/n*100, 1),
    liquid_drawn_rate_pct=round(sum(r["liquid_drawn"] for r in rows)/n*100, 1),
    wall_total_s=round(time.time()-t_all, 1),
    wall_per_episode_s=round(np.mean([r["wall_s"] for r in rows]), 1),
    mujoco=mujoco.__version__, episodes_detail=rows,
)
print("\n" + json.dumps({k2: v for k2, v in summary.items() if k2 != "episodes_detail"}, indent=2))
out = os.path.join(os.getcwd(), "..", "..", "..", "results", a.out)
json.dump(summary, open(out, "w"), indent=2)
print("yazildi:", os.path.normpath(out))
