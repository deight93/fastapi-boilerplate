# fastapi-boilerplate

fastapi boilerplate

## 기능

JWT, Session, OAuth 인증
백오피스
클라이언트
파일 업로드

## 환경 설정

이 프로젝트는 환경 변수를 사용하여 설정을 관리합니다. 환경 변수를 설정하려면 프로젝트 루트 디렉토리의 env디렉토리에 `base.env`, `dev.env`, `prod.env` 파일을 생성하고 필요한 변수를 정의해야 합니다.

### env 파일 예시

```
.
├── Dockerfile
├── ...
├── env
│   ├── base.env
│   ├── dev.env
│   └── prod.env
└── ...
```

`base.env` 

```plaintext
# dev, prod
ENV_STATE=dev
```

`dev.env` 

```plaintext
APP_ENV=dev
DEBUG=True
ALLOWED_ORIGINS=*
SECRET_KEY=secret-key
ALGORITHM=jwt-algorithm

# admin
ADMIN_ID=boilerplate_user
ADMIN_PASSWORD=boilerplate

# postgresql
POSTGRES_USER=boilerplate_user
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=boilerplate-dev-db

# redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DATABASE=0
```

`prod.env` 

```plaintext
APP_ENV=prod
DEBUG=False
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000
SECRET_KEY=secret-key
ALGORITHM=jwt-algorithm

# admin
ADMIN_ID=boilerplate_user
ADMIN_PASSWORD=boilerplate

# postgresql
POSTGRES_USER=boilerplate_user
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=boilerplate-prod-db

# redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DATABASE=0
```