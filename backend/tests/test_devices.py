def test_create_device_admin_success(admin_client):
    response = admin_client.post(
        "/devices", 
        json={"name": "Test Device", "location": "溫室"}
    )
    assert response.status_code == 200

def test_create_device_viewer_failure(viewer_client):
    response = viewer_client.post(
        "/devices", 
        json={"name": "Test Device", "location": "溫室"}
    )
    assert response.status_code == 403

def test_get_devices_admin(admin_client, operator_client):
    admin_client.post(
        "/devices", 
        json={"name": "Admin Device", "location": "溫室A"}
    )
    operator_client.post(
        "/devices", 
        json={"name": "Operator Device", "location": "溫室B"}
    )
    response = admin_client.get("/devices")
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 2

def test_get_devices_operator(admin_client, operator_client):
    admin_client.post(
        "/devices", 
        json={"name": "Admin Device", "location": "溫室A"}
    )
    operator_client.post(
        "/devices", 
        json={"name": "Operator Device", "location": "溫室B"}
    )
    response = operator_client.get("/devices")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1