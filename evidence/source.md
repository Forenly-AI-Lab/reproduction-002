# Source and provenance

## The post

**@techniahqrobot | humanoid robots** — 2026-08-31 07:07:33 UTC
`https://x.com/techniahqrobot/status/2094321176235368906`
28 likes · 7 reposts · 1 reply at time of capture (2026-09-01)

Verbatim:

> TacForcing gives robots something most policies still struggle with the
> ability to adjust actions during contact.
>
> Instead of committing to a full motion from stale sensor data, the robot keeps
> updating its actions using fresh fingertip tactile feedback.
>
> In controlled real-robot tests, TacForcing reached 69% average success across
> bottle standing, liquid transfer and whiteboard wiping.
>
> Important context this is an August 26 arXiv preprint, not a real-world
> deployment, and the official project videos are shown at 5x speed.
>
> Vision tells a robot what it sees. Touch may become what tells it what is
> actually happening.
>
> Could tactile feedback become as important as vision for the next generation
> of robot policies?

Attached media: one 19.83 s H.264 clip, 960x720, 30 fps, 1.14 MB.

**The clip is not re-hosted in this repository.** It is other people's footage;
we link it rather than redistribute it. Watch it at the post above, or on the
study page, where it is embedded with credit:
<https://forenly.ai/lab-study/reproduction-002>. What this repository keeps are
the stills and contact sheets the analysis actually cites, in
`frames/` — quoted for commentary, credited to the original authors.

The post quote-tweets the same account's 2026-08-30 post about **Zetta (Tsunghua
AIR)**, a recovery layer added on top of frozen VLA policies (LIBERO-Pro 31% ->
92.5%, RoboCasa 93.6%, 2026-08-17 preprint, mostly simulation). That clip is
context, not the subject here, and likewise is not re-hosted.

## How it was captured

`x.com` returns HTTP 402 to unauthenticated fetches. Text and metadata were read
from the public mirrors `api.fxtwitter.com` and `api.vxtwitter.com`; both agree.
The video files were pulled directly from `video.twimg.com`, which serves them
without authentication. **No account credentials were used.**

## The primary source is missing

The post asserts "an August 26 arXiv preprint" and links nothing.

Searches run 2026-09-01, both negative:

1. `TacForcing tactile feedback robot manipulation arXiv 2026 fingertip action update`
   -> returns TacCoRL, Tac2Motion, Dream-Tac, TacForeSight, FlexiTac. No
   "TacForcing".
2. `tactile policy "bottle standing" "liquid transfer" whiteboard wiping dexterous hand arXiv August 2026`
   -> returns FTP-1, TactAlign, Current as Touch, Blind Dexterous Grasping,
   Contact-Grounded Policy. No single paper carrying that task triple.

Two negative searches are not proof of absence. The honest state is
**primary source not located**, and every number in the post is therefore
second-hand: 69%, the three tasks, and the 5x playback all rest on one
anonymous account's summary of a document nobody in this repository has read.

Anyone who finds the paper should add the link here and re-open the audit.
