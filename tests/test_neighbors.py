"""前後ページを足す処理のテスト（API も検索DBも使わない）。"""

from app.retrieval import add_neighbors


def page(doc, n):
    return {"page_id": f"{doc}-p{n:03d}", "document_id": doc, "page": n, "content": f"{doc} {n}"}


PAGES = [page("lec01-main", n) for n in range(1, 4)] + [page("lec02-main", n) for n in range(1, 5)]


def ids(results):
    return [r["page_id"] for r in results]


def test_adds_previous_and_next_page_after_each_hit():
    hits = [PAGES[4]]  # lec02 p2
    assert ids(add_neighbors(hits, PAGES, 1)) == ["lec02-main-p002", "lec02-main-p001", "lec02-main-p003"]


def test_does_not_cross_into_another_document():
    hits = [PAGES[3]]  # lec02 p1, la anterior es lec01 p3
    assert ids(add_neighbors(hits, PAGES, 1)) == ["lec02-main-p001", "lec02-main-p002"]


def test_no_duplicates_when_hits_are_next_to_each_other():
    hits = [PAGES[4], PAGES[5]]  # lec02 p2 y p3
    result = ids(add_neighbors(hits, PAGES, 1))
    assert len(result) == len(set(result))
    assert result == ["lec02-main-p002", "lec02-main-p001", "lec02-main-p003", "lec02-main-p004"]


def test_neighbor_pages_say_which_hit_they_come_from():
    result = add_neighbors([PAGES[4]], PAGES, 1)
    assert "neighbor_of" not in result[0]
    assert all(r["neighbor_of"] == "lec02-main-p002" for r in result[1:])


def test_zero_keeps_normal_search():
    hits = [PAGES[4]]
    assert add_neighbors(hits, PAGES, 0) == hits


def test_graph_uses_plain_search_for_its_entry_points(monkeypatch):
    from app import retrieval

    calls = []

    def fake_search(query, neighbors=1):
        calls.append(neighbors)
        return []

    monkeypatch.setattr(retrieval, "search", fake_search)
    retrieval.search_graph("LoRA")
    assert calls == [0]
