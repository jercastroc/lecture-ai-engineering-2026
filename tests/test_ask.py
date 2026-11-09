"""ask.py のテスト（LLMもAPIキーも使わない）。"""

from types import SimpleNamespace

import pytest

from app import ask


def _fake_genai(monkeypatch, generate_content):
    class FakeModels:
        pass

    FakeModels.generate_content = staticmethod(generate_content)

    class FakeClient:
        models = FakeModels()

        def __init__(self, **kwargs):
            pass

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")


def _fake_clock(monkeypatch, *values):
    ticks = iter(values)
    monkeypatch.setattr(ask, "time", SimpleNamespace(perf_counter=lambda: next(ticks)))


def test_ask_prints_time_and_token_counts(monkeypatch, capsys):
    usage = SimpleNamespace(
        prompt_token_count=12,
        candidates_token_count=7,
        thoughts_token_count=30,
        total_token_count=49,
    )
    response = SimpleNamespace(text="answer", usage_metadata=usage)
    _fake_genai(monkeypatch, lambda **kwargs: response)
    _fake_clock(monkeypatch, 10.0, 10.25)

    assert ask.ask("q") == "answer"
    assert capsys.readouterr().out.splitlines() == [
        "[time] 0.25s",
        "[tokens] input=12 output=7 thoughts=30 total=49",
    ]


def test_ask_handles_missing_thoughts_and_usage(monkeypatch, capsys):
    usage = SimpleNamespace(
        prompt_token_count=3,
        candidates_token_count=4,
        thoughts_token_count=None,
        total_token_count=7,
    )
    _fake_genai(monkeypatch, lambda **kwargs: SimpleNamespace(text="a", usage_metadata=usage))
    _fake_clock(monkeypatch, 0.0, 1.0)
    ask.ask("q")
    assert "thoughts=0" in capsys.readouterr().out

    _fake_genai(monkeypatch, lambda **kwargs: SimpleNamespace(text="a", usage_metadata=None))
    _fake_clock(monkeypatch, 0.0, 1.0)
    ask.ask("q")
    assert "no usage metadata" in capsys.readouterr().out


def test_ask_prints_time_when_request_fails(monkeypatch, capsys):
    def boom(**kwargs):
        raise RuntimeError("request failed")

    _fake_genai(monkeypatch, boom)
    _fake_clock(monkeypatch, 20.0, 22.5)

    with pytest.raises(RuntimeError):
        ask.ask("q")
    assert capsys.readouterr().out.strip() == "[time] 2.50s"
