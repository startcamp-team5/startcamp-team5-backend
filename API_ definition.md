LocalHub API 명세서
================

**프로젝트:** LocalHub (구미/경북)  
**기술스택:** Vue.js + FastAPI + SQLite  
**Base URL:** `/api`  
**인증:** 없음 (익명 커뮤니티)

* * *

1\. 공통 응답 형식
============

성공
--

    {
      "success": true,
      "message": "요청이 성공했습니다.",
      "data": {}
    }

실패
--

    {
      "success": false,
      "message": "오류가 발생했습니다.",
      "errorCode": "ERROR_CODE"
    }

* * *

2\. 지역 정보 API
=============

* * *

2-1. 지역정보 목록 조회
---------------

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URI | `/api/locations` |
| 설명 | 구미/경북 관광지·맛집 목록 조회 |

### Request

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| category | String | 관광지/맛집 |
| keyword | String | 검색어 |

예시: `/api/locations?category=TOURIST&keyword=금오산`

### Response

    {
      "success": true,
      "data": [
        {
          "locationId":1,
          "name":"금오산",
          "category":"TOURIST",
          "latitude":36.11,
          "longitude":128.30
        }
      ]
    }

* * *

2-2. 지역정보 상세조회
--------------

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URI | `/api/locations/{external_Id}` |

### Request

- Path Parameter
  - `externalId`: String (외부 지역 식별자)

예시: `/api/locations/126016`

* * *

2-3. 지도 데이터 조회
--------------

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URI | `/api/locations/map` |

지도 마커 출력용 좌표 조회

### Request

- 요청 본문은 없으며, 지도 마커용 전체 좌표를 조회합니다.

예시: `/api/locations/map`

* * *

3\. 커뮤니티 게시글 API
================

* * *

3-1. 게시글 목록 조회
--------------

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URI | `/api/posts` |

### Request

| 이름 | 설명 |
| --- | --- |
| category | 게시판 종류 |
| keyword | 검색 |
| page | 페이지 |

예시: `/api/posts?category=REVIEW&keyword=금오산&page=1`

* * *

3-2. 게시글 상세 조회
--------------

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URI | `/api/posts/{postId}` |

### Request

- Path Parameter
  - `postId`: Integer (게시글 ID)

예시: `/api/posts/10`

### Response

    {
      "success":true,
      "data":{
          "postId":10,
          "locationId":1,
          "title":"금오산 후기",
          "content":"정말 좋았습니다.",
          "authorName":"익명",
          "viewCount":13
      }
    }

* * *

3-3. 게시글 작성
-----------

| 항목 | 내용 |
| --- | --- |
| Method | POST |
| URI | `/api/posts` |

### Request

    {
        "locationId":1,
        "category":"REVIEW",
        "title":"금오산 후기",
        "content":"등산하기 좋아요.",
        "authorName":"익명",
        "editPassword":"1234"
    }

### Response

    {
        "success":true,
        "message":"게시글이 등록되었습니다.",
        "data":{
            "postId":10
        }
    }

* * *

3-4. 게시글 수정
-----------

| 항목 | 내용 |
| --- | --- |
| Method | PUT |
| URI | `/api/posts/{postId}` |

### Request

    {
        "title":"수정된 제목",
        "content":"수정된 내용",
        "editPassword":"1234"
    }

### Response

    {
        "success":true,
        "message":"게시글이 수정되었습니다."
    }

* * *

3-5. 게시글 삭제
-----------

| 항목 | 내용 |
| --- | --- |
| Method | DELETE |
| URI | `/api/posts/{postId}` |

### Request

    {
        "editPassword":"1234"
    }

### Response

    {
        "success":true,
        "message":"게시글이 삭제되었습니다."
    }

* * *

4\. 댓글 API
==========

* * *

4-1. 댓글 조회
----------

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URI | `/api/posts/{postId}/comments` |

### Request

- Path Parameter
  - `postId`: Integer (게시글 ID)

예시: `/api/posts/10/comments`

* * *

4-2. 댓글 작성
----------

| 항목 | 내용 |
| --- | --- |
| Method | POST |
| URI | `/api/posts/{postId}/comments` |

### Request

    {
        "content":"좋은 정보 감사합니다.",
        "authorName":"익명",
        "editPassword":"1234"
    }

* * *

4-3. 댓글 수정
----------

| 항목 | 내용 |
| --- | --- |
| Method | PUT |
| URI | `/api/comments/{commentId}` |

### Request

    {
        "content":"수정된 댓글",
        "editPassword":"1234"
    }

* * *

4-4. 댓글 삭제
----------

| 항목 | 내용 |
| --- | --- |
| Method | DELETE |
| URI | `/api/comments/{commentId}` |

### Request

    {
        "editPassword":"1234"
    }

* * *

5\. 챗봇 API
==========

* * *

5-1. 챗봇 질의
----------

| 항목 | 내용 |
| --- | --- |
| Method | POST |
| URI | `/api/chat` |
| 설명 | 관광지·맛집·게시글 기반 AI 답변 생성 |

### Request

    {
        "message":"구미에서 가볼 만한 관광지를 추천해줘."
    }

### Response

    {
        "success":true,
        "data":{
            "answer":"금오산도립공원을 추천드립니다."
        }
    }

* * *

6\. 소셜 공유 (Frontend)
====================

Web Share API를 사용하므로 별도의 백엔드 API는 구현하지 않습니다.

공유 URL 예시

    /locations/{locationId}
    
    /posts/{postId}

* * *

API 목록
======

| 구분 | Method | URI | 설명 |
| --- | --- | --- | --- |
| 지역정보 | GET | `/api/locations` | 지역정보 목록 조회 |
| 지역정보 | GET | `/api/locations/{external_Id}` | 지역정보 상세 조회 |
| 지도 | GET | `/api/locations/map` | 지도 마커 조회 |
| 게시글 | GET | `/api/posts` | 게시글 목록 조회 |
| 게시글 | GET | `/api/posts/{postId}` | 게시글 상세 조회 |
| 게시글 | POST | `/api/posts` | 게시글 작성 |
| 게시글 | PUT | `/api/posts/{postId}` | 게시글 수정 |
| 게시글 | DELETE | `/api/posts/{postId}` | 게시글 삭제 |
| 댓글 | GET | `/api/posts/{postId}/comments` | 댓글 조회 |
| 댓글 | POST | `/api/posts/{postId}/comments` | 댓글 작성 |
| 댓글 | PUT | `/api/comments/{commentId}` | 댓글 수정 |
| 댓글 | DELETE | `/api/comments/{commentId}` | 댓글 삭제 |
| 챗봇 | POST | `/api/chat` | AI 챗봇 질의응답 |

### 변경 사항

*   **게시글 PK**: `postId`
*   **지역정보 PK**: `locationId`
*   **댓글 PK**: `commentId`

처럼 각 엔티티의 PK를 명확하게 구분하여 API와 DB 스키마의 일관성을 유지했습니다.