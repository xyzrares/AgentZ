# AgentZ

A command-line AI coding agent built in Python as part of the [Boot.dev](https://www.boot.dev) "Build an AI Agent" project. Give it a task in plain English and it works on a codebase by calling tools: it can explore files, read them, write changes, and run Python code, looping until the task is done.

## Features

- **Agentic loop:** the model plans, calls tools, reads the results, and keeps going until it produces a final answer
- **Four tools** the model can call:
  - `get_files_info` lists files and directories
  - `get_file_content` reads a file's contents
  - `write_file` creates or overwrites a file
  - `run_python_file` executes a Python file and returns its output
- **Sandboxed to a working directory:** the agent can't touch anything outside the project it's pointed at
- **Verbose mode:** optionally prints each tool call, token usage, and the raw prompt

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (or pip)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Setup

```bash
git clone https://github.com/YOUR-USERNAME/AgentZ.git
cd AgentZ
uv sync
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

Make sure `.env` is listed in `.gitignore` so your key is never committed.

## Usage

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to see what the agent is doing under the hood:

```bash
uv run main.py "fix the bug in the calculator" --verbose
```

### Example prompts

```bash
uv run main.py "list the files in the root directory"
uv run main.py "what does main.py do?"
uv run main.py "run the calculator tests"
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"
```

## Project structure

```
.
├── main.py             # Entry point and agent loop
├── config.py           # Settings (limits, working directory, etc.)
├── prompts.py          # System prompt
├── call_function.py    # Dispatches the model's tool calls
├── functions/          # Tool implementations and their schemas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/         # Sample project the agent works on
├── .env                # API key (not committed)
└── pyproject.toml
```

## How it works

1. Your prompt is sent to the Gemini model along with a system prompt and the available tool declarations.
2. If the model asks to call a tool, the agent runs it and sends the result back.
3. This repeats until the model returns a plain text response, or an iteration limit is reached.

## Safety notes

This agent can write files and execute code. It's a learning project, **not production-ready**:

- File access is restricted to a permitted working directory, but the sandboxing is basic.
- Don't point it at anything you can't afford to have modified.
- Never commit your `.env` file or API key.

## Acknowledgements

Built following the [Boot.dev](https://www.boot.dev) "Build an AI Agent in Python" course.

## License

MIT
