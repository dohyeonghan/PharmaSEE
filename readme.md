## [task list]
reminder API <br> 
pill API o<br> 
회원가입 API o<br> 
JWT 토큰 o<br> 
보호자 피보호자 연결 API<br>

## app 단위 개발
### nugu proxy, 배포(다영)
+ nugu views.py
    + backend proxy 연결 과정(6단계)
        + 누구 디바이스와 유저 연결 인증(todo)
### API 구현, 인증 허가(도형)
+ [API]
    + accounts 
      + User
        + model : abstractuser로 불러오기 -> 보호자, 피보호자
        + serializer : signup serializer 
        + url : 
          + accounts/signup
          + accounts/follow
          + accounts/unfollow
    + pharmasee
        + model : pill, reminder 
        + serializer : pillserializer, reminderserializer
        + url : router 사용 -> api/pills, api/reminders
        + view : modelviewset 사용 
+ [검색기능]
  + user 검색 -> 보호자 
  + pill 검색 -> 증상(효과)

+ [url 정리](1차)
    + accounts/signup : 로그인
    + accounts/follow : 팔로우셋에 저장
    + accounts/unfollow : 언팔로우
    + accounts/search : 유저검색
    + pharmasee/api/pills : pill 데이터
    + pharmasee/api/reminder : reminder 데이터
    + pharmasee/search : 약통 검색



### 머신러닝 모델, UI (경환)
배포(미정)<br>
도커 vs VM<br>

[폴더 구조] <br>
backend - config <br>
accounts - custom user signup, login, create ...<br>
pharmasee - pill register, create reminder... <br> 


