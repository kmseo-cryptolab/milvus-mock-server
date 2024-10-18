# tests/unit_tests/test_user_schema.py
import pytest

from app.schemas.base import camel_case_alias_generator
from app.schemas.user import UserCreate


def test_camel_case_alias_generator():
    assert camel_case_alias_generator("user_name") == "userName"
    assert camel_case_alias_generator("user_first_name") == "userFirstName"
    assert camel_case_alias_generator("first_name") == "firstName"
    assert camel_case_alias_generator("last") == "last"


def test_user_serialization():
    input_json = {
        "userName": "john_doe",
        "password": "secret_key",
        "pubKey": "pub_key_value",
    }
    user = UserCreate(**input_json)

    expected_json = {
        "user_name": "john_doe",
        "password": "secret_key",
        "pub_key": "pub_key_value",
    }

    assert user.model_dump() == expected_json


if __name__ == "__main__":
    pytest.main()

