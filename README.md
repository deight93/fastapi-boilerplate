# fastapi-boilerplate

fastapi boilerplate

## 기본 기능

- 기본기능
  - 관리자 # sqladmin 삭제가능
  - 회원
    - 회원 가입
    - 로그인 사용자 정보(내 정보)
  - 인증
    - 로그인
    - 토큰갱신

---

## 팀원 개발 환경 설정 가이드

이 프로젝트는 FastAPI 기반으로 `uv`, `ruff`, `pre-commit`, `pytest` 등을 사용하여 팀원 간 일관된 개발 환경을 구성했습니다.
팀원들은 아래 절차에 따라 로컬 개발 환경을 셋업해주세요.

---

### 초기 셋업

```bash
# uv 설치 (최초 1회)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 가상환경 생성
uv venv

# 프로젝트 환경 동기화 (uv.lock 기반)
uv sync --group dev
# dev 의존성을 설치하지 않으려면 --no-dev 를 추가
uv sync --no-dev
```

> `uv sync`는 `.venv`에 정확히 동일한 패키지 버전을 설치합니다.

---

### VSCode 설정 (권장 IDE)

`.vscode/settings.json`이 다음과 같이 설정되어 있어야 합니다:

```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "none",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": true
  }
}
```

**설치 필요한 확장 프로그램:**
- Python
- Ruff
- Pylance

---

### IntelliJ / PyCharm 설정
1. ruff plugin download

2. **Interpreter 등록**
  - `.venv/bin/python` 경로를 Python Interpreter로 설정

3. **외부 도구로 Ruff 등록**
  - File > Settings > Tools > Ruff

---

### 4️⃣ Pre-commit 설정

```bash
# pre-commit 훅 설치
pre-commit install

# 전체 코드에 훅 수동 실행 (선택)
pre-commit run --all-files
```

`.pre-commit-config.yaml`에 정의된 작업:
- YAML/TOML 문법 검사
- 줄 끝 공백 제거, EOF 개행 유지
- `ruff` lint 및 format 자동 실행

---

### GitHub Actions / GitLab CI

CI에서는 다음 작업이 자동으로 수행됩니다:

| 플랫폼 | 위치 | 작업 내용 |
|--------|------|------------|
| GitHub | `.github/workflows/ci.yaml` | `uv sync`, `ruff`, `pytest` |
| GitLab | `.gitlab-ci.yml` | `uv sync`, `ruff`, `pytest` |

---

### 요약

| 항목 | 해야 할 일 |
|------|-------------|
| 패키지 설치 | `uv sync --group dev` |
| 가상환경 | `uv venv` |
| pre-commit | `pre-commit install` |
| 린트/포맷 | `ruff`, 저장 시 자동 실행 (IDE 설정) |
| 테스트 | `pytest`, CI 자동 실행 |

---

## 환경 설정

이 프로젝트는 환경 변수를 사용하여 설정을 관리합니다.
환경 변수를 설정하려면 프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 변수를 정의해야 합니다.

### env 파일 예시
```
.
├── Dockerfile
├── .env
└── ...
```

`.env`

```plaintext
# 공통 설정
ENV_STATE=dev
JWT_SECRET_KEY=jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=60

# 공통 admin 설정
ADMIN_ID=admin
ADMIN_PASSWORD=admin

# 공통 Redis 설정
REDIS_HOST=redis-db
REDIS_PORT=6379
REDIS_DATABASE=0

# 공통 Postgresql 설정
POSTGRES_HOST=postgresql-db
POSTGRES_PORT=5432

# prod, dev별 설정
# dev 설정
DEV_DEBUG=True
DEV_ALLOWED_ORIGINS=*
DEV_POSTGRES_USER=boilerplate_user
DEV_POSTGRES_PASSWORD=boilerplate
DEV_POSTGRES_DB=boilerplate-dev-db
DEV_REDIS_PASSWORD=dev-redis-password

# prod 설정
PROD_DEBUG=False
PROD_ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000
PROD_POSTGRES_USER=boilerplate_user
PROD_POSTGRES_PASSWORD=boilerplate
PROD_POSTGRES_DB=boilerplate-prod-db
PROD_REDIS_PASSWORD=prod-redis-password
```
