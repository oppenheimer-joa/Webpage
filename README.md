# Webpage
Django 기반의 슬문생 웹 서비스 페이지입니다.

## 2023.09.19

### 구현기능
- 회원 가입, 로그인, 로그아웃 및 관리자 기능
- 영화 데이터 검색 기능 : 영화 제목 / 영화 인물
- 영화 데이터 조회 기능 : 영화 상세정보 / 박스 오피스 순위 / 영화제
- 공연 데이터 검색 기능 : 공연 제목
- 공연 데이터 조회 기능 : 공연 상세정보
- 고객 센터 이메일 문의 기능

### 서버정보
- Framework : Django
- IP : 43.202.116.246
- Port : 9000

### Endpoint
- 메인
   * 시작 화면 : /
   * 로그인 화면 : /login
   * 회원가입 화면 : /signup
   * 메인 화면 : /main
- 영화
   * 영화 메인 화면 : /dir
   * 영화 목록 조회 화면 : /movie
   * 영화 상세정보 조회 화면 : /movie/{영화_id}
   * 박스오피스 화면 : /boxoffice
   * 영화제 목록 조회 화면 : /awards
   * 영화제 상세정보 조회 화면 : /awards/{영화제명}/{연도}
- 공연
   * 공연 목록 조회 화면 : /prf
   * 공연 상세정보 조회 화면 : /prf/{공연_id}
- 기타
   * 가이드 문서 : /document
   * 고객 지원 : /help
   * 고객 상담 : /help/inq
   * FAQ : /help/faq
   * Q&A: /help/qna
   * 소개 : /about
   * 개요 : /about/outline
   * 팀 소개 : /about/team
   * 패치노트 : /about/release
   * API : /about/api
