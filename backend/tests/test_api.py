"""End-to-End-API-Tests über den TestClient (Stub-Scoring, temporäre DB)."""


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["scoring_provider"] == "stub"
    assert "fall-01" in body["cases"]


def test_list_and_get_case(client):
    r = client.get("/cases")
    assert r.status_code == 200
    ids = [c["case_id"] for c in r.json()]
    assert "fall-01" in ids and "fall-02" in ids

    r = client.get("/cases/fall-01")
    assert r.json()["titel"].startswith("Das Geheimnis")

    assert client.get("/cases/gibtsnicht").status_code == 404


def test_get_scene_hides_solution(client):
    r = client.get("/cases/fall-01/scene/szene-05")
    assert r.status_code == 200
    scene = r.json()
    assert scene["mode"] == "fehlerjagd"
    assert scene["proofread_error_count"] == 4
    # Lösungen dürfen NICHT im Szenen-Payload stehen.
    assert "proofread_errors" not in scene
    assert "correct" not in r.text or "correct" not in scene


def test_navigation_choice_and_bonus_gate(client):
    r = client.post("/scene/next", json={
        "case_id": "fall-01", "scene_id": "szene-01", "choice_index": 0,
    })
    assert r.json()["next_scene_id"] == "szene-02a"

    # Bonus gesperrt ohne all_green.
    r = client.post("/scene/next", json={
        "case_id": "fall-01", "scene_id": "szene-07", "all_green": False,
    })
    body = r.json()
    assert body["ended"] and body["skipped_bonus"]

    # Mit all_green offen.
    r = client.post("/scene/next", json={
        "case_id": "fall-01", "scene_id": "szene-07", "all_green": True,
    })
    assert r.json()["next_scene_id"] == "bonus-01"


def test_proofread_check_resolution(client):
    # Zuerst Tokens holen, um die richtigen Indizes zu markieren.
    scene = client.get("/cases/fall-01/scene/szene-05").json()
    text = scene["text"]
    # Markiere alles korrekt via /proofread/check leerer Lauf → tokens + outcomes.
    empty = client.post("/proofread/check", json={
        "case_id": "fall-01", "scene_id": "szene-05", "marked_indices": [],
    }).json()
    correct_indices = [o["token_index"] for o in empty["outcomes"]]

    r = client.post("/proofread/check", json={
        "case_id": "fall-01", "scene_id": "szene-05",
        "marked_indices": correct_indices,
    })
    body = r.json()
    assert body["all_found"] is True
    assert body["total"] == 4 and body["found_count"] == 4
    by_shown = {o["shown"]: o for o in body["outcomes"]}
    assert by_shown["ales"]["regel"] == "8"
    assert by_shown["regal"]["correct"] == "Regal"
    assert "Bücehr" in text


def test_proofread_on_non_fehlerjagd_is_400(client):
    r = client.post("/proofread/check", json={
        "case_id": "fall-01", "scene_id": "szene-01", "marked_indices": [],
    })
    assert r.status_code == 400


def test_score_fluency_stub(client):
    r = client.post("/score/fluency", data={
        "expected_text": "Im Regal stehen viele Bücher",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["provider"] == "stub"
    assert body["calibrated"] is False
    assert len(body["words"]) == 5


def test_profile_and_progress_flow(client):
    pid = client.post("/profiles", json={"name": "Antonia"}).json()["id"]
    r = client.put("/progress", json={
        "profile_id": pid, "case_id": "fall-01", "current_scene": "szene-03",
    })
    assert r.json()["current_scene"] == "szene-03"
    # Upsert: gleiche (profile, case) aktualisiert statt zu duplizieren.
    client.put("/progress", json={
        "profile_id": pid, "case_id": "fall-01", "current_scene": "szene-05",
        "completed": True,
    })
    rows = client.get(f"/progress/{pid}").json()
    assert len(rows) == 1 and rows[0]["completed"] is True

    prof = client.post("/points", json={"profile_id": pid, "delta": 50}).json()
    assert prof["points"] == 50
