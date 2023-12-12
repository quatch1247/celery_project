2023/12/12 celery 예제 실행 및 정리

poetry(requirements.txt 관리)
sed -i '' '/--hash/d' requirements.txt
sed -i '' 's/ *; python_version.*$//' requirements.txt
cat requirements.txt | xargs -n 1 poetry add

##CELERY

큐 관리는 비동기 작업을 처리하는 분산 시스템의 중요한 요소이다.
Celery, FastAPI, Redis, Flower를 통해 대기열 문제를 처리하는 예제이다.

Celery : 작업을 비동기적으로 실행할 수 있는 오픈 소스 분산 작업 대기열 시스템이다.
Redis : Celery에서 메세지 브로커로 사용할 수 있는 메모리 내 데이터 저장소이다.
Flower : Celert를 위한 실시간 웹 기반 모니터링 도구

celery A worker.celery worker --loglevel=info
- celery worker은 celery 작업자를 시작하는데 사용
- -A worker.celery Celery 애플리케이션 실행

도커 실행

Redis 확인(pong)
docker run -p 6379:6379 --name some-redis -d redis 
docker exec -it some-redis redis-cli ping       


도커 compose
cd queue
docker-compose up -d --build
docker-compose exec web python -m pytest

/project/logs/celery.log 에서 로그 확인
/project/static/main.js 를 보면 온클릭 이벤트로 type 매개변수를 JSON 형식으로 변환하여 전송
http://localhost:5556/ flowr에서 실시간 모니터링 가능