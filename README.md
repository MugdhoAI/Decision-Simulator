# Decision Simulator

Decision Simulator stress tests a real choice by staging a debate between several simulated future versions of you.

Each future self represents a different option, argues from that path, and responds to the other paths. The result is a structured debate that helps expose trade offs, assumptions, and possible consequences before making a decision.

The application runs locally as a Python CLI. Live simulations send prompts to Anthropic. Saved reports remain local and are not uploaded to a remote storage service.

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/MugdhoAI/Decision-Simulator.git
cd Decision-Simulator
python -m pip install -e .
```

Set `ANTHROPIC_API_KEY` before running a live simulation.

## Run a simulation

Interactive mode:

```bash
decision-simulator
```

Scriptable mode:

```bash
decision-simulator --decision "Study abroad or stay" --option "Study abroad" --option "Stay" --context "I care about education, family, and building a startup" --rounds 2
```

Generate a machine readable report:

```bash
decision-simulator --decision "Study or work" --option "Study" --option "Work" --json
```

Save a report locally:

```bash
decision-simulator --decision "Study or work" --option "Study" --option "Work" --output reports/debate.json
```

Reports contain the decision, options, context, round count, transcript, creation time, and application version.

## How it works

The application separates the debate engine from the model provider.

1. The CLI validates the decision and options.
2. Each option is represented as a different future perspective.
3. The model generates arguments for each perspective.
4. The perspectives respond to the competing paths.
5. The completed debate can be printed or saved as JSON.

This keeps the core decision flow independent from the model adapter and makes the application easier to test.

## Tests

Install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
python -m pytest
```

The test suite uses fake clients and mocks, so it does not require an Anthropic API key.

## Security

Never commit API keys or other secrets.

See `SECURITY.md` for reporting guidance.

## License

MIT

## Author

Mugdho (All Asmaul Husnain)

GitHub: https://github.com/MugdhoAI
