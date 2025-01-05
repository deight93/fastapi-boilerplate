# fastapi-boilerplate

fastapi boilerplate

## TODO 기능

- 기본기능
  - 회원
    - ~~회원 가입~~
    - 로그인/로그아웃
    - 회원 정보 확인
    - 회원 정보 수정
    - 회원 탈퇴
  - 게시판
    - 게시판 목록
    - 게시글 작성
    - 게시글 수정
    - 게시글 상세
    - 게시글 삭제
    - 파일 업로드
    - 파일 다운로드
  - 관리자페이지
    - 회원 관리
      - 회원 목록 조회
      - 회원 정보 수정
      - 회원 삭제
      - 회원 권한 설정
    - 게시판 관리
      - 게시판 생성 및 수정
      - 게시글 관리 (수정, 삭제)
      - 게시글 신고 처리
    - 권한 관리
      - 관리자 계정 생성 및 수정
      - 관리자 권한 설정
    - 로그 관리
      - 시스템 로그 조회
      - 활동 로그 조회
    - 파일 관리
      - 업로드된 파일 관리
      - 파일 삭제


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
ALGORITHM=jwt-algorithm # HS256, HS512, ...

# admin
ADMIN_ID=boilerplate_user
ADMIN_PASSWORD=boilerplate

# postgresql
POSTGRES_USER=boilerplate_user
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=postgresql-db
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
SECRET_KEY=secret-key # HS256, HS512, ...
ALGORITHM=jwt-algorithm

# admin
ADMIN_ID=boilerplate_user
ADMIN_PASSWORD=boilerplate

# postgresql
POSTGRES_USER=boilerplate_user
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=postgresql-db
POSTGRES_PORT=5432
POSTGRES_DB=boilerplate-prod-db

# redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DATABASE=0
```
