# Django 프로젝트 실무형 초기 설정 (Windows 기준)

---

## 1. 가상환경 생성 및 패키지 설치 (CMD 또는 PowerShell)

```cmd
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install django djangorestframework python-decouple
pip freeze > requirements.txt
```

---

## 2. 현재 폴더 기준 프로젝트 생성

```cmd
django-admin startproject config .
```

- `config`는 설정용 폴더 이름으로 많이 사용

---

## 3. 앱 생성

```cmd
python manage.py startapp member
```

---

## 4. settings.py에서 환경변수 로딩 (.env)

- `.env` 파일 예시:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

- settings.py 예시:
```python
from decouple import config

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")
```

---

## 5. 앱 등록

```python
INSTALLED_APPS = [
    'member',
    'rest_framework',
    'django.contrib.admin',
    ...
]
```

---

## 6. 커스텀 사용자 모델 생성

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
```

- settings.py에 추가:
```python
AUTH_USER_MODEL = 'member.User'
```

---

## 7. 마이그레이션 및 슈퍼유저 생성

```cmd
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 8. 관리자(admin) 등록

```python
from django.contrib import admin
from .models import User

admin.site.register(User)
```

---

## 9. URL 연결

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('member/', include('member.urls')),
]
```

---

## 10. 폴더 구조 예시

```
myproject/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── member/
│   ├── models.py
│   └── views.py
├── templates/
├── static/
├── .env
└── requirements.txt
```

---

## 추가 실무 팁

- `.env` 파일을 Git에 커밋하지 않도록 `.gitignore`에 추가
- `DEBUG=False`로 배포 시에는 `ALLOWED_HOSTS`를 정확히 설정