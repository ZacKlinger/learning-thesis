# Research web

Interactive force-directed graph of the resource bank. Nodes = thesis seeds, claim-evidence threads, verified sources, leads, raw files awaiting processing. Edges = anchors, supports, counters, frames, relates-to, tracked-in.

## Local preview

```sh
python3 -m http.server -d web 8000
# open http://localhost:8000
```

## How it gets regenerated

`bin/build-graph.py` walks `sources/`, `claim-evidence/`, `leads/`, `canon-map.md`, `thesis-seeds.md`, and `sources-raw/`, then writes `web/graph.json`. Run as part of the Saturday session's index-build step. The rendered page (`index.html`) fetches `graph.json` on load and lays out a Cytoscape.js force-directed graph.

## Deployment

`.github/workflows/deploy-pages.yml` deploys the `web/` directory to GitHub Pages on every push to `main`. The published URL is the repo's Pages URL (see Settings → Pages once enabled).

## Conventions

- **Layer colors** come from frontmatter `layer:` field. Add a new layer? Add a color in `LAYER_COLOR` in `index.html`.
- **Edge kinds** come from which section a source link appears under in a claim-evidence file (`### Supporting evidence` → supports; `### Counter-evidence` → counters; `### Cross-listed` → frames).
- The graph is a derived artifact: never edit `graph.json` by hand. Edit the underlying markdown and re-run the extractor.
