# POPPY MAIL proj

> 주의 : local 환경에서는 
>
> 1. `BACKEND/settings/__init__.py`에서 **from .local import ** 로 수정
> 2. `accountapp/views.py`에서 **from BACKEND.settings.local import SECRET_KEY**로 수정
>
> 주의 : 배포 환경에서 superuser 생성하기
>
> 1. (AWS 서버라면) pem key 이용하여 username **ubuntu**로 접속
> 2. 장고 컨테이너에 접속 : **sudo docker exec -it [장고 컨테이너 이름] /bin/bash**
> 3. 배포 환경에서 관리자 생성 : **python manage.py createsuperuser --settings=BACKEND.settings.deploy**

## Description

## IA

## Environment

## Prerequisite

## Usage

## Service imgs

