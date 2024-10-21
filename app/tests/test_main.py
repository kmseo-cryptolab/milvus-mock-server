"""
app.tests.test_main.py
"""

# pylint: disable=redefined-outer-name

import random
import pytest

from fastapi.testclient import TestClient

from app.main import app

USERNAME = f"tenant-test-{random.randint(1, 1000)}"
PASSWORD = "password"
ROOT_TOKEN = "root:password"
USER_TOKEN = f"{USERNAME}:{PASSWORD}"


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def headers():
    return {"Content-Type": "application/json"}


def test_create_new_user(client, headers):
    """
    새로운 사용자를 생성하는 테스트
    """

    # GIVEN 새로운 사용자 정보 (userName, password, pubKey)
    url = "/v2/vectordb/users/create"
    headers["Authorization"] = f"Bearer {ROOT_TOKEN}"
    data = {
        "userName": USERNAME,
        "password": PASSWORD,
        "pubKey": "pk-xxxxxxxxxxxxxxxxxxxxx",
    }

    # WHEN 사용자 생성 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 응답 코드가 0이어야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0


def test_create_duplicated_user(client, headers):
    """
    중복된 사용자를 생성하려고 할 때의 테스트
    """

    # GIVEN 이미 생성된 사용자 정보
    url = "/v2/vectordb/users/create"
    headers["Authorization"] = f"Bearer {ROOT_TOKEN}"
    data = {
        "userName": USERNAME,
        "password": PASSWORD,
        "pubKey": "pk-xxxxxxxxxxxxxxxxxxxxx",
    }

    # WHEN 사용자 생성 API를 동일 조건으로 두 번 호출하면
    client.post(url, json=data, headers=headers)
    duplicate_result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 400이어야 한다.
    assert duplicate_result.status_code == 400


def test_list_users(client, headers):
    """
    사용자 목록을 가져오는 테스트
    """

    # GIVEN 사용자 인증 정보
    url = "/v2/vectordb/users/list"
    headers["Authorization"] = f"Bearer {ROOT_TOKEN}"

    # WHEN 사용자 목록 API를 호출하면
    result = client.post(url, headers=headers)

    # THEN 응답 상태 코드가 200이고, 데이터가 포함되어 있어야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0
    assert "data" in result.json()
    assert isinstance(result.json()["data"], list)


def test_create_collection(client, headers):
    """
    새로운 컬렉션을 생성하는 테스트
    """

    # GIVEN 새로운 컬렉션 정보 (name, dimension)
    url = "/v2/vectordb/collections/create"
    headers["Authorization"] = f"Bearer {USER_TOKEN}"
    data = {"name": "test_collection", "dimension": 5}

    # WHEN 컬렉션 생성 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 응답 코드가 0이어야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0


def test_list_collections(client, headers):
    """
    컬렉션 목록을 가져오는 테스트
    """

    # GIVEN 사용자 인증 정보
    url = "/v2/vectordb/collections/list"
    headers["Authorization"] = f"Bearer {USER_TOKEN}"
    data = {"dbName": "test_collection"}

    # WHEN 컬렉션 목록 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 데이터가 포함되어 있어야 한다.
    assert result.status_code == 200
    assert "data" in result.json()


def test_insert_vectors(client, headers):
    """
    벡터를 삽입하는 테스트
    """

    # GIVEN 컬렉션 이름과 벡터 데이터
    url = "/v2/vectordb/entities/insert"
    headers["Authorization"] = f"Bearer {USER_TOKEN}"
    data = {
        "collectionName": "test_collection",
        "data": [
            {
                "id": 1,
                "vector": [0.1, 0.2, 0.3, 0.4, 0.5],
                "color": "red",
            },
            {
                "id": 2,
                "vector": [0.2, 0.3, 0.4, 0.5, 0.6],
                "color": "blue",
            },
        ],
    }
    # WHEN 벡터 삽입 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 응답 데이터에 삽입 개수가 포함되어야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0
    assert "insertCount" in result.json()["data"]


def test_search_vectors(client, headers):
    """
    벡터 검색 테스트
    """

    # GIVEN 컬렉션 이름과 검색할 벡터 데이터
    url = "/v2/vectordb/entities/search"
    headers["Authorization"] = f"Bearer {USER_TOKEN}"
    data = {
        "collectionName": "test_collection",
        "data": [[0.1, 0.2, 0.3, 0.4, 0.5]],
        "limit": 2,
        "annsField": "vector",
        "outputFields": ["color"],
    }

    # WHEN 벡터 검색 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 응답 데이터가 비어있지 않아야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0
    assert len(result.json()["data"]) > 0


def test_drop_collection(client, headers):
    """
    컬렉션 삭제 테스트
    """

    # GIVEN 삭제할 컬렉션 정보
    url = "/v2/vectordb/collections/drop"
    headers["Authorization"] = f"Bearer {USER_TOKEN}"
    data = {"name": "test_collection"}

    # WHEN 컬렉션 삭제 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 응답 코드가 0이어야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0


def test_unauthorized_access(client, headers):
    """
    권한이 없는 접근 테스트
    """

    # GIVEN 잘못된 인증 정보
    url = "/v2/vectordb/collections/list"
    headers["Authorization"] = "Bearer invalid:token"
    data = {"dbName": "_default"}

    # WHEN 컬렉션 목록 API를 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 401이어야 한다.
    assert result.status_code == 401


def test_drop_existent_user(client, headers):
    """
    사용자 삭제 테스트
    """

    # GIVEN 존재하는 사용자 정보
    url = "/v2/vectordb/users/drop"
    headers["Authorization"] = f"Bearer {ROOT_TOKEN}"
    data = {"userName": USERNAME}

    # WHEN 사용자 삭제 API 호출하면
    result = client.post(url, json=data, headers=headers)

    # THEN 응답 상태 코드가 200이고, 응답 코드가 0이야 한다.
    assert result.status_code == 200
    assert result.json()["code"] == 0


def test_drop_not_existent_user(client, headers):
    """
    존재하지 않는 사용자 삭제 테스트
    """

    # GIVEN 존재하지 않는 사용자 정보
    url = "/v2/vectordb/users/drop"
    headers["Authorization"] = f"Bearer {ROOT_TOKEN}"
    non_existent_user = "non-existent-user"

    # WHEN 사용자 삭제 API 호출하면
    drop_result = client.post(url, json={"userName": non_existent_user}, headers=headers)

    # THEN 응답 상태 코드가 404여야 한다.
    assert drop_result.status_code == 404
    assert drop_result.json()["detail"] == "User not found"


if __name__ == "__main__":
    pytest.main([__file__])
