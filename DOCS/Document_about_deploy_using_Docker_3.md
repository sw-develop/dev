# 장고 백엔드 API 서버 구축에 도커 사용하기 3



> 관련 링크 : [실용주의 프로그래머](https://www.youtube.com/channel/UCmm6VRoi59BUHDPoa3k4VPw/videos)



## MariaDB

### settings.py 수정

Django `settings.py`에서 mariadb를 사용하는 배포용 환경을 따로 설정해준다. settings.py가 있던 자리에 settings라는 디렉토리를 두고, 그 안에 `base.py` `local.py` `deploy.py` 3개의 파일로 나누어 관리한다.

```
settings
	- base.py
	- local.py
	- deploy.py
```

 폴더구조가 바뀌었으므로 BASE_DIR을 좀 만져줘야되고, deploy 파일에서 DATABASES를 mariadb에 맞게 ENGINE, NAME 등을 설정해줘야 한다. settings.py를 수정하였고, mairadb가 장고 컨테이너에 붙어야하니 Dockerfile을 다시 작성하여 장고 컨테이너를 생성한다.

```dockerfile
FROM python:3.9.0

WORKDIR /home/

RUN echo "testing!"  # cache에서 불러오는 것을 막고 모두 새로 build 될 수 있도록

RUN git clone -b be --single-branch https://github.com/(깃헙 디렉토리).git

WORKDIR /home/(깃헙 디렉토리)/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --settings=BACKEND.settings.deploy && gunicorn BACKEND.wsgi --env DJANGO_SETTINGS_MODULE=BACKEND.settings.deploy --bind 0.0.0.0:8000"]

```



### 컨테이너 생성

1. 네트워크 설정:

   `nginx_django`로 설정

2. Volume 설정:

   `database` 라는 이름의 Named volume을 만든다.

   설정 경로는 공식문서에 나와있다. (/var/lib/mysql)

3. Env 환경 변수 설정

   MYSQL_ROOT_PASSWORD

   MYSQL_DATABASE

   MYSQL_USER

   MYSQL_PASSWORD



이로써 nginx_django 네트워크에 mariadb가 붙은 장고 컨테이너가 들어가게 된다! 하지만, 컨테이너들을 배포할 때마다 이 많은 작업들을 반복적으로 수행해주어야 하는걸까?..
