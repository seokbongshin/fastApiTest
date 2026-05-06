# fastApiTest

Python 3.12 기반 FastAPI 기본 프로젝트 구조입니다.

## 프로젝트 구조

```text
.
├── app
│   ├── api
│   │   ├── router.py
│   │   └── v1/endpoints/sample.py
│   ├── core
│   └── main.py
├── tests
│   └── test_health.py
├── .python-version
└── pyproject.toml
```

## 시작하기

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## 확인용 엔드포인트

- `GET /health`
- `GET /api/v1/hello`
- `GET /api/v1/calculate?left=10&right=2`

## API Authentication

`/api/v1` endpoints require a JWT bearer token.

```bash
curl "http://127.0.0.1:8000/api/v1/calculate?left=10&right=2" \
  -H "Authorization: Bearer <jwt-token>"
```

Set `JWT_SECRET_KEY` in the environment to validate tokens with a custom secret.
