# bootstrap/

One-time setup actions that require a token scope the autonomous agent doesn't have.

## fetch-sources.workflow.yml — install the source-fetcher workflow

The autonomous agent's GitHub PAT lacks `workflow` scope, so it cannot create files under `.github/workflows/`. GitHub rejects the push with:

> refusing to allow a Personal Access Token to create or update workflow `.github/workflows/fetch-sources.yml` without `workflow` scope

The workflow file itself is correct; it just needs to be installed from a token that has the scope. **You** do — your normal local git push will work.

### One-time install (do this once, never again)

From a fresh checkout on your machine:

```bash
git pull
mkdir -p .github/workflows
git mv bootstrap/fetch-sources.workflow.yml .github/workflows/fetch-sources.yml
git commit -m "Install fetch-sources workflow"
git push
```

That's it. After this single push:

- Any push that changes `sources-wishlist.txt` triggers the workflow.
- The workflow downloads each listed URL on github.com infrastructure (which can reach the hosts the agent's container can't) and commits the bytes into `sources-raw/`.
- The agent reads from `sources-raw/` in its next Saturday run.

The initial wishlist already contains the 5 priority sources (KSC 2006, HSDC 2007, Dewey 1897, Papert 1980, Illich 1971). After installing the workflow, the first push that touches the wishlist — or a manual trigger from the Actions tab — will fetch them.

### Alternative: update the agent's PAT

If you'd rather not do the one-time install and want the agent to manage workflow files itself going forward, regenerate the PAT used for autonomous runs with `workflow` scope added (classic token) or with `Workflows: read and write` (fine-grained token). Then the agent can install and update workflows on its own.
