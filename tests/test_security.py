
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    create_refresh_token,
    hash_refresh_token,
)


def test_password_hashing():
    password = "TestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)


def test_access_token():
    user_id = "test-user-123"
    role = "Sales Representative"

    token = create_access_token(user_id, role)
    payload = decode_access_token(token)

    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert payload["type"] == "access"


def test_refresh_token():
    token = create_refresh_token()

    hashed_token = hash_refresh_token(token)

    assert token != hashed_token
    assert len(token) > 20
    assert len(hashed_token) == 64
    assert hash_refresh_token(token) == hashed_token


if __name__ == "__main__":
    test_password_hashing()
    test_access_token()
    test_refresh_token()

    print("All authentication security tests passed!")
