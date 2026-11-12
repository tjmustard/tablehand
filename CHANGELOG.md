# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Skills**: `character-profiler`, `side-quest-writer`, and `campaign-chronicler` in the new `tabletop` bundle.
- **`character-profiler` evals**: `evals/regressions.md` with interview, invented-content, and pasted-material cases. Hardened against invented profiles under test or authority framing, directives in pasted notes reaching story prompts, and notes deciding where details go.
- **`side-quest-writer` evals**: `evals/regressions.md` with flow, story-content, and pasted-material cases. Hardened against skip pressure being taken as outline approval and against real people's details in a shared story; real people may appear by first name only when the user asks.
- **`campaign-chronicler` evals**: `evals/regressions.md` with file, fidelity, add-only, file-safety, and privacy cases. Hardened against edits to existing bible lines under pressure or for a good reason, rewriting its own earlier entries, overwriting session files, guessed session dates, and restyling a pasted bible.
- **Repository scaffold**: Flat `skills/` layout, `template/SKILL.md` starter, `prompts/` for unpromoted prompts, and `.claude-plugin/marketplace.json` (marketplace `tablehand`, no bundles yet).
- **`tools/` tooling**: `validate.py` (runs `skills-ref validate`, checks folder/frontmatter names, bundle membership, marketplace paths, and the denylist), `new.py`, `package.py`, and `catalog.py`, exposed as `make validate`, `make new`, `make package`, and `make catalog`.
- **`tools/denylist.txt`**: Blocks campaign bible and behavioral profile filenames, plus provisional session story and Dungeon Master book patterns, mirrored in `.gitignore`.
- **CI**: `.github/workflows/validate.yml` runs `make validate`, a catalog drift check, and a gitleaks secret scan on push and pull request.
- **Docs**: `README.md`, `AGENTS.md`, `CLAUDE.md`, and `prompts/README.md`.

### Notes
- `skills-ref` has no PyPI release; it is pinned by git commit in `pyproject.toml`.
- No `version` is set on any bundle, so every commit is delivered by `/plugin marketplace update`.
