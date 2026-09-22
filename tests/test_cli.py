from main import build_parser


def test_parser_accepts_multiple_options():
    args = build_parser().parse_args(
        ["--decision", "Study or work", "--option", "Study", "--option", "Work", "--rounds", "3"]
    )
    assert args.decision == "Study or work"
    assert args.options == ["Study", "Work"]
    assert args.rounds == 3


def test_parser_defaults_to_interactive_mode():
    args = build_parser().parse_args([])
    assert args.decision is None
    assert args.options is None
    assert args.rounds == 2


def test_cli_noninteractive_mode_runs_without_api():
    from main import main

    class FakeClient:
        def generate(self, system_prompt, user_prompt, *, max_tokens=600):
            return "test response"

    assert main(
        ["--decision", "A or B", "--option", "A", "--option", "B", "--rounds", "1"],
        client=FakeClient(),
    ) == 0
