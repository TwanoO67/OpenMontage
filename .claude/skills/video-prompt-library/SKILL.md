---
name: video-prompt-library
description: Search the community library of ~720 Claude Opus 5.5 video-creation prompts (LeaddeOpenLab/awesome-opus-5-5-video-prompts) — motion graphics, explainers, product launches, Remotion/HyperFrames/Manim/Three.js/Blender/canvas pieces — with tools, inputs, duration and the creator's original prompt. Use when looking for inspiration or a proven prompt pattern before a proposal or script, when the user asks "how did people make X with Opus", or wants a reference brief for a style (showreel, launch video, 3D explainer…).
metadata:
  tags: inspiration, prompts, reference, motion-graphics, remotion, hyperframes, manim, threejs
---

# video-prompt-library — Opus 5.5 video prompt reference

Source: <https://github.com/LeaddeOpenLab/awesome-opus-5-5-video-prompts> (web view with
video previews: <https://leaddeopenlab.github.io/awesome-opus-5-5-video-prompts/>).

Each case = one creator post: the **original prompt**, the **tools** the author used
(Remotion, HyperFrames, FFmpeg + Playwright, Three.js, Manim, Blender…), required
**inputs**, duration / aspect ratio, and a verification tier. It is a *reference* library —
not OpenMontage pipelines. Use it to borrow brief structure, pacing ideas and phrasing,
then produce through the normal pipeline (Rule Zero in `AGENT_GUIDE.md` still applies).

## Tool

`scripts/vpl.py` keeps a sparse, media-free clone (~26 MB, no GIFs/covers) in
`~/.cache/openmontage/awesome-opus-5-5-video-prompts` (override with `VPL_CACHE`).
First call clones automatically.

```bash
S=.agents/skills/video-prompt-library/scripts/vpl.py
python3 -I $S sync                                   # refresh (repo updates daily)
python3 -I $S categories                             # category -> case count
python3 -I $S search launch saas --full-prompt       # keywords (AND), ranked by likes
python3 -I $S search --category explainers --tool remotion --limit 10
python3 -I $S search --verified                      # only maintainer-reproduced cases
python3 -I $S show <id>                              # full prompt card (markdown)
```

Search matches title, use case, summary, prompt text and tool names (case-insensitive,
English). Categories: `motion-graphics`, `explainers`, `other-animation`,
`canvas-interactive`, `3d-scenes`, `games-interactive`, `remotion`, `manim`, `blender`,
`external-video-model`.

Raw data if you need more fields: `data/library/<id>.json` in the cache
(`analysis.caseEvidence` has `tools[].role`, `video.shots`, `result.evidence`,
`prompt.missing`…). `templates/` holds three runnable 15 s HTML→MP4 templates
(product-ui, feature-demo, product-launch).

## How to use it well

1. **Search narrowly, then read 2–3 cards** with `show`. Prefer `--full-prompt`
   (prompt disclosed in full) — partial/paraphrased prompts are weak references.
2. **Map the author's tools to OpenMontage**: Remotion → `remotion-composer/`;
   HyperFrames → `hyperframes` skills; "JavaScript + Playwright + FFmpeg" → HyperFrames
   or atelier mode; Three.js → `threejs-world-generation`; Manim → `manim-composer`.
3. **Extract patterns, not text**: duration budget, shot list shape, "go all out" style
   ambition cues, BPM-synced pacing, inputs the agent should ask for. Fold them into the
   brief / scene plan of the active pipeline.
4. **Say where an idea came from** when presenting concepts ("inspired by case
   `<id>` — @author's launch video structure").

## Caveats

- Almost all cases are tier `reference`: the author's claim, **not reproduced** by the
  maintainers (`verified` ≈ 15 cases). Treat results as plausible, not guaranteed.
- Third-party prompts and media belong to their authors (`data/docs/RIGHTS.md`). Use them
  as inspiration; don't republish prompts or previews verbatim in client deliverables.
- In atelier mode, this is inspiration for the *brief*, not a source of components —
  the distinctness review still applies.
