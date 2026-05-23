# Research queue

Prioritized list of next work. The Saturday routine works from the top.

**Status (2026-05-23):** Refreshed after the second Saturday run. Five
verified `sources/` notes now exist; four `claim-evidence/` threads have
their first verbatim quotes. The next moves are driven by two pressures:
(a) the Hmelo-Silver rejoinder must enter before the KSC-anchored
counter-evidence in `augmentation-not-efficiency.md` is allowed to do
heavy work, and (b) the tech-cycles thread has one data point (Jordan
2014) and needs Cuban or Watters to become a documented pattern.

## Next up

1. **Read Hmelo-Silver, Duncan & Chinn (2007) — top priority.** Protocol
   requires reading alongside, not after, Kirschner/Sweller/Clark (2006).
   The KSC entries in `claim-evidence/augmentation-not-efficiency.md`
   are flagged provisional pending HSDC. The new wishlist URL points at
   an AFT mirror; if that also fails next week, demote and ask Zack to
   obtain the PDF directly (the paper is well-cited and a copy almost
   certainly exists in his network).

2. **Read Illich (1971), Chapters 2–7.** The file is in `sources-raw/`
   and parsing works. Chapter 1 was read this Saturday. The remaining
   chapters — Phenomenology of School; Ritualization of Progress;
   Institutional Spectrum; Irrational Consistencies; Learning Webs;
   Rebirth of Epimethean Man — sharpen the "AI-could-be-the-learning-web
   Illich-imagined" tension that surfaced this week. Particular interest
   in *Learning Webs* (Ch. 6) for the AI-routing-around-the-institution
   reading.

3. **Read Skinner (1958) "Teaching Machines" — second-priority for the
   tech-cycles thread.** Retried with a Wayback Machine mirror. A primary
   document of the personalized-learning lineage; the structural
   similarity to current AI-tutoring rhetoric is exactly the point. If
   delivered next week, pair the reading with the existing Jordan 2014
   entries in `claim-evidence/tech-cycles-in-education.md`.

4. **Audit pass on this session's claims.** Per protocol, sample 2–3
   claims from the entries written this week and re-verify the quote +
   URL + locator. This is the discipline that keeps the ledger from
   rotting. Treat as a non-negotiable next Saturday.

5. **Read Pea & Kurland (1984), "On the Cognitive Effects of Learning
   Computer Programming," if a URL can be located.** The canonical
   critique of early Logo enthusiasm. The Papert claims in
   `claim-evidence/augmentation-not-efficiency.md` need this complication
   before they can do heavy lifting in the thesis. Add to wishlist this
   week.

6. **Read Mehta & Fine (2019) excerpt if a chapter PDF can be located.**
   Their finding — that deeper learning is rare even in schools that
   explicitly aim for it, and tends to happen in electives and clubs
   rather than core classes — is exactly the kind of empirically
   grounded complication the `ambition-over-complacency` thread is
   asymmetric without. The book is paywalled; an open chapter or
   author preprint is worth searching for before defaulting to leads.

## Standing items (every Saturday)

- **Audit pass: re-verify 2–3 random existing claims** in
  `claim-evidence/`. *Now active — first claims exist as of this session.*
- **Tension scan:** surface the most interesting complication from this
  week's reading.
- **Thesis-fit check:** quote a current line from `thesis-seeds.md` and
  ask whether the week's reading still supports it.
- **Wishlist maintenance:** when reading reveals a needed source,
  append a line to `sources-wishlist.txt`. Demote persistently-failing
  URLs to `leads/` and replace with a working mirror.
- **Source-fetch failure triage:** inspect new files in `sources-raw/`
  for the landing-page-masquerading-as-PDF problem. Delete corrupted
  files; demote in `leads/` with a note on what mirror would work.

## Backlog

- Cuban (1986) *Teachers and Machines* and Watters (2021) *Teaching
  Machines* — both paywalled; Zack to obtain or the agent records as
  leads only. Both are load-bearing for the tech-cycles thread; the
  thread cannot move from "one data point (MOOCs)" to "documented
  pattern" without one of these.
- Postman (1992) *Technopoly* — same access situation. The media-ecology
  critique line cannot fully proceed without this.
- Sizer (1984), Mehta & Fine (2019) once the practitioner layer comes up.
- Locate and assess the Bloom 2-sigma replication record (VanLehn 2011
  on intelligent tutoring is the contemporary update).
- Founding documents of the American high school's shape: Committee of
  Ten (1893), Cardinal Principles (1918), Conant (1959).
- Hirsch (1987) and the Core Knowledge sequence — the strongest
  content-first counter to the "ambition" framing. The
  `ambition-over-complacency` thread is asymmetric without this.
- Lemov (2010) — the strongest practitioner counter to the "agency"
  framing. The `teacher-agency` thread is asymmetric without this.
- Cristia et al. (2017) OLPC Peru RCT — demoted from wishlist this week
  because the AEA URL returned a landing page. Try NBER WP 18610 mirror.
- Reiser (2001) — demoted from wishlist this week because the Springer
  URL returned a landing page. Need a working mirror.
- Pappano (2012) NYT MOOC piece — paywalled. Either Zack supplies it or
  the thread cites it second-hand through Jordan 2014, p. 134.

## Backlog (deferred until canon is read)

- Synthesis essay 1: what does "previously impossible learning" mean,
  operationally? Draft only after enough primary sources are read to
  defend a definition.
- Synthesis essay 2: which empirical wins in edtech are efficiency wins,
  which are augmentation wins, and is the distinction stable on
  inspection?
- Synthesis essay 3 (tech-cycles thread): what would have to be true
  for the AI wave to break the historical pattern? Draft only after
  Cuban, Watters, and one wave-primary document (Skinner) are read.

## Workflow-level item for Zack

- The current `fetch-sources` workflow uses `curl --fail`, which does
  not catch the case where a publisher URL returns an HTTP 200 HTML
  landing page instead of the requested PDF. Consider adding a
  content-type check or a `file --mime-type` probe after the fetch
  so that bad fetches are recorded as failures rather than committed
  as garbage. The agent can write the patch; installing it requires
  the `workflow` scope on the PAT.
