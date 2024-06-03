2023/12/12 celery 예제 실행 및 정리

![image](https://github.com/quatch1247/celery_project/assets/80108373/0cdee4d6-7122-4cf8-93ba-51ce18af8c2c)

# 큐 관리 시스템 예제

비동기 작업을 처리하는 분산 시스템에서 큐 관리는 중요한 요소입니다. 이 예제에서는 Celery, FastAPI, Redis, Flower를 사용하여 대기열 문제를 처리하는 방법을 다룹니다.

## 기술 스택

- **Celery**: 작업을 비동기적으로 실행할 수 있는 오픈 소스 분산 작업 대기열 시스템입니다.
- **Redis**: Celery에서 메시지 브로커로 사용할 수 있는 메모리 내 데이터 저장소입니다.
- **Flower**: Celery를 위한 실시간 웹 기반 모니터링 도구입니다.

## 시작하기

### Celery Worker 시작

```bash
celery -A worker.celery worker --loglevel=info
```

- `celery worker`는 Celery 작업자를 시작하는 데 사용됩니다.
- `-A worker.celery`는 Celery 애플리케이션을 실행합니다.

### 도커 실행

#### Redis 실행 및 확인

```bash
docker run -p 6379:6379 --name some-redis -d redis
docker exec -it some-redis redis-cli ping
```

- Redis 서버를 실행하고 `ping` 명령어로 확인합니다 (`pong` 응답이 오면 정상적으로 동작).

#### 도커 Compose 실행

```bash
cd queue
docker-compose up -d --build
docker-compose exec web python -m pytest
```

- `docker-compose`를 사용하여 모든 서비스를 빌드하고 백그라운드에서 실행합니다.
- `docker-compose exec web python -m pytest`로 테스트를 실행합니다.

## 로그 및 파일 위치

- `/project/logs/celery.log`에서 Celery 로그를 확인할 수 있습니다.
- `/project/static/main.js`에서 `onclick` 이벤트로 `type` 매개변수를 JSON 형식으로 변환하여 전송하는 코드를 확인할 수 있습니다.

## 모니터링

- [Flower](http://localhost:5556/)에서 실시간 모니터링이 가능합니다.
