FROM python:3.9.0

WORKDIR /home/

# 한국 시간으로 설정
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

# 도커가 (혹은 portainer가) build시 속도를 위해 cache를 해서,
# 장고에서 수정 후 다시 build할 때, cache하지 않도록
# 아래의 명령어를 바꿔가면서 (ex) testing!으로 했다가, test!!로 했다가 등등) build
RUN echo "~!~!~!TEST!!!"

RUN git clone -b be --single-branch https://github.com/POPPY-MAIL/dev.git

WORKDIR /home/dev/BACKEND/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --settings=BACKEND.settings.deploy --no-input && python manage.py migrate --settings=BACKEND.settings.deploy && gunicorn BACKEND.wsgi --env DJANGO_SETTINGS_MODULE=BACKEND.settings.deploy --bind 0.0.0.0:8000"]

# superuser 만드는 법
# pemkey 가지고 ubuntu 접속
# 장고 컨테이너에 접속 : sudo docker exec -it [컨테이너 이름] /bin/bash
# 관리자 생성 : python manage.py createsuperuser --settings=BACKEND.settings.deploy
