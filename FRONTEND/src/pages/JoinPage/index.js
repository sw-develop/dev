import React from 'react';
import { Link } from 'react-router-dom';

import * as S from './styles';
import LogoNameJoin from '../../components/Txt/LogoNameJoin';
import BackBtn from '../../components/Btn/BackBtn';

function JoinPage() {

//   if (loading) return <LoadingScreen />;
//   if (error) return <div>에러가 발생했습니다.</div>;
  return (
    <>
      <S.JoinScene>
      <Link to="/">
      <BackBtn></BackBtn>
        </Link>
          
        <LogoNameJoin></LogoNameJoin>
      </S.JoinScene>
    </>
  );
}

export default JoinPage;
