# Django_Musicblog

Django framework 학습을 위한 간단한 음악 블로그입니다.  
Django MTV (Model, Template, View) 기본 원칙에 따라 프로젝트를 진행했으며,  
Model로는 Django 기본 ORM 모듈을 사용하여 SQLite3와 연동했으며,  
Template은 Django Templete 문법을 활용해 HTML 페이지 생성 및 렌더링을 하는 방식입니다.  

## Model 구조

- Artist
  - name
  - slug (url 만들 때에 쓰임. 공백을 '-'로 바꾼다던가...)
  - company (소속 회사)
  - debut (데뷔 일자)
  - artist_info (상세 정보)
- Member -> 아티스트가 그룹인 경우 소속 멤버
  - name
  - slug
  - team (소속 그룹, 팀, Foreign Key)
- Album
  - title
  - slug
  - artist (아티스트, Foreign Key)
  - on_sale (발매 일자)
- Track
  - title
  - slug
  - artist (아티스트, Foreign Key)
  - album (앨범, Foreign Key)
  - is_titlesong (타이틀곡 여부 -> Boolean)
  - youtube_id (youtube 영상 id)
  - lyrics

## 주요 기능
- 아티스트, 앨범 등 컨텐츠 목록 조회
- 컨텐츠 세부 정보 확인
- 트랙 유튜브 영상 조회
- 신규 컨텐츠 등록