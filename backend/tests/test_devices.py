def test_create_device_admin_success(client, admin_token):
    response = client.post(
        "/devices/", 
        json={"name": "Test Device", "location": "溫室"}, 
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_create_device_viewer_failure(client, viewer_token):
    response = client.post(
        "/devices/", 
        json={"name": "Test Device", "location": "溫室"}, 
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403

def test_get_devices_admin(client, admin_token, operator_token):
    client.post(
        "/devices/", 
        json={"name": "Admin Device", "location": "溫室A"}, 
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/devices/", 
        json={"name": "Operator Device", "location": "溫室B"}, 
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    response = client.get(
        "/devices/", 
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_get_devices_operator(client, admin_token, operator_token):
    client.post(
        "/devices/", 
        json={"name": "Admin Device", "location": "溫室A"}, 
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/devices/", 
        json={"name": "Operator Device", "location": "溫室B"}, 
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    response = client.get(
        "/devices/", 
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1