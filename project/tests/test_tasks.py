import json
from unittest.mock import patch

from worker import create_task

# 홈페이지 라우트가 정상적으로 작동하는지 테스트하는 함수입니다.
def test_home(test_app):
    # 테스트 클라이언트를 사용하여 홈페이지 ('/') 경로에 대한 GET 요청을 보냅니다.
    response = test_app.get("/")
    # 응답 상태 코드가 200(정상)인지 확인합니다.
    assert response.status_code == 200

# create_task 작업이 예상대로 작동하는지 테스트하는 함수입니다.
def test_task():
    # create_task 작업을 여러 입력값(1, 2, 3)으로 실행하고, 정상적으로 수행되는지 확인합니다.
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)

# create_task 작업의 호출을 모의(Mocking)하여 테스트하는 함수입니다.
@patch("worker.create_task.run")
def test_mock_task(mock_run):
    # 모의 객체를 사용하여 create_task 작업을 호출하고, 한 번만 호출되었는지 확인합니다.
    assert create_task.run(1)
    create_task.run.assert_called_once_with(1)

    # 모의 객체를 사용하여 create_task 작업을 추가로 호출하고, 호출 횟수가 증가했는지 확인합니다.
    assert create_task.run(2)
    assert create_task.run.call_count == 2

    # 모의 객체를 사용하여 create_task 작업을 추가로 호출하고, 호출 횟수가 정확한지 확인합니다.
    assert create_task.run(3)
    assert create_task.run.call_count == 3

# 작업 상태를 테스트하는 함수입니다.
def test_task_status(test_app):
    # POST 요청을 사용하여 새 작업을 생성하고, 반환된 작업 ID를 검사합니다.
    response = test_app.post("/tasks", data=json.dumps({"type": 1}))
    content = response.json()
    task_id = content["task_id"]
    assert task_id

    # GET 요청을 사용하여 생성된 작업의 상태를 확인합니다.
    response = test_app.get(f"tasks/{task_id}")
    content = response.json()
    # 작업 상태가 'PENDING'(대기 중)인지, 결과가 None(없음)인지 확인합니다.
    assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
    assert response.status_code == 200

    # 작업 상태가 'SUCCESS'(성공)로 변경될 때까지 계속 상태를 확인합니다.
    while content["task_status"] == "PENDING":
        response = test_app.get(f"tasks/{task_id}")
        content = response.json()
    # 최종적으로 작업 상태가 'SUCCESS'이고, 결과가 True인지 확인합니다.
    assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}
