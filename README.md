# Flask ChatBot

A minimal Flask web app that serves a browser-based chat UI backed by [ChatterBot](https://chatterbot.readthedocs.io/), a corpus-trained conversational engine (not an LLM).

## Features

- Simple chat interface (`app/templates/index.html`) with jQuery-driven message polling
- ChatterBot instance trained on the built-in English corpus on first startup only (subsequent restarts reuse the trained SQLite database)
- Single `/get` endpoint for retrieving bot responses
- App factory pattern (`create_app`) so the bot can be swapped out for tests

## Tech stack

- [Flask](https://flask.palletsprojects.com/) for the web server
- [ChatterBot](https://chatterbot.readthedocs.io/) 1.2.14 + `chatterbot-corpus` for the conversational engine (SQLite storage via `SQLStorageAdapter`), using spaCy 3.8 + the `en_core_web_sm` model for tagging
- jQuery + Font Awesome (loaded from CDN) for the frontend
- [pytest](https://docs.pytest.org/) for tests

## Getting started

### Prerequisites

- Python version matching `runtime.txt` (currently 3.14; ChatterBot 1.2.14 requires Python >=3.10,<3.15)

### Installation

```bash
pip install -r requirements.txt
```

This also installs the `en_core_web_sm` spaCy model (pinned directly in `requirements.txt` as a wheel URL), so no separate `spacy download` step is needed.

For development (adds pytest):

```bash
pip install -r requirements-dev.txt
```

### Running locally

```bash
python wsgi.py
```

The app starts a Flask dev server. ChatterBot trains on the English corpus the first time it runs (so the first startup takes a moment); subsequent restarts reuse the existing `database.sqlite3` and skip retraining.

Visit `http://localhost:5000` in your browser and start chatting.

### Configuration

The app reads these environment variables (see `app/config.py`):

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | `dev` | Flask secret key |
| `FLASK_DEBUG` | `0` | Set to `1` to enable debug mode |
| `CHATBOT_NAME` | `Chatterbot` | Name passed to `ChatBot()` |
| `CHATBOT_DATABASE_URI` | `sqlite:///database.sqlite3` | ChatterBot's storage backend |

### Running tests

```bash
pytest
```

Tests inject a fake bot (see `tests/conftest.py`) so they run instantly without training the real ChatterBot corpus or requiring the ML dependencies to be installed.

## Project structure

```
app/
  __init__.py         # App factory (create_app)
  config.py            # Environment-based configuration
  chatbot.py            # ChatterBot creation + one-time training
  routes.py              # Flask blueprint: / and /get
  templates/
    index.html            # Chat UI
  static/
    style.css              # Chat UI styling
    chat.js                 # Chat UI behavior (escapes output to prevent XSS)
    favicon.ico
tests/
  conftest.py           # Fixtures (fake bot, test client)
  test_routes.py          # Route tests
wsgi.py                # WSGI entry point (calls create_app())
requirements.txt      # Runtime dependencies
requirements-dev.txt  # Runtime + pytest
runtime.txt
Procfile
```

## API

- `GET /` — renders the chat UI
- `GET /get?msg=<text>` — returns the bot's plain-text reply to `<text>`

## Deployment

`Procfile` runs `gunicorn wsgi:app`. Set `CHATBOT_DATABASE_URI` to a persistent path/database if your host doesn't preserve the filesystem between deploys, otherwise ChatterBot will retrain from scratch on every deploy.

## Security

See [SECURITY.md](./SECURITY.md) for the vulnerability reporting policy. Chat messages and bot replies are HTML-escaped client-side (`app/static/chat.js`) before being inserted into the page, since `/get` returns plain text that is otherwise rendered as HTML.
