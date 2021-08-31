# 장고 백엔드 API 서버 구축에 도커 사용하기 4

> 참고 : [실용주의 프로그래머](https://www.youtube.com/channel/UCmm6VRoi59BUHDPoa3k4VPw/videos)



지금 설정한 내용들을 커맨드 파일 형태로 만들어서 기록해 두고, 그 파일만 실행해준다면! 컨테이너를 손쉽게 생성할 수 있고 관리하기도 수월해진다. -> **yml 파일**!



## Docker STACK

yml 파일을 작성하면서, 위에서 언급한 반복적인 설정 작업을 없애는 기능에 더해 automatic reboot 기능을 하도록 파일에 적어준다. 그러기 위해선 도커로 구현한 컨테이너들을 **서비스(Service)**로 격상 시킨다. 서비스로 격상시키게 되면, 

1. Automatic REBOOT
2. Container의 자유로운 생성

이 가능하게 된다.

이러한 STACK을 어디에서 어떻게 굴리게 될까?



## Docker Swarm

**도커시스템을 포함하고 있는 가상서버 하나** 이 덩어리를 **Node**라고 한다. 이 노드들을 마치 하나의 서버인 것처럼 이용할 수 있게 묶어주는 것이 **Docker Swarm**이다. 물론, 이 프로젝트에서 구축하고자 하는 노드의 개수는 1개이다. 도커 swarm을 켜주어야 하는데, 불행히도 현재시점에서 **portainer**에서 구동할 수 없어서, CLI 환경으로 서버에 접속하여 도커 swarm을 명령한다.

```
docker swarm init
```



## Docker Secrets

장고 SECRET_KEY라든가 maria db 설정에서 필요한 MYSQL_ROOT_PASSWORD을 도커 시스템 내부에서 관리하게 할 수 있다. 도커 내부 어떤 경로(run/secrets/)에 저장된 secret 내용들을 이를 필요로 하는 서비스들에게 제공하게 하는 것이다. marial db에 _FILE이라는 접미사가 붙은 환경변수만 제공하는 방식으로 (예 : MYSQL_PASSWORD_FILE) secret 내용들을 전달할 수 있다.

settings/deploy.py 에서 원래는 .env 파일에서 읽어왔던 secret 내용을 도커 시크릿에서 읽어올 수 있도록 파일을 수정해야 한다.



### 최종 yml 파일

```yaml
version: "3.7"
services:
  ngnix:
    image: nginx:1.19.5
    volumes:
      - /home/(서비스 dir)/nginx.conf:/etc/nginx/nginx.conf
    networks:
      - network
    ports:
      - 80:80

  django_container_gunicorn:
    image: django_test_image:6
    networks:
      - network
    secrets:
      - MYSQL_PASSWORD
      - DJANGO_SECRET_KEY

  mariadb:
    image: mariadb:10.5
    networks:
      - network
    volumes:
      - maria-database:/var/lib/mysql
    secrets:
      - MYSQL_PASSWORD
      - MYSQL_ROOT_PASSWORD
    environment:
      MYSQL_DATABASE: (DB 이름)
      MYSQL_USER: (사용자 이름)
      MYSQL_PASSWORD_FILE: /run/secrets/MYSQL_PASSWORD
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/MYSQL_ROOT_PASSWORD

networks:
  network:

volumes:
  static-volume:
  media-volume:
  maria-database:

secrets:
  DJANGO_SECRET_KEY:
    external: true
  MYSQL_PASSWORD:
    external: true
  MYSQL_ROOT_PASSWORD:
    external: true

```



해당 프로젝트에서는 Nginx conf 에 최소한의 설정만 적용하여, 배포를 하였는데, 좀 더 공부하여 새로운 것을 적용할 것이다! (프론트를 같이 붙인다거나)