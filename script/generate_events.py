from faker import Faker
from datetime import UTC
import random, uuid

# click 이벤트 목록
CLICK_SET = [
  {"click_event_name":"video_play", "element_type":"button"}, 
  {"click_event_name":"open_course", "element_type":"a"},  
  {"click_event_name":"like_course", "element_type":"button"},  
  {"click_event_name":"checkout", "element_type":"button"},    
  {"click_event_name":"search_course", "element_type":"input"}  
]

# purchase 이벤트 목록
PRODUCTS = [
  # 개발
  {"product_id": 1100, "product_name": "비전공자도 3일 만에 끝내는 파이썬 웹 크롤러", "product_category": "development"},
  {"product_id": 213, "product_name": "제작코드가 눈에 들어오는 자바스크립트(JS) 핵심 개념 탑재", "product_category": "development"},
  {"product_id": 3008, "product_name": "에러 메시지가 두렵지 않은 개발자를 위한 디버깅 기술", "product_category": "development"},
  {"product_id": 499, "product_name": "Chat GPT를 나만의 수석 개발자로 고용하는 프롬프트 비법", "product_category": "development"},
  {"product_id": 145, "product_name": "단 한 권으로 끝내는 프론트엔드 포트폴리오 실무 가이드", "product_category": "development"},

  # 데이터 분석 & AI
  {"product_id": 6, "product_name": "데이터 분석가들이 실무에서 매일 쓰는 SQL 핵심 치트키", "product_category": "data_ai"},
  {"product_id": 7, "product_name": "엑셀에서 벗어나자! 파이썬 데이터 시각화 첫걸음", "product_category": "data_ai"},
  {"product_id": 8090, "product_name": "내 업무를 자동화하는 LLM 기반 AI 에이전트 만들기", "product_category": "data_ai"},
  {"product_id": 8, "product_name": "비즈니스 의사결정을 바꾸는 태블로(Tableau) 대시보드 구축", "product_category": "data_ai"},
  {"product_id": 9, "product_name": "숫자로 설득하는 마케터를 위한 데이터 통계학", "product_category": "data_ai"},

  # 클라우드 & devops
  {"product_id": 10, "product_name": "개발자와 싸우지 않는 서비스 기획자의 IT 기술 상식", "product_category": "cloud_devops"},
  {"product_id": 110, "product_name": "클라우드가 처음인 엔지니어를 위한 AWS 기초 아키텍처", "product_category": "cloud_devops"},
  {"product_id": 101, "product_name": "야근을 줄여주는 직장인용 구글 워크스페이스 연동 자동화", "product_category": "cloud_devops"},
  {"product_id": 120, "product_name": "도커(Docker)와 쿠버네티스로 시작하는 컨테이너 환경 구축", "product_category": "cloud_devops"},
  {"product_id": 130, "product_name": "노코드(No-code) 툴로 하루 만에 완성하는 MVP 앱 개발", "product_category": "cloud_devops"},

  # UI_UX
  {"product_id": 300, "product_name": "개발자가 바로 구현할 수 있는 UI_UX 피그마(Figma) 설계", "product_category": "ui_ux"},
  {"product_id": 333, "product_name": "트렌디한 모바일 앱을 위한 다크모드 UI 디자인 가이드", "product_category": "ui_ux"},
  {"product_id": 132, "product_name": "우리 회사 서버를 지키는 주니어 엔지니어용 보안 가이드", "product_category": "ui_ux"},
  {"product_id": 134, "product_name": "퍼블리셔가 알려주는 반응형 웹 디자인 핵심 CSS 기술", "product_category": "ui_ux"},
  {"product_id": 141, "product_name": "1인 개발자를 위한 앱 스토어 출시 및 배포 프로세스 A to Z", "product_category": "ui_ux"},
]

# error 이벤트 목록
ERRORS = [
  # 4xx
  {"error_level" : "WARNING", "error_code": 400, "error_msg": "BAD_REQUEST"},
  {"error_level" : "WARNING", "error_code": 401, "error_msg": "UNAUTHORIZED"},
  {"error_level" : "WARNING", "error_code": 403, "error_msg": "FORBIDDEN"},
  {"error_level" : "WARNING", "error_code": 404, "error_msg": "NOT_FOUND"},

  # 5xx
  {"error_level" : "ERROR", "error_code": 500, "error_msg": "INTERNAL_SERVER_ERROR"},
  {"error_level" : "CRITICAL", "error_code": 502, "error_msg": "BAD_GATEWAY"},
  {"error_level" : "ERROR", "error_code": 503, "error_msg": "SERVICE_UNAVAILABLE"},
  {"error_level" : "CRITICAL", "error_code": 504, "error_msg": "GATEWAY_TIMEOUT"},
]

def generate(size):
# 이벤트 데이터 생성 (dict)
  fake = Faker()

  event_types = ["page_view", "click", "purchase", "error"]
  page_name = ["home", "category", "courses", "player", "search", "checkout"]
  device = ["mobile", "desktop", "tablet"]
  payload = []

  # 공통 payload
  for _ in range(size):
    tmp = {}
    tmp["event_id"] = str(uuid.uuid4())
    tmp["event_type"] = random.choices(event_types, weights=[45, 35, 15, 5], k=1)[0]
    tmp["user_id"] = random.randint(1, 1000)
    tmp["event_time"] = fake.date_time_between(start_date='-1y', end_date='-1d', tzinfo=UTC).isoformat()
    tmp["page_name"] = random.choice(page_name)
    tmp["device"] = random.choice(device)
    payload.append(tmp)

  # 이벤트별 payload
  for i in range(size):
    # click
    if payload[i]["event_type"] == "click":
      payload[i].update(random.choices(CLICK_SET, weights=[50, 30, 10, 5, 20], k=1)[0])
    
    # purchase
    elif payload[i]["event_type"] == "purchase":
      payload[i].update(random.choice(PRODUCTS))
      payload[i]["payment_method"] = random.choices(["card", "pay", "account"], weights=[40, 30, 10])[0]
      payload[i]["price"] = random.randint(990, 100000)

    # error
    elif payload[i]["event_type"] == "error":
      payload[i].update(random.choices(ERRORS, weights=[25, 20, 15, 25, 10, 3, 3, 1])[0])

  return payload