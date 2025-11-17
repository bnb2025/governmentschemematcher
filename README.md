Google Flash 2.5 — Minimal HTTP Agent

What this is
- A minimal Python template that sends a user prompt to a Generative Language HTTP endpoint
  (model `google-flash-2.5`) and prints the reply.

Files
- `agent.py`: A BigQuery agent that can interact with a BigQuery dataset.
- `requirements.txt`: runtime dependency (`requests`).

Setup
1. Create a virtual environment (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set your API key in the environment (PowerShell):

```powershell
$env:GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
```

Alternative: read the API key from a file

If you store your API key in a local file (for example the file you mentioned at
`C:\workspace\google_flash_agent\gokul-harsh-bnb2025-4b6b290f0621`), the agent will
attempt to read it automatically. You can also explicitly point the agent to a
file by setting the `GOOGLE_API_KEY_FILE` environment variable in PowerShell:

```powershell
$env:GOOGLE_API_KEY_FILE = 'C:\workspace\google_flash_agent\gokul-harsh-bnb2025-4b6b290f0621'
```

The agent will try the `GOOGLE_API_KEY` env var first, then the file path in
`GOOGLE_API_KEY_FILE`, and finally the default path shown above.

Running
- One-shot prompt from CLI:

```powershell
python agent.py --prompt "Write a friendly reply to: 'How are you?'"
```



- Interactive (stdin):

```powershell
python agent.py
# then type/paste your prompt and finish with Ctrl+Z Enter on Windows
```

Notes & next steps
- This template uses a simple HTTP pattern with an API key query parameter. In many
  production setups you'll want to use the official client library or OAuth 2.0 bearer tokens.
- Field names in the JSON response can differ across API versions — `agent.py` attempts several
  common extraction patterns and falls back to pretty-printed JSON.
- If you'd like, I can:
  - convert this to use the official Google SDK, or
  - wrap it in a tiny Flask API to expose it as a local web service, or
  - add OAuth-based authentication instead of API keys.
