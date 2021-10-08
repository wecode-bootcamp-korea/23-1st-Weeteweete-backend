 ## 📓 WeeteWeete 프로젝트 소개
 
 ![image](https://user-images.githubusercontent.com/84963683/136541442-e10a989e-e8e1-4a7d-a41a-98091e12cb19.png)

 **Color라는 가치관을 담아내 감각적이고 심플하지만 강력한 구성, 부드러운 필기감을 구현한 모트모트 Motive Project**
 
 2주라는 짧은 프로젝트 기간 내에 개발에 집중해야 하므로 디자인/기획 부분만 클론했습니다.   
 개발은 초기 세팅과 데이터 모델링을 직접 진행하고 실제 MoteMote 사이트의 기능을 대부분 구현했습니다.   
 시연영상에 나오는 부분은 Frontend - Backend간 통신으로 실제 사용할 수 있는 서비스 수준으로 개발했습니다.   

## 개발 인원 및 기간
- [총 프로젝트 기간] : 2021.08.02 ~2021.08.13
- [개발 인원] 
  - Frontend 4명(최호정, 차예은, 배윤아, 이나현)
  - Backend 2명(백선호, 임종성)

## Modeling
![image](https://user-images.githubusercontent.com/84963683/136546044-936b7119-9def-4104-9780-ab4b9efcc540.png)

## 프로젝트 구현 페이지

[시연영상](https://www.youtube.com/watch?v=_oMzIV2oyxE)

## 사용 기술

[Backend] : Python, Django
[DevOps] : Mysql, AWS EC2, RDS, POSTMAN

## 구현 기능

내가 구현한 기능

### Members

- Bcrypt 암호화와 JWT를 이용한 로그인 / 회원가입
- 사용자의 편의를 위한 아이디 찾기 
- UUID 모듈을 활용한 임시비밀번호 생성 
- Login 데코레이터 작성을 통한 인가

### Products

- Main/Menu Page를 하나의 API로 통합
- Query parameter를 활용해 상품 필터링(Category, Option, Concept, Color 등) 
- Django Static Module을 사용해 상품 리뷰 이미지 파일을 Local에 저장
- 상품 상세 정보 확인 API 구현
- 평점과 작성시간을 기준으로 상품 후기를 정렬
### Orders


### 메인 페이지/메뉴 페이지
- 메뉴, 메인 페이지를 하나의 메서드에서 호출
- 메인 페이지 : 판매량 순 상위 8개 상품 정렬
- 메뉴 페이지 : 상품의 category, option, concept, color 별 분류

### 상품 상세 페이지
- 상품의 상세정보와 삼품 후기를 호출

### 상품 후기
- 구매한 사용자만 작성 가능
- 상품 후기 작성 시 form 데이터로 requset & static을 이용한 이미지 파일 저장

### 장바구니
- 사용자의 장바구니 상품의 CRUD

### 상품 구매
- 상품 구매 시 상품의 상태와 주문자의 상태 변화
- 상품 구매 시 구매한 수량만큼의 재고량이 감소, 사용자의 보유 포인트 감소, 상품의 판매수량 증가

# Reference

- 이 프로젝트는 모트모트 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
