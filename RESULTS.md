# RESULTS — The Wednesday Globe (news-image-20261125)

## Entry

- Competition: news-image-20261125 — "Sum up 25 November's world news
  in one image" (pot $100, top 50 paid; deadline Fri 27 Nov 2026 07:00 WIB).
- Image: `entry.png`, 1024×1024 RGB, 202,446 bytes,
  sha256 `a68b8c6d0fe650bc10fe6d5d8b591c99a5f31f2465689db8c9e78eec0c0e15c9`.
- Deterministic: `python3 render.py` run twice gives the same sha256;
  `main.ts` run twice copies the same bytes.
- 35 verified Wednesday 25 Nov 2026 stories, 9 regions, 14 fields,
  4 illustrated leads, 10 illustrated secondaries, UTC timeline (5 beats),
  dotted world map with 15 numbered pins, DATE CHECK box, per-story
  verification badges (CONFIRMED / OFFICIAL / REPORTED / CLAIM).

## Commits

- `82450d9` — claim file + MIT license (first commit).
- `2edf80a` — the entry (README, RESEARCH, entry.png, main.ts,
  package.json, render.py).
- This file is the third commit (build report).

## Kit check (no transcripts)

`node cli/makefun.mjs check --repo <repo> --commit 2edf80a`
(run from the unpacked kit; `--commit` and `--worktree` cannot be
combined, so the commit form was used on the clean tree):

- **4 passed**: competition_open, snapshot (8 files, 250,396 bytes),
  license_osi (MIT), entrypoint (main.ts, node22).
- **1 failed**: transcripts_present — expected; no transcripts were
  given. The bundle (built by the parent agent from the builder +
  reviser sessions) fixes this.
- **14 skipped** (all transcript checks), **5 checked at submission**
  (repo_public, repo_owner, repo_created_after_open, commit_in_repo,
  duplicate_snapshot) — these pass once Danu creates the public repo
  `DanuMahiru/news-image-20261125` on his phone and the work is pushed.

## Still to do (parent agent, after Danu creates the repo)

1. Danu creates public repo `DanuMahiru/news-image-20261125` on his phone
   (github.com/new → name → Public → no README/gitignore/license).
2. Push, set GitHub About (homepage = bounty URL, topic `makefun`),
   bundle transcripts (builder session + a reviser session, parent
   session as parent-only, prompt file = `prompt.txt` with
   "Ya, ikut news-25"), kit check WITH the bundle, then submit
   before Fri 27 Nov 07:00 WIB.
