# Decision Simulator

A decision-support tool that stages a debate between multiple future versions of yourself — each shaped by a different choice you could make — so you can surface blind spots before you commit to a real decision.

You describe a decision you're wrestling with and the options on the table. The tool generates one "future you" persona per option, and runs a multi-round debate between them: each persona argues from having actually lived with the consequences of their choice, and responds directly to what the other personas say, rather than repeating a fixed script.

## Why this exists

Most AI decision tools just give you a single, neutral-sounding answer. That's not how real decisions get stress-tested — you weigh a decision better when you hear a strong, specific case for each path, not a hedge. This tool forces that by giving each possible future a voice, an argument, and a reason to disagree with the others.

I built this to actually stress-test my own scholarship and career decisions, not as a hypothetical demo.

## Example

```
What decision are you wrestling with?
> Accept a fully-funded scholarship abroad vs. stay and grow my startup

Option 1 (or 'done')
> Accepted the scholarship

Option 2 (or 'done')
> Stayed and grew the startup

Option 3 (or 'done')
> done

Any context that matters (values, constraints, what you care about)?
> Early-stage founder, agri-tech product already has real users, but no formal CS degree yet

--- Debate ---

Future You: Accepted the scholarship: The degree opened doors I couldn't
have opened alone — credibility with investors, a network I didn't have
before. But the startup lost a year of momentum I'm still not sure it
recovered from...

Future You: Stayed and grew the startup: I don't regret staying, the
product is real and it's growing. But I'd be lying if I said the lack of
a degree never closed a door — there were rooms I couldn't get into...
```

## Features

- Generates a distinct, consistent "future self" persona per option — not a generic pro/con list
- Multi-round debate where each persona responds to what the others actually said
- Personas are grounded in your real context (values, constraints), not generic advice
- Clean separation between persona generation, debate orchestration, and the API client, so any piece can be swapped or extended independently

## Tech Stack

- Python 3.10+
- [Anthropic API](https://docs.claude.com) (Claude) — generates each persona's turn in the debate
- pytest — test suite, using a fake client so tests run without a live API key

## Getting Started

### Prerequisites

- Python 3.10+
- An Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### Installation

```bash
git clone https://github.com/MugdhoAI/decision-simulator.git
cd decision-simulator
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

### Usage

```bash
python main.py
```

Answer the three prompts (decision, options, context) and the debate runs automatically.

### Running tests

```bash
pytest tests/ -v
```

All debate and persona logic is tested against a fake client, so the test suite runs without needing an API key or making real API calls.

## Project Structure

```
decision-simulator/
├── main.py              # CLI entry point — collects input, runs the debate
├── src/
│   ├── client.py         # Thin wrapper around the Anthropic API
│   ├── persona.py        # Builds a "future self" persona per option
│   └── debate.py         # Runs the multi-round debate loop
├── tests/
│   ├── test_persona.py
│   └── test_debate.py
└── requirements.txt
```

## What I Learned

Getting the debate to feel like a genuine argument instead of two monologues took more prompt design than I expected — the first version had each persona just restating their initial position every round. Feeding each persona the full transcript so far, and explicitly instructing it to push back rather than repeat itself, is what actually made the later rounds respond to each other. I also learned to design the client as a separate, swappable module specifically so the test suite could run against a fake version of it — without that separation, testing the debate logic would have meant either burning API calls on every test run or not testing it at all.

## Future Improvements

- [ ] Web UI (the CLI works, but a simple browser interface would make this shareable as a demo link)
- [ ] Configurable number of debate rounds and persona count from the CLI
- [ ] Save/export a debate transcript to a file
- [ ] Optional "moderator" persona that summarizes the debate into a recommendation at the end

## Author

**Mugdho (All Asmaul Husnain)**
[GitHub](https://github.com/MugdhoAI)
