# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Flask web app that serves a chat UI backed by ChatterBot (a rule/corpus-based chatbot library, not an LLM). Built with the Flask app factory pattern under `app/`.

## Commands

```
pip install -r requirements-dev.txt   # runtime deps + pytest
python wsgi.py                        # run the dev server
pytest                                 # run the test suite
pytest tests/test_routes.py::test_home_page   # run a single test
```

`requirements.txt` alone (without `-dev`) installs only runtime dependencies, no pytest. There is no linter configured in this repo.

## Architecture

- `app/__init__.py` — `create_app(config_object=Config, bot=None)`, the app factory. Registers the chat blueprint and stashes the chatbot instance on `app.extensions["chatbot"]`. Pass `bot=` to inject a fake bot (used by tests) instead of building a real ChatterBot.
- `app/config.py` — `Config` class reading `SECRET_KEY`, `FLASK_DEBUG`, `CHATBOT_NAME`, `CHATBOT_DATABASE_URI` from the environment.
- `app/chatbot.py` — `create_bot(name, database_uri)` builds a `ChatBot` with `SQLStorageAdapter` and trains it on `chatterbot.corpus.english` **only if `bot.storage.count() == 0`** (i.e., only on first run against a fresh database — not on every restart). The `chatterbot` imports are deliberately deferred inside the functions so that code paths using an injected fake bot (tests) don't require ChatterBot/spaCy to be installed.
- `app/routes.py` — blueprint with two routes:
  - `GET /` — renders `app/templates/index.html`
  - `GET /get?msg=...` — reads `bot` off `current_app.extensions["chatbot"]`, returns `bot.get_response(msg)` as plain text
- `wsgi.py` — entry point; calls `create_app()` for gunicorn/WSGI servers or direct `python wsgi.py` execution.
- `app/templates/index.html` + `app/static/chat.js` — chat UI. `/get` returns plain text, not HTML, so `chat.js` HTML-escapes both the user's message and the bot's reply (`escapeHtml`) before inserting them into `#chatbox` — do not remove this when touching the chat UI, since ChatterBot responses/user input are otherwise rendered unescaped (XSS).
- `tests/conftest.py` — provides a `FakeBot` (fixed `get_response`) injected via `create_app(bot=FakeBot())`, so tests run without the ChatterBot corpus training step or ML dependencies installed.

## Dependencies

`requirements.txt` is fully pinned (a `pip freeze` of a verified-working install) on ChatterBot 1.2.14 + spaCy 3.8.13 + SQLAlchemy 2.0.51; `runtime.txt` specifies `python-3.14.6` to match, since ChatterBot 1.2.14 requires Python `>=3.10,<3.15`. The `en_core_web_sm` spaCy model is pinned directly in `requirements.txt` as a wheel URL (`en_core_web_sm @ https://...`), so `pip install -r requirements.txt` is sufficient — no separate `python -m spacy download` step. `PyYAML` is also a hard runtime dependency here even though ChatterBot lists it as optional, because `ChatterBotCorpusTrainer` needs it to parse the corpus YAML files.

Keep `runtime.txt` and these pins in sync: don't bump one without checking wheel/version compatibility for the other (verify against the target package's PyPI JSON metadata, e.g. `requires_python` and available wheel tags, before changing either). Runtime dependency bumps are otherwise managed via Dependabot — keep manual bumps minimal and scoped like existing Dependabot commits.
