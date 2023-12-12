from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from worker import create_task


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    """
    페이로드 유형에 기반하여 작업을 실행합니다.

    Args:
        payload (dict): 작업 유형을 포함하는 페이로드입니다.

    Returns:
        JSONResponse: 작업 ID를 포함하는 응답입니다.
    """
    # 클라이언트로부터 받은 데이터(payload) 중에서 'type' 키에 해당하는 값을 가져와 'task_type' 변수에 저장합니다.
    task_type = payload["type"]

    # 'create_task.delay' 함수를 호출하여 비동기 작업을 생성합니다. 
    # 'task_type'을 정수형으로 변환하여 이 함수의 인자로 전달합니다.
    task = create_task.delay(int(task_type))

    # 생성된 작업의 ID를 포함하는 JSON 응답을 클라이언트에 반환합니다.
    # 이는 클라이언트가 작업의 상태를 추적할 수 있게 합니다.
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    """
    주어진 task_id에 대한 상태를 조회하는 함수입니다.

    Parameters:
        task_id (str): 조회할 task의 고유 식별자입니다.

    Returns:
        JSONResponse: task_id, task_status, task_result를 포함한 JSON 형태의 응답입니다.
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)