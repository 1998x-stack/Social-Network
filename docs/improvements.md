# Improvement History

### 2026-11-05 05:18 UTC — ChatGPT Portfolio Iteration
- Run ID: 20261105T051853Z-social-readme
- Repo / Base SHA: 1998x-stack/Social-Network @ a2f85667e24b296e08252fd0dd293e6a192be1c5
- Historical context: docs/improvements.md was absent (404) before modification; no PRs existed. This is the first log entry.
- Product problem & expected user value: Running python main.py to scaffold missing chapters unexpectedly deletes the curated README quality bar, demo evidence and setup guidance. Preserve learner-facing documentation by default.
- Engineering diagnosis & evidence: netlab/generate.py main() unconditionally invokes gen_readme(), which overwrites README.md with write_text(); main.py calls main() directly. The module docstring promises only missing files are written.
- Options & decision: README safety (score 17 = 5+4+5+5-1-1); placeholder test honesty (13 = 4+3+5+4-2-1); chapter discovery (8 = 4+1+3+3-2-1). Chose the destructive first-use documentation regression.
- Changes: netlab/generate.py adds explicit --overwrite-readme; default leaves README unchanged. tests/test_generate_readme.py covers preservation, opt-in and invalid CLI arguments.
- Validation: C — static source review; D — new pytest tests not executed in a full checkout. Commands pending: python -m pytest tests/test_generate_readme.py -q; ruff check netlab/generate.py tests/test_generate_readme.py; python -m pytest. No CI success claimed.
- Security & regression review: No production, workflow, permission or dependency changes. Existing explicit generator functionality preserved. CLI main() still callable without arguments.
- Risk & rollback: Users relying on implicit README replacement now need --overwrite-readme; this is intentional to prevent data loss. Revert this PR to restore the old behavior.
- Follow-up: Audit placeholder tests that assert True, prioritizing runnable chapter demos.
- Commit: pending
- PR: pending
