from datasets import load_dataset
import requests

# 데이터셋 불러오기
dataset = load_dataset("Cohere/wikipedia-22-12-simple-embeddings")

# Milvus V2 REST API 엔드포인트 및 헤더 설정
USER_TOKEN = "root:password"
url = "http://localhost:10105/v2/vectordb/entities/insert"
headers = {"Authorization": f"Bearer {USER_TOKEN}", "Content-Type": "application/json"}


# 데이터셋에서 벡터 데이터 변환 및 10,000개 단위 요청
def insert_vectors_in_batches(dataset, collection_name, iteration_count, url, headers):
    data = []
    ttl = 0

    for i, record in enumerate(dataset["train"]):
        if ttl >= iteration_count:
            break

        data.append(record)
        ttl += 1

        # 10,000개 단위로 요청을 보냄
        if len(data) == 10000:
            send_request(collection_name, data, url, headers)
            data = []  # 데이터 초기화
            print(f"current: {ttl}")

    # 남은 데이터 요청 보내기
    if data:
        send_request(collection_name, data, url, headers)


# HTTP 요청 전송 함수
def send_request(collection_name, data, url, headers):
    payload = {"collectionName": collection_name, "data": data}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200 and response.json().get("code") == 0:
        print("Successfully inserted vectors.")
        print(f"Insert Count: {response.json()['data'].get('insertCount')}")
    else:
        print("Failed to insert vectors.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")


# 테스트 코드 실행
if __name__ == "__main__":
    collection_name = "wikipedia"
    iteration_count = int(input("Enter the number of iterations: "))
    insert_vectors_in_batches(dataset, collection_name, iteration_count, url, headers)
