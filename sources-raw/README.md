# sources-raw/

Drop primary-source files here (PDF, .txt, .html, .md). The autonomous agent reads them and produces verified `sources/AUTHOR-YEAR-shortname.md` notes with verbatim quotes.

## Why this directory exists

The agent's container blocks outbound HTTP to most primary-source hosts (Wikipedia, archive.org, papert.org, monoskop.org, university PDF mirrors, etc. all return `Host not in allowlist`). `WebFetch` is similarly restricted. github.com is reachable, so anything committed into the repo is reachable by the agent.

The contract is: **whatever you put here, the agent can read.**

## Workflow

1. You download a canonical work (PDF, EPUB you've converted to text, scraped HTML, transcript, etc.).
2. You commit it to `sources-raw/` with a clear filename. Suggested convention: `AUTHOR-YEAR-shortname.ext` — e.g. `Kirschner-Sweller-Clark-2006-minimal-guidance.pdf`, `Dewey-1897-pedagogic-creed.txt`, `Papert-1980-gears-of-my-childhood.html`.
3. On the next Saturday run, the agent inventories this directory, reads the new file, and produces a `sources/AUTHOR-YEAR-shortname.md` note with verbatim quotes pulled from the file. The `claim-evidence/` threads get seeded from those verified quotes.

## What to drop first

Top of the queue (see `queue.md`):

1. **Kirschner, Sweller & Clark (2006)** — "Why Minimal Guidance During Instruction Does Not Work," *Educational Psychologist*, 41(2), 75–86. Available open-access at e.g. `https://www.sfu.ca/~jcnesbit/EDUC220/ThinkPaper/KirschnerSweller2006.pdf`.
2. **Hmelo-Silver, Duncan & Chinn (2007)** — "Scaffolding and Achievement in Problem-Based and Inquiry Learning," the published rejoinder to KSC 2006. Must be read alongside.
3. **Dewey (1897)** — "My Pedagogic Creed." Public domain. Plain-text version recommended.
4. **Papert (1980)** — "The Gears of My Childhood," the foreword to *Mindstorms*. Plain text or HTML.

Anything you add beyond these is welcome — the canon-map proposal in `canon-map.md` is the full list.

## What the agent will NOT do

- **No fabrication.** If you drop a file the agent cannot parse (corrupted PDF, scanned-image-only PDF with no OCR layer, unsupported encoding), it will record that as a blocker rather than guess at content. Provide OCR'd or text-extracted versions where you can.
- **No paraphrase-as-evidence.** The protocol's non-negotiables mean verbatim quote + locator + access date for every claim that enters `claim-evidence/`. The locator for files in this directory is the filename plus a page/section reference.
- **No automatic deletion.** Files here stay until you remove them. The agent treats this directory as your input, not its workspace.

## Filename and provenance hygiene

The verified `sources/...md` note records, for each file: the original URL where you obtained it, the access date, and (for PDFs) page count + whether text is selectable. Don't rename files after the agent has cited them; if you have to, move + leave a placeholder so the cite chain doesn't break.

## .gitignore

This directory is **not** gitignored. Files here are committed and travel with the repo. Be mindful of file sizes for very long works — if you commit a 30 MB scanned PDF, the repo will carry it. For long books, prefer the relevant chapter as a separate file (e.g., `Illich-1971-deschooling-society-ch1.pdf`).
