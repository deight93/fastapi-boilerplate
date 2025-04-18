# fastapi-boilerplate

fastapi boilerplate

## TODO 기능

- 기본기능
  - 회원
    - ~~회원 가입~~
    - 로그인 사용자 정보(내 정보)
  - 인증
    - 로그인
    - 로그아웃
    - 토큰갱신


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
