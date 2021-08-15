import React from 'react';
import { Link, useHistory } from 'react-router-dom';

import * as S from './styles';
import LogoNameLogin from '../../components/Txt/LogoNameLogin';
import BackBtn from '../../components/Btn/BackBtn';
import LoginMent from '../../components/Txt/LoginMent';
import LoginBtn from '../../components/Btn/LoginBtn';
import JoinBtn from '../../components/Btn/JoinBtn';
import KakaoLogin from 'react-kakao-login';

const { Kakao } = window;

function LogInPage() {

    const history = useHistory()
    // const KakaoLoginClickHandler = () => {
    //     Kakao.Auth.login({
    //         success: function (authObj) {
    //             fetch(`${'요청보낼 벡엔드 서버 url'}`, {
    //                 method: "POST",
    //                 body: JSON.stringify({
    //                     access_token: authObj.access_token,
    //                 }),
    //             })

    //             .then(res => res.json())
    //             .then(res => {
    //                 localStorage.setItem("Kakao_token", res.access_token);
    //                 if (res.access_token) {
    //                     alert("poppy mail에 오신 것을 환영합니다!")
    //                     history.push("/login");
    //                 }
    //             })
    //         },
    //         fail: function(error) {
    //             alert(JSON.stringify(error))
    //         },
    //     })
    // }

    const KakaoLoginClickHandler = () => {
        Kakao.Auth.login({
            success: function (response) {
                console.log(response);
            },
            fail: function(error) {
                alert(JSON.stringify(error))
            },
        })
    }
    
    return (
        <>
            <S.LogInScene>
                <Link to="/">
                    <BackBtn></BackBtn>
                </Link>

                <LogoNameLogin></LogoNameLogin>
                <LoginMent></LoginMent>
                <Link to="/howto">
                    <LoginBtn></LoginBtn>
                </Link>

                <Link to="/join">
                    <JoinBtn></JoinBtn>
                </Link>

                <S.KakaoBtn fill className="btn kakao" onClick={KakaoLoginClickHandler}/>
            </S.LogInScene>
        </>
    );
}

export default LogInPage;
