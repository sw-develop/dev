import './App.css';

// images
import poppyImg from './image/poppy.png'
import backbtnImg from './image/back-btn.png'

function App() {
  return (
    <div className="App">
      <div className="full">
        <div className="welcome-screen">
          {/* <div className="back-btn"><img src={backbtnImg}></img></div> */}
          <div className="logo-name">파피메일</div>
          <div className="poppy">
            <img src={poppyImg}></img>
          </div>
          <div className="welcome-ment">
            오 안녕하세요? <br></br>반갑습니다!
          </div>
          <div className="login-btn">
            로그인
          </div>
          <div className="join-btn">
            회원가입하기
          </div>
          <div className="join-btn-deco1">
          </div>
          <div className="join-btn-deco2"></div>
        </div>
      </div>
    </div>
  );
}

export default App;
