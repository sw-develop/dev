import React from 'react';
import { Link } from 'react-router-dom';

import * as S from './styles';
import LogoNameLogin from '../../components/Txt/LogoNameLogin';
import BackBtn from '../../components/Btn/BackBtn';
import LoginMent from '../../components/Txt/LoginMent';
import LoginBtn from '../../components/Btn/LoginBtn';
import JoinBtn from '../../components/Btn/JoinBtn';

function LogInPage() {

    //   if (loading) return <LoadingScreen />;
    //   if (error) return <div>에러가 발생했습니다.</div>;
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
            </S.LogInScene>
        </>
    );
}

export default LogInPage;
