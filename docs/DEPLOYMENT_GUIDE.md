# Deployment Guide

This document is the canonical checklist for releasing mycontext-ai.  
Run through every section in order before publishing to PyPI or pushing a tagged release to GitHub.  
Nothing here should be skipped — each item exists because something broke without it.

---

## 1. Pre-Flight: Code Quality

### 1.1 Lint

```bash
ruff check src/
```

Fix all errors. Warnings may be accepted if documented. The `ruff` config in `pyproject.toml` governs the ruleset — do not bypass with `# noqa` without a comment explaining why.

### 1.2 Type Check

```bash
mypy src/mycontext
```

Strict mode is enabled. All new public functions must be fully typed. Failures here block the release.

### 1.3 Format

```bash
black src/ tests/
```

Commit the result if files changed.

---

## 2. Pre-Flight: Tests

### 2.1 Full unit test suite

```bash
python -m pytest tests/unit/ -v
```

All tests must pass. Zero failures, zero errors. Warnings are acceptable.

### 2.2 Enterprise gating tests (critical)

```bash
python -m pytest tests/unit/test_enterprise_gating.py -v
```

This test suite verifies that enterprise patterns are not accessible without a license key. **This must pass before every PyPI release.** A failure here means enterprise code may be exposed in the free tier.

### 2.3 Coverage check

```bash
python -m pytest tests/unit/ --cov=src/mycontext --cov-report=term-missing
```

There is no hard minimum threshold, but any new public function added to the release must have at least one unit test. Cover the happy path, at least one error path, and the top-level import.

### 2.4 Confirm enterprise templates excluded from build

The `pyproject.toml` build config explicitly excludes enterprise templates from the wheel and sdist:

```toml
[tool.hatch.build.targets.wheel]
exclude = ["src/mycontext/templates/enterprise"]

[tool.hatch.build.targets.sdist]
exclude = ["src/mycontext/templates/enterprise"]
```

**Verify this is still in place before every build.** If it is ever accidentally removed, enterprise code ships in the free package.

Quick check:

```bash
python -c "
import build, zipfile, pathlib
# Build a wheel and check its contents
"
```

Or after building:

```bash
python -m build --wheel
# Then inspect the wheel:
python -c "
import zipfile, sys
whl = sorted(pathlib.Path('dist').glob('*.whl'))[-1]
names = zipfile.ZipFile(whl).namelist()
enterprise = [n for n in names if 'enterprise' in n]
if enterprise:
    print('FAIL — enterprise files found in wheel:')
    for n in enterprise: print(' ', n)
    sys.exit(1)
else:
    print('OK — no enterprise files in wheel')
"
```

---

## 3. Version Bump

Version is set in **two places** — both must match:

| File | Key |
|------|-----|
| `pyproject.toml` | `version = "X.Y.Z"` |
| `src/mycontext/__init__.py` | `__version__ = "X.Y.Z"` |

Versioning follows **Semantic Versioning**:

| Change type | Version bump | Example |
|-------------|-------------|---------|
| New public API, new feature | Minor | `0.4.0` → `0.4.1` (patch if backward-compat) |
| Breaking change | Major | `0.4.x` → `0.5.0` |
| Bug fix, docs, tests only | Patch | `0.4.0` → `0.4.1` |

Confirm both files are in sync:

```bash
python -c "import mycontext; print(mycontext.__version__)"
python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['version'])"
```

Both lines must print the same version string.

---

## 4. CHANGELOG

Update `CHANGELOG.md` before releasing:

- Add a new `## [X.Y.Z] — YYYY-MM-DD` section at the top.
- Use the standard categories: Added, Changed, Deprecated, Removed, Fixed, Security, Documentation.
- Every new public function, field, or class that ships in the release must appear under **Added**.
- Every breaking change must appear under **Changed** with a migration note.
- Do not describe internal refactors unless they change observable behaviour.

---

## 5. README

The README is the PyPI landing page. Check:

- The Quick Start section compiles and runs (test it manually if anything changed).
- New capabilities from this release are reflected in the "Core Strengths" numbered list.
- The "At a Glance" comparison table includes new rows for new capabilities.
- All section numbers in the "Core Strengths" list are sequential (no gaps from additions/removals).
- The badge URLs are still valid (Python version, PyPI version).

---

## 6. Documentation Site

The Docusaurus site at `website/` must build cleanly before the release goes out.

```bash
cd website
npm run build
```

Zero errors, zero broken links in the build output. Warnings about untracked files (git) are acceptable.

Check that:

- Any new page is added to `sidebars.ts`.
- Any new API surface is reflected in `docs/api/overview.md`.
- Any new foundation field is documented in the relevant `docs/foundations/*.md` page.
- Page titles in frontmatter (`title:`) match the sidebar entry.

---

## 7. Build the Package

```bash
# Install build tools if not already present
pip install build twine

# Clean previous builds
rm -rf dist/ build/

# Build wheel and sdist
python -m build
```

This produces:
- `dist/mycontext_ai-X.Y.Z-py3-none-any.whl`
- `dist/mycontext_ai-X.Y.Z.tar.gz`

Inspect the wheel to confirm enterprise exclusion (see Section 2.4).

---

## 8. PyPI Upload

### 8.1 Test PyPI first (recommended for minor/major bumps)

```bash
twine upload --repository testpypi dist/*
```

Install from Test PyPI and smoke-test:

```bash
pip install --index-url https://test.pypi.org/simple/ mycontext-ai==X.Y.Z
python -c "
import mycontext
print(mycontext.__version__)
from mycontext import Context, Guidance, Directive, generate_context
ctx = Context('test role')
print('Core import OK')
"
```

### 8.2 Production PyPI

```bash
twine upload dist/*
```

You will be prompted for your PyPI API token. Store it in a password manager — do not commit it anywhere.

After upload, verify the release page at `https://pypi.org/project/mycontext-ai/`.

### 8.3 Smoke-test from PyPI

```bash
pip install mycontext-ai==X.Y.Z
python -c "
import mycontext
print(mycontext.__version__)

# Core
from mycontext import Context, Guidance, Directive, Constraints
ctx = Context(
    guidance=Guidance(role='Test analyst', goal='Verify install'),
    directive=Directive('Test task'),
    research_flow=True,
)
assembled = ctx.assemble()
assert '## ROLE' in assembled, 'research_flow assembly broken'
print('Context OK')

# generate_context (import only, no LLM call)
from mycontext.intelligence import generate_context, GeneratedContext
print('generate_context import OK')

# Enterprise gating
from mycontext.templates.free.reasoning import RootCauseAnalyzer
ctx2 = RootCauseAnalyzer().build_context(problem='test problem')
print('Free patterns OK')

try:
    from mycontext.templates.enterprise.decision import DecisionFramework
    print('WARN: enterprise imported without license — check exclusion')
except (ImportError, ModuleNotFoundError):
    print('Enterprise gating OK')
"
```

All lines should print "OK". Any exception or unexpected output blocks the release.

---

## 9. GitHub Release

### 9.1 Commit and tag

```bash
git add -A
git commit -m "release: v0.4.1"
git tag v0.4.1
git push origin main
git push origin v0.4.1
```

### 9.2 GitHub Release page

Go to: `https://github.com/SadhiraAI/mycontext/releases/new`

- **Tag:** select the tag you just pushed (`v0.4.1`)
- **Title:** `v0.4.1 — <one-line summary of the most important change>`
- **Body:** paste the relevant section from `CHANGELOG.md`
- **Attach:** attach the `dist/*.whl` and `dist/*.tar.gz` files from the build

### 9.3 Confirm CI passes

The `docs.yml` GitHub Actions workflow deploys the documentation site on push to `main`. Verify it completes without errors in the Actions tab before announcing the release.

---

## 10. Post-Release

- [ ] Verify `https://pypi.org/project/mycontext-ai/` shows the new version
- [ ] Verify the GitHub release page is live with the correct changelog
- [ ] Verify the Docusaurus docs site at `https://docs.mycontext.sadhiraai.com` reflects the new content (allow ~5 minutes for Cloudflare Pages CDN)
- [ ] Update the web UI at `mycontext.sadhiraai.com` if the "Docs" link or any displayed version number needs updating

---

## Quick Reference: Full Release Checklist

```
[ ] ruff check src/             — lint clean
[ ] mypy src/mycontext          — type check clean
[ ] pytest tests/unit/ -v       — all tests pass
[ ] pytest test_enterprise_gating.py — enterprise gating correct
[ ] Enterprise exclusion confirmed in pyproject.toml
[ ] Version bumped in pyproject.toml AND __init__.py (must match)
[ ] CHANGELOG.md updated
[ ] README updated (new capabilities, table, quick start)
[ ] cd website && npm run build — docs build clean
[ ] New pages added to sidebars.ts
[ ] python -m build             — wheel + sdist built
[ ] Wheel inspected — no enterprise/ files
[ ] twine upload testpypi       — test upload successful
[ ] Smoke test from Test PyPI   — core, generate_context, gating
[ ] twine upload dist/*         — production upload
[ ] Smoke test from PyPI        — all checks pass
[ ] git tag vX.Y.Z && git push  — tagged and pushed
[ ] GitHub Release page created with changelog
[ ] CI (docs.yml) passes
[ ] PyPI page verified
[ ] Docs site verified
```

---

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Enterprise patterns accessible in free install | `pyproject.toml` exclude block removed | Restore the `exclude` entries in both `[wheel]` and `[sdist]` sections |
| `__version__` mismatch | Only one of the two version files updated | Update both `pyproject.toml` and `src/mycontext/__init__.py` |
| Docs build fails | New page not added to `sidebars.ts` | Add the doc ID to the correct sidebar category |
| Docs build fails | Broken internal link in a `.md` file | Find and fix the link — Docusaurus reports the file and line |
| Test PyPI install missing a module | New file not in `src/mycontext/` package tree | Verify the file is under `src/mycontext/` and the package is re-built |
| `generate_context` not importable | Not added to `intelligence/__init__.py` or `mycontext/__init__.py` | Add to both `__all__` lists and import lines |
| LLM auth error in tests | Mock patch target is wrong | Patch the name as bound in the module (`mycontext.intelligence.context_generator.get_provider`), not where it's defined |
