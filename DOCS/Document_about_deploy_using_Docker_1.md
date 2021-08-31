# 장고 백엔드 API 서버 구축에 도커 사용하기 1



오류들을 만날 때마다 여기저기 찾아가면서 API 서버를 구축하였다. 계속 삐그덕거리면서 목적지에 도착했기 때문에, 결과를 만들었어도 '내가 뭘 어떻게 한거지?' 혼란스러움이 남아있어 과정을 정리하기 위해 글을 작성한다. 도커 사용 장고 백엔드 구축의 큰 흐름을 기록해두는 것이 목적이어서 각 단계, 단계에서 수행할 **디테일한 명령어에 대한 설명은 하지 않을 것**이다. 혹 잊었을 때, 단위 별 자세한 내용을 서치하는 방식으로 상기하고자 한다. 실용주의 프로그래머님의 유튜브 채널에 자세한 내용이 있다. (현재는 유튜브 영상은 일부만 업로드 되어있고, 인프런에 유료 강의가 있다고 한다.)

> 참고 : [실용주의 프로그래머](https://www.youtube.com/channel/UCmm6VRoi59BUHDPoa3k4VPw/videos)



## 최종 목적

`장고`에 `MariaDB`를 붙여서 프론트엔드와 통신하는 API 서버 만들기



## VPS 구축

지난 프로젝트에서 AWS를 사용해본 적이 있기 때문에 VPS(Virtual Private Server)로 `Vultr`를 택했다. 가격도 좀 더 싼 것 같다. `Vultr`에서 인스턴스를 팔 때, **도커가 설치되어 있는 서버**를 받았다. 인스턴스에 할당 받은

- IP 주소
- PW

이 2가지를 통해 해당 서버에 접속할 수 있다. (`ssh` 이용)



## Docker Hub

### portainer

도커 허브에서 이미 많이 업로드 되어있는 대표적인 Image들을 내려받을 수가 있고, 이를 이용하여 container를 생성할 수 있다. 깨끗한 도커에 가장 먼저 설치한 container는 `portainer`. 해당 컨테이너는 도커를 무려 GUI 환경에서 사용할 수가 있다. 후에 CLI로도 도커를 다루게 된다면 멋있긴 하겠지만, 초심자인 나에게 GUI 환경으로 Docker의 동작을 체험하는 것은 정말 매력적인 경험이다. 물론 포테이너를 설치할 때는 CLI 환경에서 해야하고, 이를 내려받기 위한 명령어가 Docker hub에 잘 안내되어 있다. 9000번 포트를 이용하여 포테이너로 도커를 사용할 수 있도록 명령하여서 내려받았다.

```
158.XXX.XXX.XXX:9000
```

해당 url로 들어가면, 나의 도커에 portainer가 생성된 것을 볼 수 있다.



### NGINX

**동시접속 처리에 특화된 웹 서버 소프트웨어**이다. 내가 생각하는 것보다 훨씬 멋진 놈이었는데, 더 공부하여 이에 대한 내용을 기록해두려고 한다. 역시 도커 허브에서 받아와서 컨테이너를 생성한다.



## (도커 허브에 당연히 없는) 내 개인 장고 컨테이너 생성하기

1. Django 소스코드를 깃헙에 업로드 한 뒤,
2. 이 소스코드를 내려받아 이미지를 build한다는 내용의 `Dockerfile`을 작성
3. 도커파일 이용하여 이미지 빌드 -> 컨테이너 생성

> 수정이 필요한 Dockerfile
>
> ```dockerfile
> FROM python:3.9.0
>
> WORKDIR /home/
>
> RUN git clone https://github.com/(깃헙 레포지토리)
>
> WORKDIR /home/(pj directory)
>
> RUN pip install -r requirements.txt
>
> RUN echo "SECRET_KEY=(~~~)" > .env
>
> RUN python manage.py migrate
>
> EXPOSE 8000 # 해당 포트를 사용할 수 있도록 노출
>
> CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
> ```
>
> 

도커파일로 `django_test_image:1` 이미지를 만들고, 이 이미지를 이용해서 django_container를 만든다. 이 때, 

```
host:8000 -> container:8000
```

포트가 연결되도록 설정한다.  

```
158.XXX.XXX.XXX:8000
```

으로 접속하면, 로컬에서 Django로 개발한 내용이 정상적으로 나오게 됨.

하지만,

배포환경에서 사용하면 안되는 장고의 `runserver` 명령을 Dockerfile에서 사용하고 있기 때문에, 이에 대한 처리를 해줘야 한다. 공식문서에서 다음과 같이 배포 환경에서 `runserver` 명령을 사용하지 말라고 이야기하고 있다.

> DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making Web frameworks, not Web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)

이 문제를 어떻게 해결할까?

