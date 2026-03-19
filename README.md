# PermessoAlert

Telegram bot for tracking permesso di soggiorno (Italian residence permit) status.

Periodically checks the police RSS feed and notifies you when the status changes. Supports 3 languages (RU/EN/IT), up to 10 cases per user, checks every 6 hours.

## Getting Started

1. Create a bot via [@BotFather](https://t.me/BotFather) and get the token
2. Copy `.env.example` to `.env` and set your token:
   ```
   cp .env.example .env
   ```
3. Run:
   ```
   ./run.sh
   ```
   The script will automatically create a virtual environment and install dependencies.

## Usage

1. Send `/start` — the bot will ask you to choose a language (on subsequent launches it goes straight to the menu)
2. Everything is controlled via inline buttons:
   - **➕ Add case** — the bot will ask for a case number and verify it
   - **📋 Status** — current status of all tracked cases
   - **🗑 Remove case** — list of cases with delete buttons
   - **🌐 Language** — change interface language
   - **❓ Help** — show help

## Project Structure

```
bot/
├── main.py        — entry point, handler registration
├── handlers.py    — command and inline button handlers
├── checker.py     — RSS request and status parsing
├── scheduler.py   — periodic check (every 6 hours)
├── database.py    — async SQLite (users + tracked_cases)
└── locale.py      — translations RU/EN/IT
```