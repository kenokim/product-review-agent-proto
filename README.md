# 제품 추천 플랫폼 (Product Review Agent)

![제품 추천 플랫폼](screenshot.png)

## docker compose
- GEMINI_API_KEY="<YOUR_GEMINI_API_KEY>" docker-compose up --build

## 기능 개요
- 사용자가 구체적인 제품 검색 요청을 할 경우 웹 검색 결과를 출처와 함께 응답한다.
- 구체적이지 않을 경우 구체화를 요구한다.`

## 평가 (eval)

### 테스트 개요
- 테스트 케이스: 30개
- 성공률: 29/30 (human eval)

```json
"test_results": [
    {
      "test_id": 1,
      "query": "10만원 이하 가성비 좋은 무선 이어폰 추천해줘",
      "response": "10만원 이하 가성비 좋은 무선 이어폰으로 다음 제품들을 추천합니다.\n\n*   **QCY 멜로버즈 프로/프로 플러스 ANC**\n    *   **가격대:** 3만원 ~ 5만원 이하\n    *   **주요 특징:** 액티브 노이즈 캔슬링(ANC), 전용 앱 지원, 프로 플러스 HT08 모델은 LDAC 코덱 및 Hi-Res 인증 지원.\n    *   **추천 이유:** 가격 대비 뛰어난 노이즈 캔슬링 성능과 준수한 음질 및 통화 품질을 제공하여 가성비가 매우 좋습니다.\n    *   **출처:** [[1], [2], [5]], [구스픽스](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhgeP7NIcxKGeYbh_04RRVCD0Y5vum7NumEjZhNm3l0TO2yZ2-fhzuo10-UsmHbdjXkeWW5ZUh70ORTEhTCECQtTK3VsfEGufPguV Ajjq9zTaO6_oUM6k8UMaT1o_mUHUD_-qPSXC_rgU-OIh-d7NL7l5496e-D-tls1UYL_0aePBIwNWzai7IUorCIXoNLEikNf7Qs6HXpjvbHmHCZI275V48s7GZ81j1DgoD2fDORMnt6F9vPswMObkZtr3ZpJ-GZJfyg5DyNpEnzx_m1D_UX-UBTQ5DB8xMXU0EeG5qhnjAgHpIiWSrjzlNvra2hxnQ0TsY_ew4sVvWgP-ubI0=), [골사투 - 티스토리](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHex30H-k3pMBVm4jXmixlrWWuVHmylAsEmyenpFYtf3BLUlovCauHaytJS6-wsk68CIqgbq0p53mnAXMI77M5vKDVYhGik2WmDbd15csfzWKNboGDDBjorc0w=)\n    *   **구매 링크:** [https://link.coupang.com/a/b34ZA4](https://link.coupang.com/a/b34ZA4)\n\n*   **앤커 사운드코어 리버티 4 NC**\n    *   **가격대:** 8만원 ~ 11만원 (행사 시 10만원 이하 구매 가능성 있음)\n    *   **주요 특징:** 전용 앱 지원, 맞춤형 사운드(HearID 기능), 6채널 마이크 시스템.\n    *   **추천 이유:** 균형 잡힌 성능과 개선된 통화 품질을 제공하며, ANC 및 투명 모드 등 다양한 기능을 지원합니다.\n    *   **출처:** [[1], [2], [4]], [구스픽스](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhgeP7NIcxKGeYbh_04RRVCD0Y5vum7NumEjZhNm3l0TO2yZ2-fhzuo10-UsmHbdjXkeWW5ZUh70ORTEhTCECQtTK3VsfEGufPguV Ajjq9zTaO6_oUM6k8UMaT1o_mUHUD_-qPSXC_rgU-OIh-d7NL7l5496e-D-tls1UYL_0aePBIwNWzai7IUorCIXoNLEikNf7Qs6HXpjvbHmHCZI275V48s7GZ81j1DgoD2fDORMnt6F9vPswMObkZtr3ZpJ-GZJfyg5DyNpEnzx_m1D_UX-UBTQ5DB8xMXU0EeG5qhnjAgHpIiWSrjzlNvra2hxnQ0TsY_ew4sVvWgP-ubI0=)\n\n*   **삼성 갤럭시 버즈 FE**\n    *   **가격대:** 5만원대 (최저가 기준)\n    *   **주요 특징:** 삼성 기기와의 뛰어난 호환성.\n    *   **추천 이유:** 삼성 기기 사용자에게 최적화된 사용 경험을 제공하며, 가격 대비 무난한 성능을 보여줍니다.\n    *   **출처:** [[8], [14], [19]], [예하 (YouTube)](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5JgAiEIwtDwONhKKvixi_1fkStozdSqcJ9Ywb7ZsfecxBClHfsstFkUV29Jw5TVGMUn1mYKqNkI47noWCCSTtqT_R4hVYd6aaVwRS-9qj0K_-nNq58zNAYCTVWjZ1mLkWvPNTIHg=)\n\n*   **QCY T13**\n    *   **가격대:** 2만원대\n    *   **주요 특징:** 블루투스 5.3, 최대 40시간 재생(케이스 포함), EQ 앱 지원.\n    *   **추천 이유:** 매우 뛰어난 가성비를 자랑하며, 앱 연동을 통한 EQ 조절이 가능하여 입문용 또는 서브 이어폰으로 적합합니다.\n    *   **출처:** [[3], [8]], [골사투 - 티스토리](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHS4l_oMY9RXjeyDVSIbGfyXYsgVI910Yo098MwvLEDjj-AZx_doA8w2rZHlYL4aj9v2yyIRd2o5glroCGpxaLtmsrIjkunIy6G-JgvE-ILskPxOVXRiPSL7Aih)\n\n*   **1MORE Q20K**\n    *   **가격대:** 4만원대 후반\n    *   **주요 특징:** 자연스러운 저음과 튀지 않는 고음, 우수한 착용감, 깔끔한 무광 화이트 디자인.\n    *   **추천 이유:** 전체적인 음질 밸런스가 뛰어나며, 불필요한 기능 없이 핵심에 집중한 제품입니다.\n    *   **출처:** [구스픽스](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE6Bkdo3Wd43x5kofNosuUVw7WkkuZgsr0uAb_0D-gN7rqDhb1uy-BuikVVle4R2o88VIuQKgwawWyoP7mi2-Rp0uRQLx4P9tjohDOR7NG2Vjq7eGBLOwKCs51D4-yF5UB65_IHiaMetykfjLXckjGqhjoMGwEixqaEQIM1Q371vgiYKd7mNortITg9_ptsbrLqj1FEbGXib_iB8B9z3YxGzzGELMS2TAm9CHt315xcTx5R3VkbliGhcj_YUqfGsE2ISgHJTVbz3zCMMYp5ryHuPgUs-pAGnwynXACKCSsYxMkH50q_RyuvyIOOuhHCSl0X3vI6jM41flRzzvuYgVJk)",
      "sources": [],
      "response_time_ms": 55740.72,
      "status_code": 200,
      "timestamp": "2025-06-26T05:01:41.309395",
      "error": null
    },
    {
      "test_id": 2,
      "query": "대학생용 문서작업 노트북 추천, 예산 100만원 이내",
      "response": "대학생 문서작업용 노트북으로 100만원 이내 예산을 고려하신다면, 다음 5가지 모델을 추천합니다.\n\n---\n\n### **1. 삼성전자 갤럭시 북 실버 15.6형 (NT550XEZ-A58A)**\n*   **가격대:** 약 70~85만원\n*   **주요 특징:** 12세대 인텔 코어 i5, 16GB 메모리, 256GB SSD, Windows 11 Home 탑재, 15.6인치 디스플레이.\n*   **추천 이유:** 가성비와 성능의 균형이 좋고, 삼성의 전국 A/S 지원이 강점입니다. 윈도우가 기본 탑재되어 있어 편리하게 바로 사용할 수 있습니다.\n*   **출처:** 디시인사이드 등 커뮤니티\n\n### **2. 레노버 아이디어패드 Slim3 15ABR8 82XM0038KR**\n*   **가격대:** 50만원대 ~ 60만원대\n*   **주요 특징:** 라이젠5 Zen3 7530U CPU, 16GB RAM, 256GB SSD, 15.6인치 FHD 디스플레이.\n*   **추천 이유:** 합리적인 가격에 16GB RAM을 제공하여 문서 작업 및 여러 창을 띄워놓는 멀티태스킹에 매우 쾌적한 성능을 보여줍니다.\n*   **구매 링크:** [노써치](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGN-_DF5-e3hNPEf_e0Cu85y41mTdGPZHKzmrZ3fQI_7TGwGsiAN7E-Xvi7fyXEOAPmjEn9Ss6z0OE34Rf5lZI_yd0q55pR4-IWZH0fpMYGm8YnRFL1JefG6ci5_qabR3eYegFEX9HjMiC9lJwj8vo6mjUoQhhX0IMlxHbfcMPo_CuBurpFfxLW3osYrQLjo6YGDg==), [G마켓](https://item.gmarket.co.kr/Item?goodscode=4265053781)\n*   **출처:** 노써치, 디시인사이드\n\n### **3. HP 2024 노트북 15**\n*   **가격대:** 60만원대\n*   **주요 특징:** 라이젠5 7430U CPU, 16GB RAM, 512GB SSD, 라데온 내장 그래픽, Windows 11 Home 포함, 1.59kg.\n*   **추천 이유:** 넉넉한 512GB SSD와 16GB RAM으로 문서 작업은 물론 다양한 학업 활동에 충분하며, 윈도우가 기본 포함되어 있어 추가 비용 부담이 적습니다.\n*   **출처:** 유튜브\n\n### **4. LG 울트라 PC 15U50T-GA5HK**\n*   **가격대:** 65만원\n*   **주요 특징:** i5-1334U CPU, 16GB RAM, 512GB SSD, Windows 11.\n*   **추천 이유:** 국내 대기업 제품임에도 뛰어난 가성비를 자랑합니다. 안정적인 성능과 넉넉한 저장 공간, 윈도우 기본 탑재로 편리하게 사용할 수 있습니다.\n*   **출처:** 노써치\n\n### **5. 레노버 아이디어패드 Slim 5 (Ryzen 7 8845HS)**\n*   **가격대:** 80만원대\n*   **주요 특징:** 라이젠7 8845HS CPU, 16GB RAM, 512GB SSD, 라데온 780M GPU, 1.46kg.\n*   **추천 이유:** 100만원 이내에서 고성능 라이젠 7 CPU와 준수한 내장 그래픽(라데온 780M)을 갖춰 문서 작업은 물론 가벼운 게임이나 멀티미디어 작업까지 고려한다면 좋은 선택입니다. 휴대성도 뛰어납니다.\n*   **출처:** 유튜브",
      "sources": [],
      "response_time_ms": 85822.88,
      "status_code": 200,
      "timestamp": "2025-06-26T05:03:07.135004",
      "error": null
    },
    {
      "test_id": 3,
      "query": "운동할 때 쓸 방수 기능 있는 무선 이어폰 추천",
      "response": "운동 시 사용할 방수 기능이 있는 무선 이어폰으로 다음 제품들을 추천합니다.\n\n*   **샥즈 오픈런 프로2**\n    *   **가격대:** 20만원대\n    *   **주요 특징:** 오픈형 골전도 이어폰, 샥즈 터보 피치 2.0, IP55 방수 등급.\n    *   **추천 이유:** 주변 소리를 인지할 수 있어 야외 운동 시 안전하며, 안정적인 착용감과 땀에 강한 내구성을 제공합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/crkoNN](https://link.coupang.com/a/crkoNN)\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0o2odAO1pjozIIOXGA09Lx_nXEhxdmmNIuBIMbmXatnw6tiZ4grw-QMsGyU6u-uedkPHSO9YguguxzRD848KIuUGGDtip0BJf_r0AOEONeGCQ3WDekCk4uW1QwCSNKo6CoxmJUUqORYpME4HpOyxYwitZDJBJPtg=)\n\n*   **보스 울트라 오픈 이어버드**\n    *   **가격대:** 30만원대\n    *   **주요 특징:** 오픈형 컵스 디자인, 편안한 착용감.\n    *   **추천 이유:** 귓구멍을 막지 않아 압박감이 없으며, 안경이나 마스크 착용 시에도 간섭이 적어 장시간 운동에 적합합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cqQqbW](https://link.coupang.com/a/cqQqbW)\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0o2odAO1pjozIIOXGA09Lx_nXEhxdmmNIuBIMbmXatnw6tiZ4grw-QMsGyU6u-uedkPHSO9YguguxzRD848KIuUGGDtip0BJf_r0AOEONeGCQ3WDekCk4uW1QwCSNKo6CoxmJUUqORYpME4HpOyxYwitZDJBJPtg=)\n\n*   **와일드프로 5.0 고음질 방수 스포츠용 운동용 귀걸이 TWS 핸즈프리 블루투스 무선 이어폰 MT-BE1018D PLUS**\n    *   **가격대:** 3만원대 (2021년 5월 기준)\n    *   **주요 특징:** 스포츠 활동에 특화된 이어훅 디자인, IPZ7 방수 등급, 오토페어링.\n    *   **추천 이유:** 격렬한 운동에도 쉽게 이탈되지 않으며, IPZ7의 높은 방수 등급으로 땀이나 비에 강해 안심하고 사용할 수 있습니다.\n    *   **출처:** [tistory](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrAvebCzvzUHA2QuwMj3PN1X9DApjXJ4ri7AOHCk0u0I5x4-h3hg2Qa4skChF9h69SFKwqUrsd43Jiw-8yNdoCkCJS6Ua74plUH5SQIoCxSPQsR49mh-yia8uYUwBb9z9R4fU8P3C4_6J5B6Lqjxm7KBx_Njg=)\n\n*   **1MORE 오픈형 공기전도 이어폰**\n    *   **가격대:** 10만원대\n    *   **주요 특징:** 오픈형 이어훅 형태, 티타늄 프레임, 9g의 가벼운 무게.\n    *   **추천 이유:** 편안한 착용감과 가성비 좋은 음질을 제공하며, 오픈형으로 주변 소리 인지가 가능하여 운동 시 활용도가 높습니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cqRh4k](https://link.coupang.com/a/cqRh4k)\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0o2odAO1pjozIIOXGA09Lx_nXEhxdmmNIuBIMbmXatnw6tiZ4grw-QMsGyU6u-uedkPHSO9YguguxzRD848KIuUGGDtip0BJf_r0AOEONeGCQ3WDekCk4uW1QwCSNKo6CoxmJUUqORYpME4HpOyxYwitZDJBJPtg=)\n\n*   **샤오미 레드미 버즈 6 라이트**\n    *   **주요 특징:** 12mm 드라이버, 블루투스 5.3, IP54 방수 등급.\n    *   **추천 이유:** 저음이 풍부하고 가격 대비 우수한 음질과 착용감을 제공하여 운동용으로 적합한 가성비 제품입니다.\n    *   **출처:** [Blog](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHbPZKrJ-39NN41RRs-EagSdY_6XIHguRH71nvfRo1ImLM-JfrvBDjQxQnEGO8t3b5hLUGwDzydKH5ghNu4ZjiMY_1SrevY8YOSsJJRLxoBs4gxILIpSG5hClM7L-H5wyCPD04bVLBCcYTBoUq1Z6lxHPjqUF6E00ToeyUp0epgEE91hZkaURmte7NKoLGvf2ZJS3jJte0An6vBr2dg5aaDWrxziFF9JUqO7bwXvs=)",
      "sources": [],
      "response_time_ms": 86931.93,
      "status_code": 200,
      "timestamp": "2025-06-26T05:04:34.068933",
      "error": null
    },
    {
      "test_id": 4,
      "query": "20만원 이하 게이밍 기계식 키보드 추천해줘",
      "response": "20만원 이하 게이밍 기계식 키보드를 찾으시는군요. 다음은 제공된 제품 정보를 바탕으로 추천하는 5가지 모델입니다.\n\n*   **레이니, 아이니 (정발 버전)**\n    *   **가격대:** 20만원 이하\n    *   **주요 특징:** 타건감이 좋으며, 75 배열을 채택했습니다.\n    *   **추천 이유:** 커뮤니티에서 타건감으로 호평받는 제품으로, 뛰어난 키감을 중시하는 사용자에게 적합합니다.\n    *   **출처:** 디시인사이드 기계식키보드 마이너 갤러리\n\n*   **COX 게이트론 LED 게이밍 기계식 키보드**\n    *   **가격대:** 6~7만원대\n    *   **주요 특징:** 입문용 및 라이트 유저에게 적합하며, 게이트론 스위치(황축, 갈축 등)를 사용합니다.\n    *   **추천 이유:** 10만원 미만의 저렴한 가격대에서 게이트론 스위치의 키감을 경험할 수 있는 가성비 좋은 입문용 키보드입니다.\n    *   **출처:** YouTube\n\n*   **타이폰 마르스프로**\n    *   **가격대:** 165,000원\n    *   **주요 특징:** 체리 적축 스위치를 사용하며, 타건음, 타건감, 스테빌라이저 퀄리티가 우수합니다.\n    *   **추천 이유:** 10만원 중반대에서 체리 적축의 안정적인 키감과 전반적으로 높은 빌드 퀄리티를 제공하여 만족도가 높습니다.\n    *   **출처:** 디시인사이드 기계식키보드 마이너 갤러리\n\n*   **AULA F시리즈 (독거미)**\n    *   **가격대:** 5만원대 (F87 Pro / F108은 10만원 미만)\n    *   **주요 특징:** 무선 기능을 지원하며, 좋은 타건감과 감성적인 디자인이 특징입니다. 키감과 타건감에 중점을 둔 모델입니다.\n    *   **추천 이유:** 10만원 미만의 가격대에서 무선 기능과 뛰어난 타건감을 동시에 제공하는 가성비 좋은 무선 키보드를 찾는 분께 추천합니다.\n    *   **출처:** 사용후기™\n\n*   **QSENN Q104 LCD 풀윤활 가스켓 유무선 블루투스 기계식 키보드**\n    *   **가격대:** 59,800원\n    *   **주요 특징:** 풀윤활 처리된 스위치, 가스켓 마운트 방식, 유무선 블루투스 연결, LCD 디스플레이를 지원합니다.\n    *   **추천 이유:** 5만원대라는 합리적인 가격에 풀윤활, 가스켓 마운트, 유무선 등 고급 키보드에서 볼 수 있는 다양한 기능을 갖춘 뛰어난 가성비 모델입니다.\n    *   **출처:** 뽐뿌",
      "sources": [],
      "response_time_ms": 82737.7,
      "status_code": 200,
      "timestamp": "2025-06-26T05:05:56.808620",
      "error": null
    },
    {
      "test_id": 5,
      "query": "영상편집용 고성능 노트북 추천, 예산 200만원 대",
      "response": "200만원대 예산으로 영상 편집용 고성능 노트북을 찾으시는 사용자님께 다음 5가지 제품을 추천합니다.\n\n### 1. 삼성전자 갤럭시북4 울트라 NT960XGP-G72A\n*   **가격대:** 약 260만원 (변동 가능)\n*   **주요 특징:** 코어 울트라7 155H, 32GB RAM, 1TB SSD, RTX4050, 2880x1800(WQXGA+) OLED 터치스크린, USB 4.0\n*   **추천 이유:** 뛰어난 OLED 디스플레이와 터치스크린 기능으로 영상 작업 시 시각적 만족도가 높으며, 삼성의 편리한 AS 및 갤럭시 기기 연동성이 강점입니다.\n*   **출처:** [Refurlab](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG7jxcXc3soNBQO8X8iSzOpC0o6KuX9LEh4swYvnM931G71NZm2iV6s5dwBjYU-krzunT9WzdXJr38UKK9uNhDcTwJ01_ZokA61lJ57nsF9dNvVhgg2jU91hTtz8rhxewS3L4_Aj2QEs3BDtpwO8cMAev8cSll4EklV), [네이버](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF92KayqUhkd5IrBqund9Jwj1O--3e7uAjU33tUGTxPGt45yHL-zWggkBqqmbbU0pZQ03K1FA34UtO9QOppK6lt4gJ6_MaoLeC8-F8W8uGexSxQ2gbf3DwJxkZjZ3qhKbWpQXISWeJ8nA==)\n\n### 2. LG전자 그램 프로16 16Z90SP-ED7BK\n*   **가격대:** 약 245만원 (변동 가능)\n*   **주요 특징:** 코어 울트라7 155H, 32GB RAM, 1TB SSD, RTX3050, 2560x1600(WQXGA), USB 4.0\n*   **추천 이유:** 1.279kg의 초경량으로 휴대성이 매우 뛰어나며, 밝고 선명한 디스플레이와 윈도우 기본 포함으로 즉시 사용이 편리합니다.\n*   **출처:** [다나와](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFVIBnV7AwACuvjsgulkJFxhqLBgwWmN2V9N6bKB65NFA_Ugn8tdaWv8yVWWauEYQ1VyKmB33A5i-_AYkmsLKtL57gkvAuPMVDfTexilAh3kCODCDQFCpXCQYFa5XQbtxmlVctM7UqyArQfIlvePR1CcAJxp_Sgj4xj8mB4TEJrGepqH5MDxzvsNrzlveazkyxi79_VqyKL7w3U3kSQI57OvZpajVaB-v0oznBGbwAxb24S5LHCA-jQsTsb3KYK), [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlqI5njUZ_dPWyp34HUtTGxoAL-orfx-L6gqAUDXqoGdtqvKIme3rwwAWauDV2xTPZWIws2C3HeUi3ZVmBXs--T5f9v3uXaSeRqO8Bvz8thnv2UbdEipfq_2_33oiUpFMfE6wwLg==0)\n\n### 3. APPLE 2025 맥북프로14 M4\n*   **가격대:** 약 269만원 (변동 가능)\n*   **주요 특징:** M4 칩, 24GB RAM, 512GB SSD, M4 GPU, 3024x1964(254ppi) 디스플레이, MacOS, USB 4.0\n*   **추천 이유:** Final Cut Pro에 최적화되어 있으며, 긴 배터리 수명과 저소음으로 쾌적한 작업 환경을 제공합니다. Mac 생태계 사용자에게 특히 유리합니다. (프리미어 프로 플러그인 호환성 확인 필요)\n*   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlqI5njUZ_dPWyp34HUtTGxoAL-orfx-L6gqAUDXqoGdtqvKIme3rwwAWauDV2xTPZWIws2C3HeUi3ZVmBXs--T5f9v3uXaSeRqO8Bvz8thnv2UbdEipfq_2_33oiUpFMfE6wwLg==2)\n\n### 4. 레노버 LEGION 5i 15IRX9\n*   **가격대:** 약 171만원 (할인 적용가, 변동 가능)\n*   **주요 특징:** 인텔 i7-13650HX, 32GB RAM, RTX4060 (140W), 1TB SSD, 15.6인치 FHD 144Hz 디스플레이\n*   **추천 이유:** 강력한 RTX4060 그래픽 카드와 32GB RAM으로 고사양 영상 편집 작업에 적합하며, 뛰어난 쿨링 시스템과 확장성을 제공하여 안정적인 성능을 기대할 수 있습니다.\n*   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlqI5njUZ_dPWyp34HUtTGxoAL-orfx-L6gqAUDXqoGdtqvKIme3rwwAWauDV2xTPZWIws2C3HeUi3ZVmBXs--T5f9v3uXaSeRqO8Bvz8thnv2UbdEipfq_2_33oiUpFMfE6wwLg==2), [Tistory](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlqI5njUZ_dPWyp34HUtTGxoAL-orfx-L6gqAUDXqoGdtqvKIme3rwwAWauDV2xTPZWIws2C3HeUi3ZVmBXs--T5f9v3uXaSeRqO8Bvz8thnv2UbdEipfq_2_33oiUpFMfE6wwLg==3)\n\n### 5. HP OMEN 16-wf1037TX\n*   **가격대:** 약 187만원 (할인 적용가, 변동 가능)\n*   **주요 특징:** 인텔 i7-14700HX, 32GB RAM, RTX4060 (140W), 512GB SSD, 16.1인치 QHD 240Hz 디스플레이\n*   **추천 이유:** 고성능 CPU와 RTX4060 그래픽 카드, QHD 고주사율 디스플레이를 탑재하여 영상 편집은 물론 게이밍 성능까지 뛰어나며, 높은 확장성과 미래 지향적인 포트 구성을 갖추고 있습니다.\n*   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlqI5njUZ_dPWyp34HUtTGxoAL-orfx-L6gqAUDXqoGdtqvKIme3rwwAWauDV2xTPZWIws2C3HeUi3ZVmBXs--T5f9v3uXaSeRqO8Bvz8thnv2UbdEipfq_2_33oiUpFMfE6wwLg==2)",
      "sources": [],
      "response_time_ms": 68816.0,
      "status_code": 200,
      "timestamp": "2025-06-26T05:07:05.626660",
      "error": null
    },
    {
      "test_id": 6,
      "query": "5만원 이하 가성비 좋은 게이밍 마우스 추천",
      "response": "5만원 이하 가성비 게이밍 마우스를 찾으시는 사용자분께 다음 제품들을 추천합니다.\n\n*   **로지텍 G304 LIGHTSPEED**\n    *   **가격대:** 3만원대 (벌크), 4~5만원대 (일반)\n    *   **주요 특징:** 무선, HERO 센서 (최대 12,000 DPI), AA 배터리 1개로 최대 250시간 사용, 빠른 응답속도.\n    *   **추천 이유:** 뛰어난 가성비로 입문용 무선 마우스를 찾는 사용자에게 적합하며, FPS 게임에 유리합니다.\n    *   **출처:** [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuW3PK2npkQ5Iyw_E0_nFnBoDv4iaf_fThMbVnMS99iKx), [리뷰프로](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFEB_sqkykTjJ4zMCDxj-akhKfeabzTNPDXZraUf7d_iDYjImmvXTTiKHzMBBY0VM9hMVagknu_peK56vl54uNqR9xANDwh68Pp555iztMPovJkIupTlAxN63wgwhQZQtPaCZAd), [고레컨 - 티스토리](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGEhzUG92tIRVayd0Fhi68_c36N6TeJu4OQcmmIr_tM), [FPS 게임용 무선 마우스 추천](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHSI1CBcaRdEUJBw3TZTEp7upyQWqgcKTUQGf7LrMaUsIy88cLhV89X_m1U71mKKZxQhmT2E0d51UxllHGVrqQ2gOQ1nSG6U8naB8ju4vrbo4QdwwYmodLlmvc3), [퀘이사존](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGPP2sRsC7rdNRLPjJmNmRxWyHoGsubhIxg0MjW5ib0NLU6N-MX1Ya31r2uw0tTPXo-178EN9RHCIZeL7BckevlGzvwQwwi9xoN7pnsD6oDq03jtbSNjfBRvM-Nq4qt5KRLmXpemE1uLP3X)\n\n*   **VGN VXE R1 SE+ (잠자리 마우스)**\n    *   **가격대:** 3만원대 (1+1 행사 가격 기준)\n    *   **주요 특징:** 유무선 겸용, 51g/55g 초경량, PAW3395 SE 센서.\n    *   **추천 이유:** 매우 가벼운 무게와 뛰어난 가성비로 사무용 및 게임용 모두에 적합하다는 평가를 받습니다.\n    *   **출처:** [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFYr1Sk56Yo_qWCknTDaSte0toBCO8P0h48p2AW9DBxQB2FwZ3XZya6p4a7wd0Vf2RQEnjp-PyrbGcSDDfYcgiCktVUWg-o0yIMYyDZE8j7bOfLVW8VUshrNLobiqQ4k-suoc7Ldg==)\n\n*   **로지텍 G102 2세대 LIGHTSYNC**\n    *   **가격대:** 2만원대\n    *   **주요 특징:** 유선, 가볍고 편안한 그립감, 게이밍에 적합한 성능.\n    *   **추천 이유:** 저렴한 가격에 로지텍의 안정적인 성능과 소프트웨어 지원을 받을 수 있어 PC방 마우스로도 인기가 많습니다.\n    *   **출처:** [DCoupas](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFGATRsRhAkno6-xWHtiCF7dsdXNYXQqV1-VGBQX3F4e4-YnfS5Sh0Dlg7FuqoOzSKi_miwGBQhsRPzF6y800EYPRrbpZYGg70TvejQx8V9d2OxtRe1KAVQ==)\n\n*   **맥스틸 TRON G10 PRO Reborn**\n    *   **가격대:** 5만원 이하 (가성비 라인으로 언급)\n    *   **주요 특징:** 유선, 빠른 반응속도, 무게추 적용 가능.\n    *   **추천 이유:** 빠른 반응속도를 선호하는 사용자에게 가성비 좋은 유선 옵션으로 고려할 만합니다.\n    *   **출처:** [리뷰프로](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFEB_sqkykTjJ4zMCDxj-akhKfeabzTNPDXZraUf7d_iDYjImmvXTTiKHzMBBY0VM9hMVagknu_peK56vl54uNqR9xANDwh68Pp555iztMPovJkIupTlAxN63wgwhQZQtPaCZAd), [킹가이드](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGvDhqcFVZn_FRVIPTbRN3WGAR4JwIoFkiNB18DA_I8Hma06ZM1jnpkw9u7DU0GJh5TlIHgDM_5eY5yN4fn-P3FpMZsNfd5qhV_khTHyVMLlTu5kUDXJXtrarC1sLDw38pJZbIh)\n\n*   **제닉스 타이탄 GV 에어**\n    *   **가격대:** 5만원 이하 (가성비 라인으로 언급)\n    *   **주요 특징:** 69g의 가벼운 무게, \"짭슈라\"로 불릴 만큼 지슈라와 유사한 디자인.\n    *   **추천 이유:** 초경량 마우스를 선호하며, 인기 모델과 유사한 그립감을 저렴하게 경험하고 싶은 사용자에게 적합합니다.\n    *   **출처:** [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuW3PK2npkQ5Iyw_E0_nFnBoDv4iaf_fThMbVnMS99iKx), [리뷰프로](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFEB_sqkykTjJ4zMCDxj-akhKfeabzTNPDXZraUf7d_iDYjImmvXTTiKHzMBBY0VM9hMVagknu_peK56vl54uNqR9xANDwh68Pp555iztMPovJkIupTlAxN63wgwhQZQtPaCZAd)",
      "sources": [],
      "response_time_ms": 72801.37,
      "status_code": 200,
      "timestamp": "2025-06-26T05:08:18.430226",
      "error": null
    },
    {
      "test_id": 7,
      "query": "재택근무용 웹캠 추천, 화질 좋고 10만원 이내로",
      "response": "재택근무용 웹캠으로 화질이 좋고 10만원 이내인 제품을 찾으시는군요. 다음은 해당 조건에 맞는 추천 웹캠 5가지입니다.\n\n---\n\n**1. 앱코 APC930U / APC925**\n*   **가격대:** 7만원 ~ 8만원대 (APC930U), 3만원 ~ 7만원대 (APC925)\n*   **주요 특징:** QHD 해상도, 오토포커스, 넓은 화각, 내장 스테레오 마이크, 사생활 보호 커버.\n*   **추천 이유:** 선명한 QHD 화질과 넓은 화각을 제공하여 화상 회의 및 영상 제작에 적합하며, 가격 대비 성능이 우수합니다.\n*   **구매 링크:** [앱코 APC930U](https://link.coupang.com/a/bRV784)\n*   **출처:** 다양한 쇼핑 정보\n\n**2. 펭카 PCWEB400**\n*   **가격대:** 3만원대\n*   **주요 특징:** 4K 해상도 지원, 노이즈 캔슬링 마이크 내장, 간편한 설치, 다양한 OS 호환.\n*   **추천 이유:** 3만원대라는 매우 합리적인 가격에 4K 화질을 제공하여 온라인 수업 및 화상 회의에 뛰어난 가성비를 자랑합니다.\n*   **출처:** 네이버 쇼핑 등 온라인 쇼핑몰 정보\n\n**3. 한성컴퓨터 4K 웹캠**\n*   **가격대:** 5만원대\n*   **주요 특징:** 4K UHD 해상도, 800만 화소, 자동 초점, 77도 넓은 시야각, 내장 마이크, 프라이버시 셔터.\n*   **추천 이유:** 5만원대의 합리적인 가격에 4K 화질과 다양한 편의 기능을 제공하여 고화질 재택근무 환경에 적합합니다.\n*   **구매 링크:** [한성컴퓨터 4K 웹캠](https://link.coupang.com/a/bRuL15)\n*   **출처:** 다양한 쇼핑 정보\n\n**4. 로지텍 C920**\n*   **가격대:** 7만원 ~ 10만원대\n*   **주요 특징:** Full HD(1920x1080) 해상도, 화상 수업용으로 적합, 로지텍 브랜드의 높은 신뢰도.\n*   **추천 이유:** 웹캠 시장에서 검증된 로지텍의 대표 모델로, 안정적인 FHD 화질과 뛰어난 호환성을 제공하여 일반적인 재택근무 및 화상 회의에 적합합니다.\n*   **출처:** 다양한 쇼핑 정보\n\n**5. 넥스트유 CAM1080A**\n*   **가격대:** 3만원대\n*   **주요 특징:** FHD(1920x1080) 1080P 해상도, 오토포커스, USB 연결.\n*   **추천 이유:** 3만원대의 저렴한 가격에도 FHD 화질과 오토포커스 기능을 제공하여 가성비 좋은 재택근무용 웹캠을 찾는 분께 적합합니다.\n*   **출처:** YouTube 정보",
      "sources": [],
      "response_time_ms": 93618.25,
      "status_code": 200,
      "timestamp": "2025-06-26T05:09:52.050836",
      "error": null
    },
    {
      "test_id": 8,
      "query": "카메라 성능 좋은 스마트폰 추천, 예산 50만원 이하",
      "response": "50만원 이하 예산으로 카메라 성능이 좋은 스마트폰을 찾으신다면 다음 제품들을 추천합니다.\n\n*   **구글 픽셀 7a (중고)**\n    *   **가격대:** 50만원 이하 (중고)\n    *   **주요 특징:** 구글 텐서 G3 칩셋, 64MP 메인 카메라 + 13MP 초광각, 5년간 안드로이드 업데이트 보장.\n    *   **추천 이유:** 구글의 뛰어난 소프트웨어 최적화 덕분에 특히 야간 촬영에서 발군의 카메라 성능을 보여줍니다. 최고의 소프트웨어 경험을 제공합니다.\n    *   **출처:** [choigo-da BLOG](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFcC3XmFN0hmvRh83BwBqrluCokU9sgveEFU3-ZELs-EGT0b_vQSY7PlPxCOcAabRJZSsrZ9rmfFME0o05uGYr6oO7HZNQRAn9Dcz3s6iCikAa3fPn2TXM4vmM_SujLPyXyAiLyIAVkP1ynKnjN6ADLlFlEWs4EleP89rMeaW8IoDx4hm04WtAf7H7UvTnDcngMQLD_NbVbs-KcR7Sbm0WY9OMGT0lRLBbP1Ta1pRQDo4jjpFVMWynAP6dhQ==)\n\n*   **갤럭시 S22 울트라 (중고)**\n    *   **가격대:** 30만원대 후반 (중고)\n    *   **주요 특징:** 플래그십 모델로, 카메라 성능 업그레이드에 용이합니다.\n    *   **추천 이유:** 30만원대 후반의 가격으로 플래그십급의 카메라 성능을 경험할 수 있어 가성비가 뛰어납니다.\n    *   **출처:** [디시인사이드](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQp4cQWKxaCzg3WR5DWcCjje60ZDsbKZEtVo4xcSPk0p6vd1XONtpxhnTvXqKFZbkE6nnw3TicNE6fG8VOqpt4-3vs21cnMQ5JzsNyUYfpfSj_TuIzcO3l7Uk5jAXLIwlYusuQJhwI66y2vyML)\n\n*   **삼성 갤럭시 A35**\n    *   **가격대:** 40만원대 초반\n    *   **주요 특징:** 플래그십 디자인, OIS (광학 손떨림 보정) 지원 카메라, 120Hz 디스플레이, 삼성페이 지원.\n    *   **추천 이유:** OIS 덕분에 사진 촬영 시 안정적이며, 일상 사용에 적합한 성능과 세련된 디자인을 갖춘 신제품입니다.\n    *   **출처:** [아정당](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyxgRh4oO7nvKD45zpv6GXQznY87mle0Wx-URgigf0eEZnE8P1oF7IBHWWhAKTtcTYuk74ZKUQ77NIeJhzBCm0zMsyZ16NzI mAhbbSurRYb2rfP_fBVQZUlDAUSccqXPvItk2GKdQF-66N-_SFzE8GiYqqUt6k2C_2vH8x1NrCdBXuDjmlbvL mRms6IudqN5SsfGAu66qxJyARaLvw1IgV2b6DLtNUdZds3jz49FeBBrtzSCw67vl5dnCfOQa9fSsAKCB_0pJYV9tbaRFpidQ8CA==), [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG7JUpIZhu5fv9FoQCS_mGbMqr32y5pX3StDYSmQmSgi2hXeKKqEBCcTUFlqT49iIYxmj4BUAnrgNjzYQGYMO_F6Hj7sJT4WLFkPrBISOm51dh2wX5daYNefJzD1yiXmvVF9DzX9-A=)\n\n*   **샤오미 Redmi Note 13**\n    *   **가격대:** 30만원대\n    *   **주요 특징:** 120Hz AMOLED 디스플레이, 108MP 카메라, 5000mAh 대용량 배터리.\n    *   **추천 이유:** 108MP 고화소 카메라를 탑재하여 사진 품질이 우수하며, 가격 대비 뛰어난 성능을 제공합니다.\n    *   **출처:** 뽐뿌, dalinart 블로그\n\n*   **갤럭시 S23 (중고)**\n    *   **가격대:** 40만원대 (중고)\n    *   **주요 특징:** 플래그십 모델로, 전반적으로 우수한 카메라 성능을 제공합니다.\n    *   **추천 이유:** 40만원대 중고 가격으로 비교적 최신 플래그십 모델의 안정적인 카메라 성능을 누릴 수 있습니다.\n    *   **출처:** [디시인사이드](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQp4cQWKxaCzg3WR5DWcCjje60ZDsbKZEtVo4xcSPk0p6vd1XONtpxhnTvXqKFZbkE6nnw3TicNE6fG8VOqpt4-3vs21cnMQ5JzsNyUYfpfSj_TuIzcO3l7Uk5jAXLIwlYusuQJhwI66y2vyML)",
      "sources": [],
      "response_time_ms": 63768.96,
      "status_code": 200,
      "timestamp": "2025-06-26T05:10:55.821634",
      "error": null
    },
    {
      "test_id": 9,
      "query": "장시간 착용해도 편한 헤드셋 추천, 사무용으로 15만원 이하",
      "response": "장시간 착용에도 편안한 15만원 이하 사무용 헤드셋으로 다음 제품들을 추천합니다.\n\n1.  **소니 WH-CH520**\n    *   **가격대:** 7만원 ~ 9만원대\n    *   **주요 특징:** 약 147g의 가벼운 무게, 푹신한 이어패드, 최대 50시간 사용 가능한 긴 배터리.\n    *   **추천 이유:** 가성비가 뛰어나며, 가벼운 무게와 편안한 이어패드로 장시간 착용 시 부담이 적습니다.\n    *   **출처:** [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErnb5JpVm0K95URXPh2nF63DlYvHaCL2nPOF8SBZ0qLgpdDZXm57My0roYiAH86MzRLA0nOosoRPOs9DYas5VRUjnXOyYkm169KqIaKt2ci0xpVtjmLz22KumdeDaPUhQE9oKltWcTCLsx](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErnb5JpVm0K95URXPh2nF63DlYvHaCL2nPOF8SBZ0qLgpdDZXm57My0roYiAH86MzRLA0nOosoRPOs9DYas5VRUjnXOyYkm169KqIaKt2ci0xpVtjmLz22KumdeDaPUhQE9oKltWcTCLsx)\n\n2.  **자브라 Evolve2 30**\n    *   **가격대:** 9만원 ~ 11만원대\n    *   **주요 특징:** 소음 제거 마이크 2개 탑재, 인체공학적 설계, Microsoft Teams 인증.\n    *   **추천 이유:** 화상 회의나 전화 통화 시 주변 소음을 효과적으로 줄여주고 음성 전달이 깨끗하여 사무용으로 매우 적합합니다.\n    *   **출처:** [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErnb5JpVm0K95URXPh2nF63DlYvHaCL2nPOF8SBZ0qLgpdDZXm57My0roYiAH86MzRLA0nOosoRPOs9DYas5VRUjnXOyYkm169KqIaKt2ci0xpVtjmLz22KumdeDaPUhQE9oKltWcTCLsx](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErnb5JpVm0K95URXPh2nF63DlYvHaCL2nPOF8SBZ0qLgpdDZXm57My0roYiAH86MzRLA0nOosoRPOs9DYas5VRUjnXOyYkm169KqIaKt2ci0xpVtjmLz22KumdeDaPUhQE9oKltWcTCLsx)\n\n3.  **앤커 Soundcore Life Q30**\n    *   **가격대:** 10만원 ~ 12만원대\n    *   **주요 특징:** 하이브리드 액티브 노이즈 캔슬링(ANC), 40mm 다이내믹 드라이버, EQ 설정 가능.\n    *   **추천 이유:** 뛰어난 노이즈 캔슬링 기능으로 집중이 필요한 사무 환경에 적합하며, 풍부한 사운드를 제공합니다.\n    *   **출처:** [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErnb5JpVm0K95URXPh2nF63DlYvHaCL2nPOF8SBZ0qLgpdDZXm57My0roYiAH86MzRLA0nOosoRPOs9DYas5VRUjnXOyYkm169KqIaKt2ci0xpVtjmLz22KumdeDaPUhQE9oKltWcTCLsx](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErnb5JpVm0K95URXPh2nF63DlYvHaCL2nPOF8SBZ0qLgpdDZXm57My0roYiAH86MzRLA0nOosoRPOs9DYas5VRUjnXOyYkm169KqIaKt2ci0xpVtjmLz22KumdeDaPUhQE9oKltWcTCLsx)\n\n4.  **QCY H3 무선 노이즈 캔슬링 블루투스 헤드셋**\n    *   **가격대:** 약 2만원대\n    *   **주요 특징:** 노이즈 캔슬링 기능, 부드러운 가죽 패드와 메모리 폼 쿠션, 최대 35시간 배터리.\n    *   **추천 이유:** 매우 뛰어난 가성비와 편안한 착용감으로 장시간 사용에도 귀와 머리에 부담이 적다는 평가를 받습니다.\n    *   **출처:** [Sarah pick 네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHdi2kG4t9aCJxizvTIQbVzTXev6IiFMkmCCppoT36Dj78C97hoM27zQR2mV0xkw7xLNFq0J314aGZYHyJss5fKrYDws-0Z-7qBo9BrD6HIikU53dVEG4v77IyhntuKb4C7QQ-2Y_lw5bnqNnDiw8HGdB3IR_xtdPiWhn82hu_qGAvi5K9y6vYKGpboLcNVcUsB6A==)\n\n5.  **마이크로소프트 모던 USB-C 헤드셋**\n    *   **가격대:** (정보 없음, 다나와 가격 비교 필요)\n    *   **주요 특징:** 142g의 가벼운 무게, 소프트한 가죽 재질 쿠션형 이어컵, 유연한 접이식 고감도 마이크, USB-C 타입 연결, Microsoft Teams 앱 전용 버튼.\n    *   **추천 이유:** 가벼운 무게와 편안한 착용감으로 화상 회의가 잦은 사무 환경에 특히 적합하며, 깨끗한 음성 전달이 강점입니다.\n    *   **출처:** [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG2-VxUoWO8spwpoHi_6D1bStIzsE_EY_fj6v76mQHYqMne0U1PGYgtnpRHVGxij1DkcrdRh7_kspfCf_SRhQxnca0Aee7God3Kt1me1CjsTdUsOo83_ijxk8aa-P5lRB9ThzFX](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG2-VxUoWO8spwpoHi_6D1bStIzsE_EY_fj6v76mQHYqMne0U1PGYgtnpRHVGxij1DkcrdRh7_kspfCf_SRhQxnca0Aee7God3Kt1me1CjsTdUsOo83_ijxk8aa-P5lRB9ThzFX)",
      "sources": [],
      "response_time_ms": 63928.78,
      "status_code": 200,
      "timestamp": "2025-06-26T05:11:59.752576",
      "error": null
    },
    {
      "test_id": 10,
      "query": "휴대용 모니터 추천, 업무용으로 쓸건데 30만원 이내",
      "response": "업무용 휴대용 모니터로 30만원 이내 제품을 찾으신다면 다음 5가지 모델을 추천합니다.\n\n1.  **LG전자 그램 +View 16MR70**\n    *   **가격대:** 30만원대 초반\n    *   **주요 특징:** 920g의 가벼운 무게와 8.3mm의 얇은 두께로 뛰어난 휴대성, 2560x1600 (WQXGA) 고해상도, DCI-P3 99%의 높은 색재현율, USB-C 포트 2개 지원.\n    *   **추천 이유:** LG 그램 노트북과 동일한 화질 스펙으로 확장 모니터 사용 시 이질감이 없으며, 사무용으로 최적화된 품질과 신뢰할 수 있는 사후 서비스를 제공합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/b8havK](https://link.coupang.com/a/b8havK)\n    *   **출처:** [노써치](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEy_311ekJyIe5Ip8GRts_hZN82qifaImQFlvbbnzC-FF4Yk3_9S2uz4HSQ0mnpRbwFvL8SlnuvmHG8prCAxVyFEtLXQIA-LM4Edbp_kGtUql2KtkP_hSzWz7PJCoW6xeS_O659HBM70EYr6USoGGWSm0m6aDI6HYR5aGDXM615nJlmrGVfhcWlH66VODFr_Tsl7C7DGKAcurQ98pQEaeQcERxi2qLmACJcUsYd9Lo=), [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGcLJVtQn9gpxqgKvApuFP3uaRivP-5SXkeXDW1MurNapduj5JvhyxQcNOVPMCnjxTJ-yFpchBW1pTifa9mHFrRDnKX9kACMzx8A4W0cq_jKdge1q4CRpd5vbnD8zS7r4sKuS_wnJw=)\n\n2.  **알파스캔 16F90P IPS USB-C 포터블 HDR 무결점**\n    *   **가격대:** 17만원 ~ 20만원\n    *   **주요 특징:** 16인치 FHD (1920x1080) 해상도, 805g의 가벼운 무게와 10mm의 얇은 두께, 최대 2년 A/S 지원.\n    *   **추천 이유:** 성능과 가격의 밸런스가 합리적이며, 초기 불량 걱정 없이 안정적으로 사용할 수 있는 제품입니다.\n    *   **구매 링크:** 다양한 온라인 쇼핑몰에서 구매 가능\n    *   **출처:** [노써치](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEy_311ekJyIe5Ip8GRts_hZN82qifaImQFlvbbnzC-FF4Yk3_9S2uz4HSQ0mnpRbwFvL8SlnuvmHG8prCAxVyFEtLXQIA-LM4Edbp_kGtUql2KtkP_hSzWz7PJCoW6xeS_O659HBM70EYr6USoGGWSm0m6aDI6HYR5aGDXM615nJlmrGVfhcWlH66VODFr_Tsl7C7DGKAcurQ98pQEaeQcERxi2qLmACJcUsYd9Lo=)\n\n3.  **ZEUSLAP P16ST 16인치 144Hz 2.5K 터치 모니터**\n    *   **가격대:** 225,000원 (특가)\n    *   **주요 특징:** 16인치, 2.5K 고해상도, 144Hz 주사율, 터치 기능 지원.\n    *   **추천 이유:** 고해상도와 터치 기능으로 업무 효율성을 높일 수 있으며, 부드러운 화면 전환이 필요한 작업에도 적합합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cwhtm5](https://link.coupang.com/a/cwhtm5)\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE30K3cbLSsRdJMVOyxeMdtaOy5unXjkVGxdkHjY2MKjCfuKF1r2ZtnXiX-2BwgR9VYiyT3aGMuPaoeKQ0Dblo50PCRrI7aljXNCAo_kIWlCj7KkXkgBP-1C3GXQtmGkIAN6DUFmQ==)\n\n4.  **UPERFECT 터치 휴대용 모니터 IPS 18 인치 HDR 120Hz**\n    *   **가격대:** 169,000원 (특가)\n    *   **주요 특징:** 18인치 대화면, IPS 패널, HDR 지원, 120Hz 주사율, 터치 기능.\n    *   **추천 이유:** 넓은 화면으로 멀티태스킹 작업에 유리하며, 터치 기능으로 편리성을 더했습니다. 가성비 좋은 대화면 휴대용 모니터를 찾는 분께 적합합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cwhtvi](https://link.coupang.com/a/cwhtvi)\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE30K3cbLSsRdJMVOyxeMdtaOy5unXjkVGxdkHjY2MKjCfuKF1r2ZtnXiX-2BwgR9VYiyT3aGMuPaoeKQ0Dblo50PCRrI7aljXNCAo_kIWlCj7KkXkgBP-1C3GXQtmGkIAN6DUFmQ==)\n\n5.  **ZEUSLAP 제우스랩 15.6inch 120hz IPS 휴대용 모니터 DEX 모니터 P15A120hz**\n    *   **가격대:** 97,000원\n    *   **주요 특징:** 15.6인치, 120Hz 주사율, IPS 패널, DEX 지원, 초경량/초슬림 디자인.\n    *   **추천 이유:** 10만원 미만의 가격으로 뛰어난 가성비를 자랑하며, 높은 주사율과 DEX 지원으로 다양한 기기와의 호환성 및 활용성이 우수합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cAgj92](https://link.coupang.com/a/cAgj92)\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCm4dILhXOrPhXWI05MEpCrabOQzQi-a2nRXB2p2PfjvwGSeNwHf6c8ZIwLYRUVKU-Uxsud5OnO9RjzNYyEcHPtRHXociCfvKnMfqMYO0n6cMRBCjpsB5DSVEZ_4OUqtw3w9MuBQ==)",
      "sources": [],
      "response_time_ms": 90587.03,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:30.342568",
      "error": null
    },
    {
      "test_id": 11,
      "query": "키보드 추천해줘",
      "response": "어떤 용도로 사용하실 키보드를 찾으시나요? (예: 게이밍, 사무용, 휴대용 등) 예산은 어느 정도 생각하고 계신가요?",
      "sources": [],
      "response_time_ms": 2794.49,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:33.141226",
      "error": null
    },
    {
      "test_id": 12,
      "query": "좋은 노트북 알려줘",
      "response": "어떤 용도로 노트북을 찾으시는지, 예산은 어느 정도 생각하시는지, 그리고 특별히 필요한 기능이 있으신지 알려주시면 더 적합한 제품을 추천해 드릴 수 있습니다.",
      "sources": [],
      "response_time_ms": 3549.74,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:36.693255",
      "error": null
    },
    {
      "test_id": 13,
      "query": "이어폰 뭐가 좋을까?",
      "response": "어떤 용도로 사용하실 건가요? (예: 운동용, 통화용, 음악 감상용 등) 예산은 어느 정도 생각하시는지, 그리고 선호하는 형태(무선/유선, 인이어/오버이어 등)나 특별히 필요한 기능(노이즈 캔슬링, 방수 등)이 있으신가요?",
      "sources": [],
      "response_time_ms": 3991.33,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:40.686842",
      "error": null
    },
    {
      "test_id": 14,
      "query": "마우스 추천",
      "response": "어떤 용도로 사용하실 마우스를 찾으시나요? (예: 게이밍, 사무용, 휴대용 등) 예산은 어느 정도로 생각하시나요? 특별히 선호하는 기능이나 브랜드가 있으신가요?",
      "sources": [],
      "response_time_ms": 3071.4,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:43.760324",
      "error": null
    },
    {
      "test_id": 15,
      "query": "스마트폰 사고 싶어",
      "response": "어떤 용도로 사용하실 건가요? (예: 게임, 사진 촬영, 업무용) 예산은 어느 정도로 생각하시나요? 특별히 선호하는 브랜드나 중요하게 생각하는 기능이 있으신가요?",
      "sources": [],
      "response_time_ms": 2353.21,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:46.115818",
      "error": null
    },
    {
      "test_id": 16,
      "query": "모니터 추천해줘",
      "response": "어떤 용도로 사용하실 모니터인가요? (예: 게임, 사무, 디자인 등) 예산은 어느 정도로 생각하시나요? 아니면 특별히 원하는 기능이 있으신가요?",
      "sources": [],
      "response_time_ms": 3142.63,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:49.260538",
      "error": null
    },
    {
      "test_id": 17,
      "query": "헤드셋이 필요해",
      "response": "어떤 용도로 사용하실 건가요? (예: 게임, 음악 감상, 업무 등) 예산은 어느 정도로 생각하시나요? 특별히 원하는 기능이 있으신가요?",
      "sources": [],
      "response_time_ms": 4842.75,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:54.105130",
      "error": null
    },
    {
      "test_id": 18,
      "query": "웹캠 뭐 쓸까?",
      "response": "어떤 용도로 사용하실 웹캠을 찾으시나요? (예: 화상 회의, 온라인 수업, 스트리밍 등) 예산은 어느 정도 생각하고 계신가요? 특별히 필요한 기능이 있으신가요?",
      "sources": [],
      "response_time_ms": 3773.59,
      "status_code": 200,
      "timestamp": "2025-06-26T05:13:57.881123",
      "error": null
    },
    {
      "test_id": 19,
      "query": "태블릿 추천",
      "response": "어떤 용도로 사용하실 건가요? (예: 학습용, 영상 시청용, 그림 그리기용 등) 예산은 어느 정도로 생각하시나요? 특별히 원하는 기능이 있으신가요?",
      "sources": [],
      "response_time_ms": 3387.03,
      "status_code": 200,
      "timestamp": "2025-06-26T05:14:01.270304",
      "error": null
    },
    {
      "test_id": 20,
      "query": "프린터 사야 하는데",
      "response": "어떤 용도로 사용하실 예정이신가요? (예: 가정용, 사무용, 사진 인쇄용 등) 그리고 예산은 어느 정도로 생각하시나요?",
      "sources": [],
      "response_time_ms": 5126.27,
      "status_code": 200,
      "timestamp": "2025-06-26T05:14:06.398122",
      "error": null
    },
    {
      "test_id": 21,
      "query": "중고등학생용 학습 태블릿 추천, 15만원 이하로 펜 지원되는 걸로",
      "response": "중고등학생 학습용 태블릿으로 15만원 이하, 펜 지원 조건을 모두 충족하는 제품은 현재 **레노버 샤오신 패드 2024**가 가장 적합합니다.\n\n*   **레노버 샤오신 패드 2024**\n    *   **가격대:** 10만원대 초반 (14만원 내외)\n    *   **주요 특징:** 가성비가 우수하며, 레노버 정품 펜 AP500U와 호환되어 필기가 가능합니다.\n    *   **추천 이유:** 10만원대 태블릿 중 필기 기능이 확인된 몇 안 되는 모델로, 간단한 메모나 아이디어 정리, 학생들이 필기용으로 사용하기에 적합합니다.\n    *   **구매 링크:**\n        *   쿠팡 직구: [https://link.coupang.com/a/bmUEdy](https://link.coupang.com/a/bmUEdy)\n        *   다나와: [https://prod.danawa.com/info/?pcode=29618384](https://prod.danawa.com/info/?pcode=29618384)\n        *   레노버 펜 AP500U: [https://link.gmarket.co.kr/itTXvuwBF](https://link.gmarket.co.kr/itTXvuwBF)\n    *   **출처:** 10만원대 가성비 태블릿은 필기용으로 쓸만할까? (샤오신패드 2024 + 펜 AP500U 사용 후기)\n\n**참고:** 15만원 이하의 예산으로 펜 지원 태블릿을 찾는 것은 매우 제한적입니다. 위 제품 외에는 펜 지원 여부가 불확실하거나 가격대가 15만원을 초과하는 경우가 많습니다. 구매 전 반드시 최신 가격과 펜 호환 여부를 확인하시기 바랍니다.",
      "sources": [],
      "response_time_ms": 57642.53,
      "status_code": 200,
      "timestamp": "2025-06-26T05:15:04.041828",
      "error": null
    },
    {
      "test_id": 22,
      "query": "출장용 노트북 파우치 추천, 15인치 노트북용 충격방지 기능 있는 걸로",
      "response": "출장용 15인치 노트북을 위한 충격 방지 파우치를 찾으시는군요. 다음은 충격 방지 기능과 출장 시 유용한 특징을 갖춘 추천 제품들입니다.\n\n### 추천 제품\n\n1.  **킨맥 360 시리즈 랩탑 숄더 백**\n    *   **주요 특징:** 두툼한 엠보싱 쿠션과 모서리 완벽 보호로 360도 충격 방지 기능을 제공합니다. 탈부착 가능한 숄더 스트랩과 캐리어 연결 장치가 있어 출장 시 휴대 편의성이 뛰어납니다. 전면 수납 포켓으로 주변기기 수납도 용이합니다.\n    *   **추천 이유:** 강력한 충격 보호 기능과 캐리어 연결 등 출장 시 필요한 실용적인 기능들을 모두 갖추고 있습니다.\n    *   **출처:** [쿠팡, 네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFK1Drr5tCbWJpinbGvr15-hG2tIzz_EFPbKv2PGJd5mvmDu85gQWHy6MPKGB-p83hmpF0dSWsEabbcqY1JfegFLVYARAhVWNbMjREKcEdItffIOVKjumOZKFLuX_raBSN53FqWwTC5MGt716URzxTWsrlJQg==)\n\n2.  **INC 노트북 서류가방 (15.6인치)**\n    *   **주요 특징:** 15.6인치 노트북에 적합하며, 생활 방수 폴리에스테르 겉감과 극세사 안감으로 스크래치 및 충격 방지 기능을 제공합니다. 손잡이 내장으로 파우치/가방 겸용 사용이 가능하며, 숄더/크로스 끈이 포함되어 휴대성이 좋습니다. 넉넉한 수납 공간이 장점입니다.\n    *   **추천 이유:** 가방 겸용으로 활용할 수 있어 실용적이며, 생활 방수 및 충격 방지 기능으로 출장 시 노트북을 안전하게 보호할 수 있습니다.\n    *   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH-Kl6EqmVWDz853Jl57H0BVbEu0NJ4SmDhYGcpINXrM9wubWsAjZdfLSZ4M-swtf7aBzjGDg7hl0JMv7pJcNSDPIQoqK7Os_8iQedHPd1u5EOgk84e8ICDG4y9QPRHCrZ3Okd3a0k=)\n\n3.  **탐탁 360 세이프가드 노트북 브리프 케이스**\n    *   **주요 특징:** 자동차 에어백과 유사한 코너 암머 기술을 적용하여 뛰어난 충격 보호 기능을 자랑합니다. 노트북을 단단히 고정하는 시큐어 벨트가 내장되어 있으며, 실용적인 수납 공간을 제공합니다.\n    *   **추천 이유:** 이동 중 발생할 수 있는 강한 충격으로부터 노트북을 철저하게 보호하고자 할 때 최적의 선택입니다.\n    *   **출처:** [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEIklmFtRjfyWOkDqBEObJSH0fQFVBJytITAI5t8hbcoiSmYdBwNeVvJDuTsPG6LDEMHluzIKr9KcAteH4dpPnRptDwzndOD3IQ8aJsguOHRGDj46dmvPgszvZfLQzgm0jfSypk3g==)\n\n4.  **뉴엔 맥북 노트북 파우치 CP55**\n    *   **주요 특징:** 내마모성 원단과 생활 방수 기능을 갖추고 있으며, 푹신한 내부 재질로 기기를 안전하게 보호합니다. 캐리어 거치 끈, 핸드 스트랩 및 탈부착 스트랩이 제공되어 다양한 방식으로 휴대할 수 있으며, 외장하드, 충전기, 마우스 등 주변기기 수납이 용이합니다.\n    *   **추천 이유:** 캐리어 거치 기능과 다양한 수납 공간, 여러 형태의 스트랩 제공으로 출장 시 휴대 편의성을 극대화한 제품입니다.\n    *   **출처:** [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEIklmFtRjfyWOkDqBEObJSH0fQFVBJytITAI5t8hbcoiSmYdBwNeVvJDuTsPG6LDEMHluzIKr9KcAteH4dpPnRptDwzndOD3IQ8aJsguOHRGDj46dmvPgszvZfLQzgm0jfSypk3g==)\n\n5.  **HP 슬리브 15인치 14V33AA**\n    *   **가격대:** 9,840원\n    *   **주요 특징:** 15인치대 노트북 수납이 가능하며, 내충격성, 긁힘 방지, 내수성 기능을 제공합니다. 230g의 가벼운 무게가 특징입니다.\n    *   **추천 이유:** 합리적인 가격으로 기본적인 충격 방지 및 생활 방수 기능을 제공하여, 가볍고 필수적인 보호 기능을 원하는 사용자에게 적합합니다.\n    *   **구매 링크:** [다나와](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTmVw2g5Fx9ajkFX50W3jFlFQhUFDdiYlGbnYNjKO_QrzDyh4AuigZ6V8jfdLNMft6kAKoD9biXaBnoGk1dyvr0HWgvyeTp5IO2IDl0b0yK8zzG6WiYa5b6N3-rS0EENSnDKXy6HPRuKTDVFWXPgeO2TGWEWJcgyLa-vbVm24roTJlPvlMqYEdlBIuPw2x9BZ8cBPEAstq4P7SycPpbdqZTkbNElGh6467Nvhd-vP8g5c=)\n    *   **출처:** [다나와](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTmVw2g5Fx9ajkFX50W3jFlFQhUFDdiYlGbnYNjKO_QrzDyh4AuigZ6V8jfdLNMft6kAKoD9biXaBnoGk1dyvr0HWgvyeTp5IO2IDl0b0yK8zzG6WiYa5b6N3-rS0EENSnDKXy6HPRuKTDVFWXPgeO2TGWEWJcgyLa-vbVm24roTJlPvlMqYEdlBIuPw2x9BZ8cBPEAstq4P7SycPpbdqZTkbNElGh6467Nvhd-vP8g5c=)",
      "sources": [],
      "response_time_ms": 94261.45,
      "status_code": 200,
      "timestamp": "2025-06-26T05:16:38.305224",
      "error": null
    },
    {
      "test_id": 23,
      "query": "집에서 쓸 프린터 추천, 가정용으로 컬러 인쇄 가능한 20만원 이하",
      "response": "집에서 사용할 20만원 이하 컬러 프린터를 찾으신다면 다음 제품들을 추천합니다.\n\n1.  **삼성전자 SL-C513W**\n    *   **가격대:** 199,000원 (2023년 10월 기준)\n    *   **주요 특징:** 컬러 레이저 프린터, Wi-Fi, 유선랜, USB 등 다양한 연결 방식 지원, NFC 탑재로 간편한 모바일 프린팅, 컴팩트한 사이즈.\n    *   **추천 이유:** 가정이나 소규모 사무실에 적합하며, 다양한 연결 옵션이 편리합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/bgVva2](https://link.coupang.com/a/bgVva2)\n    *   **출처:** YouTube\n\n2.  **캐논 PIXMA 정품 무한 G1930**\n    *   **가격대:** 10만원대 초중반\n    *   **주요 특징:** 정품 무한 잉크 시스템, 대량의 컬러 문서나 사진 인쇄에 적합.\n    *   **추천 이유:** 유지비 부담 없이 대량 컬러 인쇄가 필요한 실속형 구매자에게 적합합니다.\n    *   **출처:** 다나와\n\n3.  **엡손 EcoTank L3250**\n    *   **가격대:** 약 20만원대\n    *   **주요 특징:** 정품 무한 잉크 시스템으로 유지비 절감, 스마트폰 무선 인쇄 및 컬러 사진 출력 가능, 모바일 앱 호환.\n    *   **추천 이유:** 경제적인 유지비와 편리한 무선 연결로 가정에서 다양한 컬러 인쇄물을 출력하기 좋습니다.\n    *   **출처:** 티스토리\n\n4.  **삼성 SL-J1780W 잉크젯 복합기**\n    *   **가격대:** 10만원대 초반 (쿠팡 할인 적용)\n    *   **주요 특징:** 잉크젯 복합기 (프린트, 스캔, 복사), Wi-Fi 무선 연결 지원, 심플한 디자인.\n    *   **추천 이유:** 저렴한 가격에 인쇄, 스캔, 복사 기능을 모두 갖춘 무선 복합기로 가정용으로 활용도가 높습니다.\n    *   **출처:** 네이버 블로그\n\n5.  **캐논 무한 잉크젯 복합기 G2910**\n    *   **주요 특징:** 프린트, 복사, 스캔 3in1 복합기, 무한 잉크 탱크로 유지비 절감, 캐논 특유의 고화질 컬러 출력, 흑백 6,000매/컬러 7,000매 출력 가능.\n    *   **추천 이유:** 높은 출력량과 고화질 컬러 인쇄가 가능하여 초등학생부터 고등학생까지 학습용으로 활용하기에 적합합니다.\n    *   **출처:** 티스토리",
      "sources": [],
      "response_time_ms": 63838.73,
      "status_code": 200,
      "timestamp": "2025-06-26T05:17:42.146249",
      "error": null
    },
    {
      "test_id": 24,
      "query": "신혼집 스마트 TV 추천, 거실용 55인치 이상 100만원 이내",
      "response": "신혼집 거실용 55인치 이상 스마트 TV를 100만원 이내로 찾으시는군요. 다음은 해당 조건에 맞는 추천 제품들입니다.\n\n*   **삼성전자 4K UHD QLED 스마트 TV (KQ55QD67AFXKR)**\n    *   **가격대:** 82만원대\n    *   **주요 특징:** QLED 기술로 뛰어난 화질과 색 재현율, Tizen OS 기반의 직관적인 스마트 기능, 얇고 세련된 디자인, HDMI 2.1 및 ALLM 등 게이밍 기능 지원.\n    *   **추천 이유:** 대기업 제품의 안정적인 성능과 뛰어난 화질, 편리한 스마트 기능으로 OTT 서비스 이용이 잦은 신혼부부에게 적합합니다.\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEkkltIwOcW8IAvvKI0KPr238XCfRXkCKy5CSwbkfuHzd4DoEbwQZxq3Kepz8iQOXvFKc-gdGGjA47UaEwZc1vfjz66DAV2Da9oWAFlo_aRRJW4zrwcGIVfnCKXiZcWtIP6I4iAhw==)\n\n*   **LG전자 울트라 HD 55인치 TV**\n    *   **가격대:** 60만원대 ~ 70만원대\n    *   **주요 특징:** IPS 패널로 넓은 시야각과 정확한 색감, 인공지능 알파 7 프로세서로 화질 및 음질 자동 최적화, LG 씽큐(ThinQ) AI 기능, 돌비 비전 IQ 및 돌비 애트모스 지원.\n    *   **추천 이유:** LG 특유의 선명한 화질과 넓은 시야각, 인공지능 기반의 편리한 스마트 기능으로 몰입감 있는 시청 경험을 제공합니다.\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFfdCH7Ok_PC9Pg0h98qxELciBEflFlEnYbDJwqtrp7c-ODXdxudIPyS_yVc8BINZkr5-vZ7S88pDY8vwhWqyvzlfS_WmI_nnWish5qCrEA2S2-fsCe9_Kh3IJ7jfvWSp5Vx4wcnN0=)\n\n*   **더함 Multiple TV 스마트 55 UHD 120HZ 돌비 AI 구글3.0 게이밍**\n    *   **가격대:** 39만원 ~ 47만원\n    *   **주요 특징:** 55인치 4K UHD 해상도, 120Hz 주사율 지원, 돌비비전 IQ 및 HDR10 지원, 구글 TV OS 내장, 2년 무상 A/S 제공.\n    *   **추천 이유:** 합리적인 가격에 120Hz 주사율과 구글 TV OS를 제공하여 게이밍과 다양한 OTT 서비스 이용에 모두 적합한 가성비 모델입니다.\n    *   **출처:** [노써치](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHboZvbm5llAB8spGDIQxfjDvisqlV7b-IvepOxxo88B5rhtWehRYXBRYSTIEy07o22KRcd_N8x3w-dRJZFT6hCjras9pJDYs2kIIDIiax6qx2KD7buQf1_raNdlpnjehg47FDSYE8qmTdDRiqVclng4TifvnlIADU4Tp3YnDmQdk5LOW2UcLEM0AVj9zCXlrpP-g==)\n\n*   **이스트라 UC552QLED SMART THE MAXIMUM**\n    *   **가격대:** 56만원대\n    *   **주요 특징:** QLED 패널, 3세대 구글 스마트 TV, 120Hz 주사율, HDMI 2.1 및 ALLM 등 게이밍 기능, 논 글레어 스크린 적용.\n    *   **추천 이유:** QLED 패널과 120Hz 주사율을 갖춰 선명한 화질과 부드러운 화면을 제공하며, 게이밍과 OTT 시청 모두에 만족스러운 경험을 선사합니다.\n    *   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGj3hnfsyM6xbuYWmjW-XJDQlpML7OTGqSW-ZXk1D15CAYudP7E7CwPqQTRfPMw_mk7RJC2aA-xxgU_KuMXS1UfTxUNDUDpr6zFw0ntbPdSDSIsHpKrU1XDXtBCLgw6gORyEZ-_Me90P_bU3Fenyd1cyB7fuK_tC6DTa2flSno_x-GMjQ==)\n\n*   **TCL 4K UHD TV**\n    *   **가격대:** 30만원대 ~ 40만원대\n    *   **주요 특징:** 합리적인 가격의 4K UHD 스마트 TV, 안드로이드/구글 TV OS 탑재, 돌비 비전 및 HDR10 지원, 24개월 무상 AS.\n    *   **추천 이유:** 최소한의 예산으로 55인치 4K 스마트 TV를 구매하고자 할 때 가장 좋은 가성비를 제공하며, 필수적인 스마트 기능과 AS를 지원합니다.\n    *   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGxoQbFhoe5kgXTJGk-S8FsoL_fSMVTA64MLcL1hvilE84FBMPDnQULFWT8BzIPbUep8U2hItZNZyS01IHJwoGBgb8sz0sLZ-Poe5EegwwB7X7716RrhGkR_rmDAbuuRj4AtP5GEO4=)",
      "sources": [],
      "response_time_ms": 73487.15,
      "status_code": 200,
      "timestamp": "2025-06-26T05:18:55.635660",
      "error": null
    },
    {
      "test_id": 25,
      "query": "카페에서 쓸 블루투스 스피커 추천, 휴대용으로 10만원 이하",
      "response": "10만원 이하 휴대용 블루투스 스피커로 카페에서 사용하시기 적합한 제품들을 추천해 드립니다.\n\n*   **앤커 사운드코어 3 (Anker Soundcore 3 A3117)**\n    *   **가격대:** 5만원대 (쿠폰 적용 시)\n    *   **주요 특징:** 100% 티타늄 드라이버로 깔끔한 사운드, 24시간 재생 가능한 긴 배터리, IPX7 방수, USB-C 충전.\n    *   **추천 이유:** 가성비가 뛰어나며, 긴 배터리 시간과 깔끔한 음질로 카페에서 장시간 사용하기에 적합합니다.\n    *   **구매 링크:** [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEl1TmhSe5bfi3lZZmloYzVlmhO983cEgd45dX8x5IdE4nRjnidCsyKtOEt3hbUmqc4KlGM71zcAJJC5LJGaU5PYAd8KMBsFzSojMm3AdIKyfFhn2qTPoXIrIM9MLbS44VY2ZR7T-TeINF3cwEVkhsYA7zXk8MiQGBT3G1gabT3ycnmfnLSIHANii8WCOnAHzFI1DXePRkvAEVWVgPYHmkI5u46hJIDXVSL8NzkKg3rjTANepAGcw0Zk3de8PMuz9_kM4BBDYeJ5DGXS2kXF9puw8KzQMaY01WJcHiwgg==](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEl1TmhSe5bfi3lZZmloYzVlmhO983cEgd45dX8x5IdE4nRjnidCsyKtOEt3hbUmqc4KlGM71zcAJJC5LJGaU5PYAd8KMBsFzSojMm3AdIKyfFhn2qTPoXIrIM9MLbS44VY2ZR7T-TeINF3cwEVkhsYA7zXk8MiQGBT3G1gabT3ycnmfnLSIHANii8WCOnAHzFI1DXePRkvAEVWVgPYHmkI5u46hJIDXVSL8NzkKg3rjTANepAGcw0Zk3de8PMuz9_kM4BBDYeJ5DGXS2kXF9puw8KzQMaY01WJcHiwgg==) (쿠팡)\n    *   **출처:** 피자헛둘셋넷, 리뷰존, YouTube\n\n*   **소니 SRS-XB100**\n    *   **가격대:** 6만원대\n    *   **주요 특징:** 약 274g의 가벼운 무게, IP67 방수/방진, 최대 16시간 배터리, 소니만의 균형 잡힌 음질.\n    *   **추천 이유:** 휴대성이 뛰어나면서도 음질과 내구성이 우수하여 카페 내에서 이동하며 사용하거나 다양한 환경에서 안정적인 사운드를 제공합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cxlx7L](https://link.coupang.com/a/cxlx7L)\n    *   **출처:** YouTube, ABC데일리\n\n*   **QCY SP7 PLUS**\n    *   **가격대:** 4만원대\n    *   **주요 특징:** 최대 40W의 강력한 출력 (고음 10W + 저음 30W), IPX7 방수, 14시간 연속 사용.\n    *   **추천 이유:** 저음이 강조된 강력한 사운드를 제공하여 넓은 카페 공간에서도 충분한 볼륨감을 원할 때 적합합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cxly7G](https://link.coupang.com/a/cxly7G)\n    *   **출처:** ABC데일리\n\n*   **JBL GO 3**\n    *   **가격대:** 5~6만원대\n    *   **주요 특징:** 200g 이하의 초경량, IP67 방수.\n    *   **추천 이유:** 휴대성이 매우 뛰어나 카페 내에서 위치를 자주 변경하거나 작은 공간에서 가볍게 사용하기에 좋습니다.\n    *   **구매 링크:** 정보 없음\n    *   **출처:** ABC데일리, 가성비 블로그\n\n*   **필립스 TAS2307**\n    *   **가격대:** 3만원대\n    *   **주요 특징:** 5W 출력, IPX4 생활 방수, 7시간 연속 사용, 200g 무게.\n    *   **추천 이유:** 매우 저렴한 가격과 가벼운 무게로 부담 없이 구매하여 작은 카페 공간이나 개인 작업 공간에서 사용하기에 적합합니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cxlwP6](https://link.coupang.com/a/cxlwP6)\n    *   **출처:** ABC데일리",
      "sources": [],
      "response_time_ms": 89907.39,
      "status_code": 200,
      "timestamp": "2025-06-26T05:20:25.545447",
      "error": null
    },
    {
      "test_id": 26,
      "query": "아이패드 케이스 추천, 11인치 프로용 키보드 분리형으로",
      "response": "아이패드 프로 11인치용 키보드 분리형 케이스를 찾으시는군요. 다음은 주요 추천 제품들입니다.\n\n*   **Apple 정품 매직 키보드**\n    *   **가격대:** 448,200원\n    *   **주요 특징:** 맥북 수준의 우수한 타이핑 키감, 백라이트 키, 트랙패드 내장, 스마트 커넥터로 간편하게 연결 및 충전됩니다. 아이패드 프로 11인치 M4 모델용으로 최적화되어 있습니다.\n    *   **추천 이유:** 타이핑 작업이 많고 아이패드를 노트북처럼 활용하려는 사용자에게 최적의 경험을 제공하는 프리미엄 제품입니다.\n    *   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGgH-XzWafkomwqxHB6Mj6dhiWS5RvF4EbOGfeMMHqFDACD23g0z9OX6zJ3OdAh2goTXgzi90qELIF4O7uO4EK8Mun-_S_YDRfW0GW6-JL-_bm7fmZKQc7W7T02lFvNhuFRcoWSKo8=)\n\n*   **로지텍 콤보 터치 키보드 케이스**\n    *   **가격대:** 20만원대 후반 ~ 40만원대 (정품 315,000원, 영문 자판 419,000원, 해외구매 240,800원)\n    *   **주요 특징:** 분리형 키보드 디자인으로 필요에 따라 탈착 가능하며, 정밀한 트랙패드와 다양한 각도 조절이 가능한 킥 스탠드를 제공합니다. 스마트 커넥터로 연결 및 자동 충전되며, 케이스가 아이패드 측면을 보호합니다.\n    *   **추천 이유:** 애플 매직 키보드의 훌륭한 대안으로, 쫀득한 키감과 정밀한 트랙패드를 제공하며 아이패드 보호 기능까지 겸비하여 휴대성과 생산성 향상에 기여합니다.\n    *   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEa1Gb2HTmLzTptClAweI82q3aDC2sF90oXhvDPHelU9WpzKh_caLaj-RM7-S3_hmbGqf4klHbxWDirS_SCGc59HIAyFrMGYYZDAXxw0Plu5D_eC5xIPhxh_8TIME5WaCDHLOSeA4euTOzIZ45LflY2QnbOg1lILuxgL0c9QMzrZ1h90Oz02x0BacGXuB6QX), [다나와](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEXXEXxR8yDLHYE4Y0irkmLXTDp1ID1KyBeqSkQrMc4t8yw8sVGXJ2iAcnIV9ABFd41bRNy7RyQnpXb_GI2puMSgHtys3dkokJX2geg33uMfT-0AHm05D3oBcIBa9RCzj66ljJ7rM7eu9RESnepMu30mCDxKAPMWCrBkP7mBNg8EzVbZDm0lDrIK0ikdp3U6Mj-OS-YXxAQ9OgPM29drrgAI_yyK2W3znDDB2-QOIm0RbfL41rHzs6GqNpci99z0PmOm7AKtW1voAEVeZov4Ttyx0JbZDr0uONV0JD4Pj0ERK_rD1UQ_lT_hLas5CvR5CDdaQ==)\n\n*   **ESR 블루투스 키보드 케이스**\n    *   **가격대:** (정보 없음)\n    *   **주요 특징:** 분리형 키보드와 마그네틱 커버로 구성되어 있으며, 다양한 각도 조절과 가로/세로 모드를 지원합니다. 확장된 초민감 멀티터치 트랙패드와 백라이트 키보드를 갖추고 있습니다. iPad Pro 11인치(2024) 모델과 호환됩니다.\n    *   **추천 이유:** 애플 매직 키보드 대비 합리적인 가격으로 유사한 사용감을 제공하며, 휴대성과 디자인이 우수하여 대학생 및 직장인에게 유용합니다.\n    *   **출처:** [Google 쇼핑](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGPePou7gurGvV2ATiPW_flZXz1W_wf2E5WXfUGnR7U7ATHISq9pVJtkYBZ-7eQW6bpXjxViVjGQW_6__hk_N24M-Vtah6y6eUzLWySxSUdh6wnS0u27u1NnfsETn77uE3K9C_HABysE_BFP1BAvA==), [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFt4wfIvnEhiKB1AxkNXxmi7Kwq_N_XwDlu9rnUVU7isd8H-mrZ-bNsJs0SuOLz_J4j_VhNVuC_S8cokhzn6aQsOqBR4mSNDuPR5SIrUQQ26bELcJnk_8VJvz_1tyMQfw_MqM1AvO-UX7e1Bg==)\n\n*   **GOOJODOQ 매직 키보드 케이스**\n    *   **가격대:** 11만원대 (알리익스프레스)\n    *   **주요 특징:** 자기 분리형 RGB 키보드 커버로, 트랙패드와 백라이트 기능을 제공합니다. 캔틸레버 디자인으로 다양한 각도 조절이 가능하며, 맥북 스타일 제스처를 지원합니다. 아이패드 프로 11인치 모델과 호환됩니다.\n    *   **추천 이유:** 저렴한 가격에 트랙패드와 백라이트 등 고급 기능을 제공하며, 맥북 스타일 제스처를 지원하여 가성비가 뛰어납니다.\n    *   **구매 링크:** [https://s.click.aliexpress.com/e/\\_ol7rlTp](https://s.click.aliexpress.com/e/_ol7rlTp)\n    *   **출처:** [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFECck6RRlzu-ue_ntnKUyLTaxy73pXBL-N9m2MdBbNbMW9FVMuuGDDs7luGDa0hgwlNgmwTFgDtDxWiEOuk-d1_ggsyS5t1-G9vio-HqIxeQ2AMgHNRz3NYt1tiDQoA1PAP7JY6YM=)\n\n*   **HOU 키보드 케이스**\n    *   **가격대:** 59,900원 (과거 할인가 기준, 현재 가격 변동 가능성 있음)\n    *   **주요 특징:** 분리형 키보드로, 세로/가로 모드 전환 등 다양한 각도 조절이 가능합니다. 애플 펜슬 수납 공간과 슬림한 디자인이 특징입니다.\n    *   **추천 이유:** 가성비가 뛰어나며, 빠른 블루투스 연결과 만족스러운 터치패드 반응 속도를 제공하여 합리적인 가격에 분리형 키보드 케이스를 찾는 사용자에게 적합합니다.\n    *   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEqPEQ4dPYjX9yCZ2qrzYnchl0NFhLL5ZvEqNXnK2itLfb0uFeWNAh1XtPeQP_s97InZAt2KMD-Cn1hta-Hywb-_9EZxznT0Hc0OIiwdMw4Xjkd6h8Q1SxZKVQrlA9xFjbLO2i2ioM6pfku8deKwVomUk3_X3Hvsh3p)",
      "sources": [],
      "response_time_ms": 80108.47,
      "status_code": 200,
      "timestamp": "2025-06-26T05:21:45.657049",
      "error": null
    },
    {
      "test_id": 27,
      "query": "게이밍 체어 추천, 장시간 앉아도 편한 걸로 30만원 이내",
      "response": "장시간 앉아도 편안한 30만원 이내 게이밍 체어를 찾으시는군요. 다음은 여러 커뮤니티 및 제품 정보를 바탕으로 추천하는 제품들입니다.\n\n---\n\n### 1. 시디즈 T50\n*   **가격대:** 20만원대 후반 ~ 30만원대 초반\n*   **주요 특징:** 안정감 있는 머리 받침대, 클라우드폼 좌판 쿠션, 넓은 요추 지지대, 프로텐션 메쉬 소재로 쾌적함 유지, 싱크로나이즈드 틸팅.\n*   **추천 이유:** 디시 갤러리에서 인기가 많으며, 세밀한 조절이 가능하여 사용자 체형에 맞게 조절하기 좋습니다. 특히 요추 통증으로 고생하는 분들에게 적합하다는 평이 많아 장시간 착석 시 허리 부담을 줄여줍니다.\n*   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEKlxLmq-ysHDYfJyzqfHIAAVDoJIuhroK4WSy-6fvNqTz3RGICrgU3-MWUr3wdbpt7isYs_VWw9YhikrMYageCEwbNF2yxReHexVNHtifVaHH4inGSpq3vvgau7p1iaslc6KUkfWz8JzExbM4-0df5fagF4rNLRg==), [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXL_rHv1_QtlQeoacidfjKotiVSUWk4ELtBb0LF_hik2_sorWpGueRN4TgYFLdYY5rZyVZCfhjX93WhqPcemwHnRHqYrY3w6FrnA1xSU_zYVCi158Zf3q7MYM1-flzRiTQRA==4)\n\n### 2. 클라우드백 마이사이즈 체어 M900MQ\n*   **가격대:** 30만원대 초반\n*   **주요 특징:** 자신의 키와 체형에 맞게 S~XL 사이즈 선택 가능, 메쉬 등판 및 좌판으로 통기성 우수, 틸팅/강도/높낮이/팔걸이 조절 가능, 윙/헤드/요추/팔 쿠션의 경도 조절 가능.\n*   **추천 이유:** 체형에 딱 맞는 사이즈를 선택할 수 있어 최적의 편안함을 제공합니다. 푹신한 착화감을 선호하며 장시간 앉아있을 때 편안함을 극대화하고 싶은 분들에게 추천됩니다.\n*   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXL_rHv1_QtlQeoacidfjKotiVSUWk4ELtBb0LF_hik2_sorWpGueRN4TgYFLdYY5rZyVZCfhjX93WhqPcemwHnRHqYrY3w6FrnA1xSU_zYVCi158Zf3q7MYM1-flzRiTQRA==), [클라우드백 공식 홈페이지](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXL_rHv1_QtlQeoacidfjKotiVSUWk4ELtBb0LF_hik2_sorWpGueRN4TgYFLdYY5rZyVZCfhjX93WhqPcemwHnRHqYrY3w6FrnA1xSU_zYVCi158Zf3q7MYM1-flzRiTQRA==0)\n\n### 3. 듀오백 브라보 BR-200CW\n*   **가격대:** 30만원대 초반\n*   **주요 특징:** 등판과 좌판이 움직임에 맞춰 다른 각도로 기울어지는 인체공학적 설계, 알루미늄 다이캐스팅 프레임, 최첨단 인간공학 트위스트백, 등판 메쉬로 통기성 및 탄력성 우수.\n*   **추천 이유:** 견고한 내구성과 함께 사용자의 움직임에 맞춰 유연하게 반응하는 설계로 장시간 앉아있어도 편안함을 유지합니다. 튼튼한 의자를 선호하는 분들에게 적합합니다.\n*   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEKlxLmq-ysHDYfJyzqfHIAAVDoJIuhroK4WSy-6fvNqTz3RGICrgU3-MWUr3wdbpt7isYs_VWw9YhikrMYageCEwbNF2yxReHexVNHtifVaHH4inGSpq3vvgau7p1iaslc6KUkfWz8JzExbM4-0df5fagF4rNLRg==), [디시인사이드](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyyqbW3Wi0kvGYRNAt1CfL91Qb--kh--Vo9iK7-LYxtZqcwZK3XyKVZ0_lUx4SEBQbwVpwub-AZz81SR8HvIes8cmgk_S-1Fexz6YpAcgCNURTzdr2NVDdUJUQ8)\n\n### 4. 제닉스 아레나 TYPE-1\n*   **가격대:** 10만원대 후반 ~ 20만원대 초반\n*   **주요 특징:** 강한 내구성을 가진 풀 메탈 프레임, 프리미엄 레더 사용, 고품질 PU Cold Cure Form으로 탄력성 및 복원력 우수, 최대 180도 등받이 조절 가능.\n*   **추천 이유:** 게이머들 사이에서 높은 인기를 얻고 있는 제품으로, 튼튼한 내구성과 편안한 쿠션감을 제공합니다. 180도 틸팅 기능으로 휴식 시에도 편안하게 사용할 수 있습니다.\n*   **출처:** [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXL_rHv1_QtlQeoacidfjKotiVSUWk4ELtBb0LF_hik2_sorWpGueRN4TgYFLdYY5rZyVZCfhjX93WhqPcemwHnRHqYrY3w6FrnA1xSU_zYVCi158Zf3q7MYM1-flzRiTQRA==), [유튜브](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG88fry1fu1-rhrJ87uGR-5pO8Ds2tn3DXcz-PunBBLAJRhLgHaGk8KPA86vasEq3BTIOxnehmTuYHav55HEN12WI1dIdsiNle1tGfD8MaEEyT10fy49bdKtWoxC_e-HSYXR6iIbJwv3IFZ)\n\n### 5. 다임체어 DG04\n*   **가격대:** 30만원 초반대\n*   **주요 특징:** 국내 제조, 고밀도 스펀지, 큼직한 등받이, 방문 설치 서비스 제공.\n*   **추천 이유:** 방석이 푹신하고 넓어 편안하며, 허리 지지력이 좋아 오래 앉아도 편안하다는 사용자 평이 있습니다. 국내 제조 및 방문 설치 서비스로 신뢰도를 더합니다.\n*   **구매 링크:** [쿠팡](https://link.coupang.com/a/cjWIlv)\n*   **출처:** [YouTube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHYXA9hSrBjpX1ZqRQhvZqbtfxtvPZfDyNHxy4-obnCPstKAKdwsFqhr-s4AoqTpymH1CmiuN3UFfYpeBPv9YiivJRvsVaWEoZ51GtB-h4JgQXLreD2HoT91uERZ18pcvyHen9QHQ==)",
      "sources": [],
      "response_time_ms": 79154.51,
      "status_code": 200,
      "timestamp": "2025-06-26T05:23:04.814218",
      "error": null
    },
    {
      "test_id": 28,
      "query": "외장하드 추천, 2TB 이상 용량으로 가격 저렴한 걸로",
      "response": "2TB 이상 용량의 저렴한 외장하드를 찾으시는 사용자님께 다음 제품들을 추천합니다.\n\n1.  **WD Elements Portable**\n    *   **가격대:** 119,900원\n    *   **주요 특징:** USB 3.0 지원, 윈도우 및 맥에서 모두 사용 가능, 휴대성이 좋습니다.\n    *   **추천 이유:** 뛰어난 가성비와 안정성으로 개인 데이터 백업에 최적화된 제품입니다.\n    *   **출처:** [Gogoon의 디지털 세상](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYtNf86yYdoBDvvDWGENQCN7nmwpfPhHeAfSPQWIT5Ex9i-9k5zuKHM1K7B_SZ2ipsDUfNDHSREOxFYiFitQT9bK34nWCnUkZeqGkinrbq0D1lJRGqcf3kfWECAtEWdZFHpZPbGov3W7Y1UwL1PVIDaljRyveTNUHGUKDhiFjhl-qjN8r5B2TP31EXkguWeGfoBqszA2hMAF50UmakvseHPHEEFZ32CZM2qeviQ7hi9EZl4kaBw3u5lpO8bYtA73JFjA4-LtgrSF0ib82rZjEH0XrjNGTF9rhQ97wIsqj3ZCRspdjraKgs17z5kpm6K8wkdq-RpDOqtrxo3vAHh-Jtlmu555_Ia6so733S6uw9f3cRwyQi_qhbq5WuDCTylhw81anj4oZdmkkIH2Vd7VOv-61vbB9Dyw-QksH1C88POpSGgvqPANvvqG1c)\n\n2.  **도시바 Canvio Advance 2세대**\n    *   **가격대:** 124,900원\n    *   **주요 특징:** 비밀번호 보호 소프트웨어 제공, USB 3.0 지원, 파우치 세트가 함께 제공됩니다. 소형 디자인과 다양한 색상 옵션이 있습니다.\n    *   **추천 이유:** 안정적인 데이터 백업이 가능하며, 합리적인 가격과 가성비를 갖춘 제품입니다.\n    *   **구매 링크:** [쿠팡](https://link.coupang.com/a/cy18Ph)\n    *   **출처:** [Gogoon의 디지털 세상](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYtNf86yYdoBDvvDWGENQCN7nmwpfPhHeAfSPQWIT5Ex9i-9k5zuKHM1K7B_SZ2ipsDUfNDHSREOxFYiFitQT9bK34nWCnUkZeqGkinrbq0D1lJRGqcf3kfWECAtEWdZFHpZPbGov3W7Y1UwL1PVIDaljRyveTNUHGUKDhiFjhl-qjN8r5B2TP31EXkguWeGfoBqszA2hMAF50UmakvseHPHEEFZ32CZM2qeviQ7hi9EZl4kaBw3u5lpO8bYtA73JFjA4-LtgrSF0ib82rZjEH0XrjNGTF9rhQ97wIsqj3ZCRspdjraKgs17z5kpm6K8wkdq-RpDOqtrxo3vAHh-Jtlmu555_Ia6so733S6uw9f3cRwyQi_qhbq5WuDCTylhw81anj4oZdmkkIH2Vd7VOv-61vbB9Dyw-QksH1C88POpSGgvqPANvvqG1c)\n\n3.  **씨게이트 One Touch HDD**\n    *   **가격대:** 135,000원\n    *   **주요 특징:** 데이터 복구 서비스와 암호화 기능을 제공하여 데이터 보안에 강점이 있습니다. 파우치와 USB 케이블이 함께 제공됩니다.\n    *   **추천 이유:** 데이터 보안 및 복구 기능이 중요하고, 디자인과 사용 편의성을 중시하는 사용자에게 적합합니다.\n    *   **구매 링크:** [쿠팡](https://link.coupang.com/a/ciRJr9)\n    *   **출처:** [2TB 외장하드 가성비 추천 디시](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNJIX4rAZ2MXA9H5BtszmyxlUa5SpAnL0ic1v57O6Pw3ATHltvZUFscuNtm2yK1hhYYYuMzJiIgfbnV2wxQ92JVwQkaIHmA-XytB3e11Z6uN1MlleP0MmjKgNbrPuEsR5qoduDUo8=)\n\n4.  **WD My Passport**\n    *   **가격대:** 124,900원\n    *   **주요 특징:** 휴대성이 좋으며, 파우치가 함께 제공됩니다.\n    *   **추천 이유:** 휴대성을 중요하게 생각하고 안정적인 WD 브랜드 제품을 선호하는 사용자에게 적합합니다.\n    *   **구매 링크:** [쿠팡](https://link.coupang.com/a/cy18O3)\n    *   **출처:** [외장하드 2TB 이상 추천 정보 종합](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrGeDP7uZAGg2GLUKMLHPdQsKaOPgG7-BPX6acuqROZO5LEUbkD6kvxNyjRi-HCztJVPuGvf0YvQxXNSkV7XL5N8wj709iToRijcgj1foKEz5WcTT64V6CG47WcQK79QruY8y7lKs=)\n\n5.  **삼성전자 J3 Portable**\n    *   **가격대:** 139,000원\n    *   **주요 특징:** 슬림하고 고급스러운 디자인이 특징이며, 파우치가 함께 제공됩니다.\n    *   **추천 이유:** 삼성 브랜드의 신뢰성과 세련된 디자인, 좋은 휴대성을 선호하는 사용자에게 적합합니다.\n    *   **구매 링크:** [쿠팡](https://link.coupang.com/a/cy18Pa)\n    *   **출처:** [외장하드 2TB 이상 추천 정보 종합](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrGeDP7uZAGg2GLUKMLHPdQsKaOPgG7-BPX6acuqROZO5LEUbkD6kvxNyjRi-HCztJVPuGvf0YvQxXNSkV7XL5N8wj709iToRijcgj1foKEz5WcTT64V6CG47WcQK79QruY8y7lKs=)",
      "sources": [],
      "response_time_ms": 80438.96,
      "status_code": 200,
      "timestamp": "2025-06-26T05:24:25.256025",
      "error": null
    },
    {
      "test_id": 29,
      "query": "차량용 블랙박스 추천, 전후방 녹화 가능한 20만원 이하",
      "response": "20만원 이하 전후방 녹화 가능한 차량용 블랙박스를 찾으시는군요. 다음은 가격 대비 성능이 우수하고 사용자들에게 추천되는 제품들입니다.\n\n---\n\n### 1. 아이나비 FXD8500\n*   **가격대:** 10만원 중반 ~ 189,000원\n*   **주요 특징:** 전후방 FHD 화질, 전방 170도 시야각, 저전력 주차 녹화, ADAS(첨단 운전자 보조 시스템) 지원, GPS 기능.\n*   **추천 이유:** 국내 탑 브랜드 아이나비의 제품으로 안정적인 성능과 완성도를 자랑하며, AS가 용이하여 가성비가 매우 우수합니다.\n*   **구매 링크:** [쿠팡](https://link.coupang.com/a/ciGVOs)\n*   **출처:** [[2], [6]], [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFas5nI_BmHSZ8Mu0kT9DcU_FKHbI_sWAwcpULYTYSYOmQ0miTrSH-L18Ce4OaEYQVn-lDmE6YfpISYHLtMGufJH3A4mKWPP9mdwIR7_BmKGW_drtqzWCpa0aCjdBcwoRE-yCE6JUnebE1-jiL)\n\n### 2. 파인뷰 X550\n*   **가격대:** 20만원 초반 (32GB 기준)\n*   **주요 특징:** 전후방 QHD 화질, 소니 스타비스 이미지 센서, 오토 나이트 비전, GPS 내장, Wi-Fi 연동.\n*   **추천 이유:** QHD 고화질로 야간에도 번호판 식별이 용이하며, 스마트폰 연동이 편리하여 선명한 영상과 다양한 기능을 활용하고 싶은 분께 적합합니다.\n*   **구매 링크:** [쿠팡 (32GB)](https://link.coupang.com/a/ciwugg), [쿠팡 (64GB)](https://link.coupang.com/a/ci89oE), [쿠팡 (128GB)](https://link.coupang.com/a/ci89tb)\n*   **출처:** [[2], [9]], [네이버 블로그](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEqH2iisHefnJirSLnpy6kpWN-rnxx9YDS8ei2NI4Uz6JnqJtwN2KjCbP4dEoY9jDJg3Wlu3lyQwLCCgsfFcWD10x7xUiK_DCjmzLkmrWvmtSzztJrn7iBto2ioiQzmeVBjjUeWIh7CmrZr)\n\n### 3. 70mai A810\n*   **가격대:** 10만원 중반\n*   **주요 특징:** 전방 4K, 후방 FHD 화질, 전방 150도 시야각, 소니 스타비스 2 이미지 센서, 5GHz Wi-Fi 지원.\n*   **추천 이유:** 가격 대비 뛰어난 4K 전방 화질을 제공하며, 콤팩트한 디자인과 빠른 5GHz Wi-Fi 연동이 장점입니다.\n*   **구매 링크:** [쿠팡](https://link.coupang.com/a/cwakl1), [쿠팡 (메모리 카드)](https://link.coupang.com/a/ci9bEz)\n*   **출처:** [[2], [7]]\n\n### 4. 파인뷰 X3300 NEW\n*   **가격대:** 18만원대 (189,000원)\n*   **주요 특징:** 전방 QHD, 후방 FHD 화질, 배터리 방전 방지 기능, Wi-Fi를 통한 스마트폰 연동.\n*   **추천 이유:** 20만원 이하 가격대에서 전방 QHD 화질을 제공하며, 배터리 보호 기능과 스마트폰 연동 편의성을 갖춘 제품입니다.\n*   **출처:** [[6]], [티스토리](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFvNUjOkoHhqFkRTmITkB8Cct066C43jmKg3jIDnWjpAMc_t0tLOqKOHGf_nJma1Dq7T8aPu5-EncA6XTII5dUJMjNifoxPNi4wqIobYTjO3I4eQHS74HxDhOk=)\n\n### 5. 바넥스 BX7W\n*   **가격대:** 10만원 이하\n*   **주요 특징:** 전후방 FHD 화질, 울트라 나이트 비전, 140도 광시야각 렌즈, 스마트폰 연동, 무료 출장 설치.\n*   **추천 이유:** 10만원 이하의 뛰어난 가성비를 자랑하며, 무료 출장 설치 서비스까지 제공되어 비용 부담 없이 전후방 블랙박스를 장착하고 싶은 분께 적합합니다.\n*   **구매 링크:** [쿠팡](https://link.coupang.com/a/cnoFix)\n*   **출처:** [[11], [22], [32]]",
      "sources": [],
      "response_time_ms": 88210.59,
      "status_code": 200,
      "timestamp": "2025-06-26T05:25:53.469826",
      "error": null
    },
    {
      "test_id": 30,
      "query": "무선충전패드 추천, 아이폰 갤럭시 둘 다 지원하는 5만원 이하",
      "response": "아이폰과 갤럭시를 모두 지원하며 5만원 이하의 무선 충전 패드를 찾으신다면 다음 제품들을 추천합니다.\n\n1.  **바우아토 아이폰 갤럭시 3in1 듀얼 코일 고속 무선충전기 거치대**\n    *   **가격:** 26,800원\n    *   **주요 특징 및 추천 이유:** 아이폰과 갤럭시를 동시에 충전할 수 있는 3in1 제품으로, 듀얼 코일 방식과 쿨링 기능으로 발열이 적어 안정적인 고속 충전이 가능합니다. 깔끔하고 심플한 디자인에 거치대 기능까지 제공하여 실용적입니다.\n    *   **구매 링크:** [https://smartstore.naver.com/artmu/products/4891133596](https://smartstore.naver.com/artmu/products/4891133596)\n    *   **출처:** 바우아토 스마트 스토어\n\n2.  **SPEEDY 15W 고속 무선충전 거치대**\n    *   **가격:** 7,900원\n    *   **주요 특징 및 추천 이유:** 매우 저렴한 가격에도 15W 고속 무선 충전을 지원하며, 다양한 스마트폰 기기와 호환됩니다. 거치대 형태로 편리하게 사용할 수 있으며, 과열 및 과충전 방지 기능도 갖추고 있습니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cxOXoX](https://link.coupang.com/a/cxOXoX)\n    *   **출처:** YouTube\n\n3.  **홈플래닛 광폭 듀얼코일 PD15W 무선고속충전 탁상용 거치대**\n    *   **가격:** 9,890원\n    *   **주요 특징 및 추천 이유:** 광폭 듀얼 코일을 사용하여 충전 효율을 높였으며, PD 15W 고속 무선 충전을 지원합니다. C타입 케이블이 포함되어 있으며, 합리적인 가격으로 아이폰과 갤럭시 모두 사용 가능한 가성비 제품입니다.\n    *   **구매 링크:** [https://link.coupang.com/a/cxOXo2](https://link.coupang.com/a/cxOXo2)\n    *   **출처:** YouTube\n\n4.  **아트뮤 15W 고속 무선충전기 WC810**\n    *   **가격:** 약 2만원\n    *   **주요 특징 및 추천 이유:** 깔끔한 디자인과 함께 최대 15W 고속 충전을 지원합니다 (아이폰은 7.5W). 과전압/과전류 보호회로 및 FOD(이물질 감지) 센서 등 안전 기능이 탑재되어 있으며, 2년 A/S를 제공하여 신뢰할 수 있습니다.\n    *   **출처:** 노써치\n\n5.  **이어맥 4IN1 스마트폰+워치 무선충전 패드**\n    *   **가격:** 39,900원\n    *   **주요 특징 및 추천 이유:** 스마트폰뿐만 아니라 갤럭시 워치와 애플 워치까지 동시에 충전할 수 있어 여러 기기를 사용하는 분들께 특히 유용합니다. 5만원 이하 가격대에서 다양한 기기 동시 충전 기능을 제공하는 실용적인 선택입니다.\n    *   **출처:** 티스토리",
      "sources": [],
      "response_time_ms": 82628.23,
      "status_code": 200,
      "timestamp": "2025-06-26T05:27:16.100093",
      "error": null
    }
  ]
```