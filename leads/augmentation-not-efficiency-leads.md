# Leads — augmentation, not efficiency

Unverified material relevant to the augmentation/efficiency thread. Nothing here has been read by the agent. Promotion to `claim-evidence/` requires a verbatim quote + URL + access date.

## Primary sources to read

- **Papert, Seymour (1980). *Mindstorms: Children, Computers, and Powerful Ideas*.** The foundational positive vision. PDF widely circulated; agent could not access the host in this run. The foreword "The Gears of My Childhood" is the most-quoted passage and the starting point.
- **Papert, Seymour (1993). *The Children's Machine: Rethinking School in the Age of the Computer*.** Papert's diagnosis of why schools absorb technology without changing. Direct ancestor of the augmentation/efficiency framing.
- **Kirschner, Paul A., Sweller, John & Clark, Richard E. (2006). "Why Minimal Guidance During Instruction Does Not Work."** *Educational Psychologist*, 41(2), 75–86. Mandatory steelman.
- **Hmelo-Silver, Cindy E., Duncan, Ravit G. & Chinn, Clark A. (2007). "Scaffolding and Achievement in Problem-Based and Inquiry Learning: A Response to Kirschner, Sweller, and Clark (2006)."** Must be read alongside KSC 2006.
- **Sweller, John (1988). "Cognitive Load During Problem Solving: Effects on Learning."** *Cognitive Science*, 12(2). Mechanism paper underlying KSC.
- **Scardamalia, Marlene & Bereiter, Carl. Knowledge Building writings.** Probably the most rigorous research program on a kind of learning that the technology (CSILE / Knowledge Forum) actually made possible. Specific candidate to test the "augmentation" claim with evidence.
- **Pea, Roy D. & Kurland, D. Midian (1984). "On the Cognitive Effects of Learning Computer Programming."** Influential critique of early Logo claims — the cautionary tale every Papert-influenced thesis needs to absorb.
- **Bloom, Benjamin S. (1984). "The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring."** *Educational Researcher*, 13(6). The empirical hook for tech-tutoring efficiency claims.

## Empirical work to locate

- Replications and meta-analyses of the Bloom 2-sigma claim — how robust is it? Recent reviews (VanLehn 2011 on tutoring systems) put the effect closer to 0.4 sigma than 2.
- Outcomes studies of intelligent tutoring systems (Cognitive Tutor, ASSISTments, Carnegie Learning) — these are the empirical body that AI-tutoring claims rest on, but the effect sizes are modest, not transformative.
- Studies attempting to operationalize "deeper" or "transferable" learning gains attributable to tools — see the Deeper Learning Network evaluations from American Institutes for Research (~2014).

## Supporting-sprint URLs that failed in the 2026-06-05 fetcher (demoted 2026-06-06)

The five wishlist URLs added on 2026-05-30 per the steer's supporting
sprint all failed to deliver to `sources-raw/` over the 2026-05-30 push,
the 2026-06-05 Friday safety-net run, and any intermediate retries. The
GitHub Actions run for 2026-06-05 reports "fetch success" (the workflow
itself did not crash) but no new files in `sources-raw/` and no follow-on
"fetch-sources: add N file(s)" bot commit. Each URL is recorded below with
the most-plausible alternate to try next; the wishlist is being updated in
the same commit as this demotion.

- **Scardamalia & Bereiter 1994 — CSILE.** Tried:
  `https://ikit.org/fulltext/1994_CSILE.pdf` — failed. The
  `ikit.org/fulltext/` directory layout is the agent's best guess and may
  not be correct, or the specific paper may be hosted elsewhere on the
  IKIT site. Alternate to try: a direct Google Scholar-derived PDF (the
  Carl Bereiter / OISE pages at `tinker.ed.uiuc.edu` historically hosted
  the *Journal of the Learning Sciences* (1994) paper). Adding
  `https://www.scribd.com/document/...` would be unreliable; better to
  ask Zack to supply the PDF if no open mirror surfaces. Until then,
  this remains the load-bearing missing source for the augmentation
  thread.
- **VanLehn 2011 — relative effectiveness of tutoring.** Tried:
  `https://www.sfu.ca/~jcnesbit/EDUC220/ThinkPaper/VanLehn2011.pdf` —
  failed. The Nesbit course directory hosted KSC and HSDC but not
  VanLehn. The most-likely alternate is the LearnLab/Pittsburgh PSLC
  site, where Kurt VanLehn's collaborators published. URL to try:
  `https://pact.cs.cmu.edu/koedinger/pubs/VanLehn2011.pdf` or the
  *Educational Psychologist* DOI mirror via Taylor & Francis (which is
  paywalled). If both fail, ask Zack to supply.
- **Zeiser et al. 2014 — Deeper Learning Outcomes (AIR).** Tried:
  `https://www.air.org/sites/default/files/downloads/report/Report_3_Evidence_of_Deeper_Learning_Outcomes.pdf` — failed. The AIR site
  reorganized its publications URL scheme around 2020; the historical
  `/sites/default/files/downloads/` path is no longer canonical. The
  current scheme is `/sites/default/files/2021-09/...` etc. Alternate:
  search `air.org` directly for "Evidence of Deeper Learning Outcomes"
  and grab the current canonical URL — likely
  `https://www.air.org/sites/default/files/Report3-Evidence-of-Deeper-Learning-Outcomes.pdf` or similar. Add to wishlist next Saturday.

## Tensions to chase

- The strongest empirical case for educational technology is *efficiency* (mastery learning, retrieval practice apps, adaptive drill). The strongest *aspirational* case is augmentation (Knowledge Building, Logo, simulation-based science). The thesis seed treats these as opposed; they may simply be different problems.
- "Previously impossible learning" needs an operational definition. Without one, the thread will drift into rhetoric. Candidate definitions:
  - Knowledge artifacts created by students that require the tool (simulations, working programs, public-facing texts).
  - Forms of collaboration only possible at digital distance.
  - Feedback loops too fast for human-only instruction.
  - Access to phenomena (microscopy, telescopy, large datasets) previously confined to specialists.
- Even if augmentation is real, *who gets access to it* may matter more than whether it exists. Equity-of-access objections to "ambitious learning" cases need a serious answer.
