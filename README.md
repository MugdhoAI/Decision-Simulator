# Decision Simulator

Decision Simulator stress-tests a real choice by staging a debate between several simulated future versions of you. Each future self represents a different option, argues from that path, and responds to the other paths.

It is a local Python CLI. The application sends prompts to Anthropic when you run a simulation, but it does not upload saved reports or operate a remote storage service.

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/MugdhoAI/Decision-Simulator.git
cd Decision-Simulator
python -m pip install -e .
```

Set `ANTHROPIC_API_KEY` before running a live simulation.

## Use

Interactive mode:

```bash
decision-simulator
```

Scriptable mode:

```bash
decision-simulator --decision "Study abroad or stay" --option "Study abroad" --option "Stay" --context "I care about education, family, and building a startup" --rounds 2
```

Print a machine-readable report:

```bash
decision-simulator --decision "Study or work" --option "Study" --option "Work" --json
```

Save a report locally:

```bash
decision-simulator --decision "Study or work" --option "Study" --option "Work" --output reports/debate.json
```

Reports contain the decision, options, context, round count, transcript, creation time, and application version.

## Tests

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

The test suite uses fake clients and mocks, so it does not require an Anthropic API key.

## Structure

The application is packaged under `src/decision_simulator`. The model adapter is separated from the debate engine through a small protocol, input validation happens before generation, transient API failures are retried, and completed simulations can be exported as local JSON.

## Security

Never commit API keys or other secrets. See `SECURITY.md` for reporting guidance.

## License

MIT

## Author

Mugdho (All Asmaul Husnain)

GitHub: https://github.com/MugdhoAI
