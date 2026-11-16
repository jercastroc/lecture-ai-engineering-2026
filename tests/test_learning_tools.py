"""make_quiz と save_learning_log のテスト（LLMもAPIキーも使わない）。"""

import json

from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent, run_with_approval


def test_make_quiz_returns_question_and_answer_of_that_lecture():
    quiz = json.loads(tools.make_quiz(2))
    assert set(quiz) == {"question", "answer"}
    terms = [e for e in tools.load_glossary() if e["lecture"] == 2]
    assert any(e["definition"] == quiz["answer"] for e in terms)


def test_make_quiz_for_unknown_lecture_returns_message():
    assert "ありません" in tools.make_quiz(0)


def test_save_learning_log_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path / "learning_log")
    message = tools.save_learning_log("LoRA", "rank を変えて比べた")
    files = list((tmp_path / "learning_log").glob("*.md"))
    assert len(files) == 1
    assert files[0].name in message
    text = files[0].read_text(encoding="utf-8")
    assert text.startswith("# LoRA") and "rank を変えて比べた" in text


def _run_save(tmp_path, monkeypatch, reply):
    monkeypatch.setattr(tools, "LOG_DIR", tmp_path / "learning_log")
    questions = []

    def fake_input(prompt):
        questions.append(prompt)
        return reply

    model = TestModel(call_tools=["save_learning_log"])
    with agent.override(model=model):
        run_with_approval(agent, "学習を記録して", model=None, ask_user=fake_input)
    return questions, list((tmp_path / "learning_log").glob("*.md"))


def test_save_waits_for_approval_and_saves_when_yes(tmp_path, monkeypatch):
    questions, files = _run_save(tmp_path, monkeypatch, "y")
    assert len(questions) == 1 and "save_learning_log" in questions[0]
    assert len(files) == 1


def test_save_is_skipped_when_user_says_no(tmp_path, monkeypatch):
    questions, files = _run_save(tmp_path, monkeypatch, "n")
    assert len(questions) == 1
    assert files == []
