# About PoppyMail📬
![image](https://user-images.githubusercontent.com/69254943/144740777-7991018a-9bd8-41ed-b525-16a32c9527c6.png)

PoppyMail📬은 개개인의 우체통에 다른 사람이 작성한 온라인 편지를 담아 랜덤 날짜에 확인하는 온라인 웹 서비스 입니다.

## 🔗 링크
▶️ [POPPY-MAIL](!https://poppy-mail.vercel.app/)   
▶️ [POPPY Instagram](!https://www.instagram.com/poppy.mail_/?utm_medium=copy_link)

## ✔️ 역할
|이름   |github                   |담당 기능|
|-------|-------------------------|--------------------|
|박세원 |[sw-develop](https://github.com/sw-develop) | 모델링 및 Django ORM을 사용해 MariaDB와 연동, JWT 인증 기반 카카오톡 소셜 로그인 구현, 우체통 CRUD 구현 |


## ✔ ️사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/MariaDB-0064a5?style=for-the-badge&logo=mariadb&logoColor=white"/>&nbsp;
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;


## ✔️ 모델링
<img width="962" alt="image" src="https://user-images.githubusercontent.com/69254943/144753735-96f031c7-a4c8-489e-867b-cdaf09130766.png">

## ✔️ 서버 구성
![architecture](./IMGS/architecture.jpg)

## ✔️ 주요 화면
![description](./IMGS/des1.png) ![description](./IMGS/des2.png)    
![img](./IMGS/img2.png) ![img](./IMGS/img3.png)

## ✔️Prerequisite
- Make a virtual environment

  ```shell
  $ cd BACKEND
  $ python3 -m venv venv
  ```

- Run a virtual environment

  ```shell
  C:\Users\Name\poppy> venv\Scripts\activate
  ```

- Install requirements

  - install requirements

    ```shell
    (venv) ~$ pip install -r requirements.txt
    ```

  - pip upgrade

    ```shell
    (venv) ~$ python3 -m pip install --upgrade pip
    ```

    ​

## ✔️Usage
```
(myvenv) ~/BACKEND$ python manage.py makemigrations
(myvenv) ~/BACKEND$ python manage.py migrate
```

```shell
(myvenv) ~/BACKEND$ python manage.py runserver
```

