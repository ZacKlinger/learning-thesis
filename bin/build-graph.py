#!/usr/bin/env python3
"""Extract the implicit graph from the resource bank and emit web/graph.json.

Nodes: thesis seeds, claim-evidence threads, verified sources, leads,
       queued canon-map entries, raw primary-source files awaiting processing.
Edges: seed -> thread (anchors), thread -> source (supports / counters),
       source <-> source (canon-map "Relates to"), thread -> lead.

Run at the end of each session as part of the index-build step. Re-runs are
idempotent: same inputs produce the same JSON.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    return meta


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


# --- Thesis seeds -----------------------------------------------------------

SEED_TITLES = {
    "teacher-agency": "1. Teacher agency is being stripped",
    "ambition-over-complacency": "2. Ambition over complacency",
    "augmentation-not-efficiency": "3. Augmentation, not efficiency",
    "tech-cycles-in-education": "4. History rhymes — tech cycles",
}


# --- Thesis-seed framings (collapsed into their thread nodes; no separate seed node)

SEED_TITLES = {
    "teacher-agency": "Teacher agency",
    "ambition-over-complacency": "Ambition over complacency",
    "augmentation-not-efficiency": "Augmentation, not efficiency",
    "tech-cycles-in-education": "Tech cycles in education",
}


def extract_seed_framings() -> dict[str, str]:
    """Pull each strand's framing paragraph(s) from thesis-seeds.md, keyed by
    slug. Returns {slug: framing_text}. The framing is the body under
    `### N. <Title>` until the next heading. Used to attach the seed's
    conviction text directly to the thread node — one node per strand.
    """
    seeds = ROOT / "thesis-seeds.md"
    if not seeds.exists():
        return {}
    text = read(seeds)
    out: dict[str, str] = {}
    # The seed-section heading pattern in thesis-seeds.md is "### N. Title"
    # Map each title to a slug; capture the body until the next heading.
    title_to_slug = {
        "Teacher agency is being stripped": "teacher-agency",
        "Ambition over complacency": "ambition-over-complacency",
        "Augmentation, not efficiency": "augmentation-not-efficiency",
        "History rhymes": "tech-cycles-in-education",
    }
    pattern = re.compile(r"^###\s+\d+\.\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        heading_title = m.group(1).strip()
        slug = None
        for needle, s in title_to_slug.items():
            if heading_title.startswith(needle.split(" — ")[0]):
                slug = s
                break
        if slug is None:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        # Trim trailing "## " sections (e.g. "## What I don't yet know")
        next_h2 = re.search(r"^##\s", text[start:end], re.M)
        if next_h2:
            end = start + next_h2.start()
        body = text[start:end].strip()
        # Truncate for sanity
        if len(body) > 800:
            body = body[:800].rsplit(" ", 1)[0] + "…"
        out[slug] = body
    return out


# --- Threads (now the strand nodes; absorb seed framings) -------------------


def build_thread_nodes() -> list[dict]:
    framings = extract_seed_framings()
    nodes = []
    for f in sorted((ROOT / "claim-evidence").glob("*.md")):
        if f.name == "README.md":
            continue
        text = read(f)
        n_claims = sum(1 for line in text.splitlines() if line.startswith("## Claim"))
        slug = f.stem
        nodes.append(
            {
                "id": f"thread:{slug}",
                "label": SEED_TITLES.get(slug, slug.replace("-", " ")),
                "type": "thread",
                "layer": "thread",
                "claims": n_claims,
                "path": str(f.relative_to(ROOT)),
                "seed_framing": framings.get(slug, ""),
            }
        )
    return nodes


# --- Sources ----------------------------------------------------------------


_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)


def extract_section(text: str, heading: str, max_len: int = 600) -> str:
    """Return the first ~max_len chars of the named section (`## Heading`)."""
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    next_section = _SECTION_RE.search(text, start)
    end = next_section.start() if next_section else len(text)
    body = text[start:end].strip()
    if len(body) > max_len:
        body = body[:max_len].rsplit(" ", 1)[0] + "…"
    return body


def extract_quotes(text: str, max_n: int = 3) -> list[str]:
    """Pull the first N bullet items from `## Key quoted claims`."""
    pattern = re.compile(r"^##\s+Key quoted claims\s*$", re.M)
    m = pattern.search(text)
    if not m:
        return []
    start = m.end()
    next_section = _SECTION_RE.search(text, start)
    end = next_section.start() if next_section else len(text)
    body = text[start:end]
    quotes = []
    current: list[str] = []
    for line in body.splitlines():
        if line.startswith("- "):
            if current:
                quotes.append(" ".join(current).strip())
                current = []
                if len(quotes) >= max_n:
                    break
            current = [line[2:].strip()]
        elif line.strip().startswith("  ") and current:
            current.append(line.strip())
        elif not line.strip():
            continue
    if current and len(quotes) < max_n:
        quotes.append(" ".join(current).strip())
    return quotes[:max_n]


def build_source_nodes() -> tuple[list[dict], dict[str, str]]:
    nodes = []
    index: dict[str, str] = {}
    for f in sorted((ROOT / "sources").glob("*.md")):
        if f.name == "README.md":
            continue
        text = read(f)
        meta = parse_frontmatter(text)
        node_id = f"source:{f.stem}"
        raw_path = find_raw_for(f.stem)
        nodes.append(
            {
                "id": node_id,
                "label": meta.get("authors", f.stem).split(",")[0].split(";")[0] + " " + meta.get("year", ""),
                "title": meta.get("title", ""),
                "type": "source",
                "layer": meta.get("layer", "?"),
                "year": meta.get("year", ""),
                "read_status": meta.get("read_status", ""),
                "url": meta.get("url", ""),
                "access_date": meta.get("access_date", ""),
                "path": str(f.relative_to(ROOT)),
                "raw_path": raw_path,
                "thesis_excerpt": extract_section(text, "Thesis"),
                "quotes": extract_quotes(text),
                "threads": [],  # filled in after edges are built
            }
        )
        index[f.stem] = node_id
    return nodes, index


def find_raw_for(stem: str) -> str:
    """Return the relative path to sources-raw/<stem>.<ext> if it exists, else ""."""
    raw_dir = ROOT / "sources-raw"
    if not raw_dir.exists():
        return ""
    for f in raw_dir.iterdir():
        if f.is_file() and f.stem == stem:
            return str(f.relative_to(ROOT))
    return ""





# --- Leads ------------------------------------------------------------------


def build_lead_nodes() -> list[dict]:
    nodes = []
    for f in sorted((ROOT / "leads").glob("*.md")):
        if f.name == "README.md":
            continue
        nodes.append(
            {
                "id": f"lead:{f.stem}",
                "label": f.stem.replace("-leads", "").replace("-", " ") + " (leads)",
                "type": "lead",
                "layer": "lead",
                "path": str(f.relative_to(ROOT)),
            }
        )
    return nodes


# --- Raw files awaiting processing -----------------------------------------


def build_raw_nodes(source_index: dict[str, str]) -> list[dict]:
    raw_dir = ROOT / "sources-raw"
    if not raw_dir.exists():
        return []
    nodes = []
    for f in sorted(raw_dir.iterdir()):
        if not f.is_file() or f.name == "README.md":
            continue
        stem = f.stem
        if stem in source_index:
            continue  # already processed into a verified source
        nodes.append(
            {
                "id": f"raw:{stem}",
                "label": stem.replace("-", " ") + " (raw)",
                "type": "raw",
                "layer": "raw",
                "path": f"sources-raw/{f.name}",
            }
        )
    return nodes


# --- Edges ------------------------------------------------------------------
#
# Seed -> thread edges are no longer emitted. Seeds were collapsed into
# their thread nodes (see build_thread_nodes), so the "anchors" edge kind
# is retired. Keep the chart MECE: one node per strand.

# Match markdown links to source files: ](../sources/<stem>.md) or (sources/<stem>.md)
SOURCE_LINK_RE = re.compile(r"\]\(\.\.\/sources\/([^)]+)\.md\)")


def build_thread_source_edges(source_index: dict[str, str]) -> list[dict]:
    """Walk each claim-evidence file, classify each link as supports vs counters
    by which section heading it lives under."""
    edges: list[dict] = []
    for f in sorted((ROOT / "claim-evidence").glob("*.md")):
        if f.name == "README.md":
            continue
        thread_id = f"thread:{f.stem}"
        section = None
        for line in read(f).splitlines():
            stripped = line.strip().lower()
            if stripped.startswith("### supporting evidence"):
                section = "supports"
            elif stripped.startswith("### counter-evidence"):
                section = "counters"
            elif stripped.startswith("### cross-listed"):
                section = "frames"
            elif stripped.startswith("###"):
                section = None
            if section is None:
                continue
            for m in SOURCE_LINK_RE.finditer(line):
                stem = m.group(1)
                src_id = source_index.get(stem)
                if src_id:
                    edges.append({"source": thread_id, "target": src_id, "kind": section})
    return edges


# Match markdown links from claim-evidence threads to their leads file
LEAD_LINK_RE = re.compile(r"`leads/([^`]+)\.md`|\]\(\.\.\/leads\/([^)]+)\.md\)")


def build_thread_lead_edges() -> list[dict]:
    edges = []
    for f in sorted((ROOT / "claim-evidence").glob("*.md")):
        if f.name == "README.md":
            continue
        thread_id = f"thread:{f.stem}"
        for m in LEAD_LINK_RE.finditer(read(f)):
            stem = m.group(1) or m.group(2)
            if (ROOT / "leads" / f"{stem}.md").exists():
                edges.append(
                    {"source": thread_id, "target": f"lead:{stem}", "kind": "tracked-in"}
                )
    # Also: leads files share a name-prefix with their thread; add explicit edges.
    for f in sorted((ROOT / "leads").glob("*.md")):
        if f.name == "README.md":
            continue
        thread_stem = f.stem.replace("-leads", "")
        if (ROOT / "claim-evidence" / f"{thread_stem}.md").exists():
            edges.append(
                {
                    "source": f"thread:{thread_stem}",
                    "target": f"lead:{f.stem}",
                    "kind": "tracked-in",
                }
            )
    # De-duplicate
    seen = set()
    out = []
    for e in edges:
        k = (e["source"], e["target"], e["kind"])
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


# Source <-> source from canon-map "Relates to:"
CANON_HEADING_RE = re.compile(r"^### \[([^\]]+)\] (.+)$")


def build_source_source_edges(source_index: dict[str, str]) -> list[dict]:
    """Extract Relates-to links from canon-map.md. Only emits edges between
    sources that have verified source notes (so we don't connect to phantom
    queued entries here; queued ones become their own node type later)."""
    canon = ROOT / "canon-map.md"
    if not canon.exists():
        return []
    edges = []
    # Build a name -> source_id index from author-year stems
    label_to_id: dict[str, str] = {}
    for stem in source_index:
        # stem like "Kirschner-Sweller-Clark-2006-minimal-guidance" -> match on
        # "Kirschner-Sweller-Clark-2006" or "Kirschner, Sweller & Clark 2006"
        parts = stem.split("-")
        # find year
        year_idx = next((i for i, p in enumerate(parts) if p.isdigit() and len(p) == 4), -1)
        if year_idx == -1:
            continue
        authors = parts[:year_idx]
        year = parts[year_idx]
        label_to_id[f"{' '.join(authors)} {year}"] = source_index[stem]
        label_to_id[f"{', '.join(authors)} ({year})"] = source_index[stem]
        # also a short form: last-author year
        label_to_id[f"{authors[-1]} {year}"] = source_index[stem]
        label_to_id[f"{authors[-1]} ({year})"] = source_index[stem]

    current_source_id: str | None = None
    for line in read(canon).splitlines():
        m = CANON_HEADING_RE.match(line)
        if m:
            heading = m.group(1) + " " + (m.group(2) or "")
            # Try to match heading to a known source
            current_source_id = None
            for label, sid in label_to_id.items():
                if label in heading:
                    current_source_id = sid
                    break
            continue
        if current_source_id and line.strip().lower().startswith("- relates to:"):
            tail = line.split(":", 1)[1]
            for label, sid in label_to_id.items():
                if label in tail and sid != current_source_id:
                    edges.append(
                        {"source": current_source_id, "target": sid, "kind": "relates-to"}
                    )
    # De-duplicate (treat as undirected)
    seen = set()
    out = []
    for e in edges:
        k = tuple(sorted([e["source"], e["target"]])) + (e["kind"],)
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


# --- Main -------------------------------------------------------------------


def main() -> None:
    WEB.mkdir(exist_ok=True)

    thread_nodes = build_thread_nodes()
    source_nodes, source_index = build_source_nodes()
    lead_nodes = build_lead_nodes()
    raw_nodes = build_raw_nodes(source_index)

    edges = (
        build_thread_source_edges(source_index)
        + build_thread_lead_edges()
        + build_source_source_edges(source_index)
    )

    # Fill source nodes' `threads` back-references from thread->source edges.
    source_threads: dict[str, set[str]] = {}
    for e in edges:
        if e["source"].startswith("thread:") and e["target"].startswith("source:"):
            slug = e["source"][len("thread:"):]
            source_threads.setdefault(e["target"], set()).add(slug)
    for n in source_nodes:
        n["threads"] = sorted(source_threads.get(n["id"], set()))

    graph = {
        "nodes": thread_nodes + source_nodes + lead_nodes + raw_nodes,
        "edges": edges,
        "generated_at": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip(),
    }

    out = WEB / "graph.json"
    out.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {out}: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges"
    )


if __name__ == "__main__":
    main()
