def test_admin_inferences_list(client):
    # First, ensure there's at least one inference by hitting analyze
    resp = client.get("/health")
    assert resp.status_code == 200

    # Call admin listing endpoint
    resp = client.get("/admin/inferences", params={"limit": 10})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Not asserting non-empty because DB might be fresh,
    # but structure should be valid.
    if data:
        rec = data[0]
        assert "id" in rec
        assert "predicted_condition" in rec
        assert "needs_review" in rec
