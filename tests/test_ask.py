from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="Respuesta",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        models = FakeModels()

        def __init__(self, **kwargs):
            pass

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    clock_values = iter([10.0, 10.25])
    monkeypatch.setattr(ask, "perf_counter", lambda: next(clock_values))

    assert ask.ask("Pregunta") == "Respuesta"
    assert capsys.readouterr().out.splitlines() == [
        "[tiempo de respuesta] 0.250s",
        "[tokens] entrada=12, salida=7",
    ]


def test_ask_prints_response_time_when_request_fails(monkeypatch, capsys):
    class FakeModels:
        def generate_content(self, **kwargs):
            raise RuntimeError("request failed")

    class FakeClient:
        models = FakeModels()

        def __init__(self, **kwargs):
            pass

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    clock_values = iter([20.0, 22.5])
    monkeypatch.setattr(ask, "perf_counter", lambda: next(clock_values))

    try:
        ask.ask("Pregunta")
    except RuntimeError as error:
        assert str(error) == "request failed"
    else:
        raise AssertionError("ask should propagate request errors")

    assert capsys.readouterr().out.strip() == "[tiempo de respuesta] 2.500s"