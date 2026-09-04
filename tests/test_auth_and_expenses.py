def test_signup_and_login(client):
    # 1. Sign up a new user
    signup_res = client.post(
        "/auth/signup",
        json={"username": "testuser", "email": "test@example.com", "password": "securepassword123"}
    )
    assert signup_res.status_code == 201
    assert signup_res.json()["username"] == "testuser"

    # 2. Log in using OAuth2 Form Data
    login_res = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "securepassword123"}
    )
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_expense_user_isolation(client):
    # Setup User A
    client.post("/auth/signup", json={"username": "usera", "email": "a@example.com", "password": "password123"})
    login_a = client.post("/auth/login", data={"username": "usera", "password": "password123"}).json()
    token_a = login_a["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Setup User B
    client.post("/auth/signup", json={"username": "userb", "email": "b@example.com", "password": "password123"})
    login_b = client.post("/auth/login", data={"username": "userb", "password": "password123"}).json()
    token_b = login_b["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates an expense
    create_res = client.post(
        "/expenses/",
        json={"amount": 45.50, "description": "Groceries"},
        headers=headers_a
    )
    assert create_res.status_code == 200
    expense_id = create_res.json()["id"]

    # User B should see 0 expenses
    user_b_expenses = client.get("/expenses/", headers=headers_b).json()
    assert len(user_b_expenses) == 0

    # User B should NOT be able to delete User A's expense
    delete_res = client.delete(f"/expenses/{expense_id}", headers=headers_b)
    assert delete_res.status_code == 404