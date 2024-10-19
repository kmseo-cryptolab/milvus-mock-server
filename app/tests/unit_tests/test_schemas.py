"""
tests.unit_tests.test_user_schema.py
"""

import pytest

from app.schemas.base import camel_case_alias_generator
from app.schemas.user import UserCreate


def test_camel_case_alias_generator():
    """
    camelCase 변환 테스트
    """

    # GIVEN snake_case 형식의 문자열들
    snake_case_inputs = ["user_name", "user_first_name", "first_name", "last"]

    # WHEN camel_case_alias_generator 함수를 각각 실행하면
    results = [camel_case_alias_generator(input_str) for input_str in snake_case_inputs]

    # THEN camelCase로 변환된 결과를 확인할 수 있다.
    assert results == ["userName", "userFirstName", "firstName", "last"]


def test_user_serialization():
    """
    UserCreate 모델 직렬화 테스트
    """

    # GIVEN camelCase로 된 사용자 입력 데이터
    input_json = {
        "userName": "john_doe",
        "password": "secret_key",
        "pubKey": "pub_key_value",
    }

    # WHEN UserCreate 모델로 변환 후 model_dump를 실행하면
    user = UserCreate(**input_json)
    result = user.model_dump()

    # THEN snake_case로 변환된 결과를 확인할 수 있다.
    expected_json = {
        "user_name": "john_doe",
        "password": "secret_key",
        "pub_key": "pub_key_value",
    }
    assert result == expected_json


if __name__ == "__main__":
    pytest.main()
