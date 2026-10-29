import os
import urllib.parse
import hashlib
import json
import shutil

# 1. 사이트 기본 설정
SITE_ORIGIN = "https://pyeongtaek-gunma1004-therapy.netlify.app"
SITE_NAME = "건천테라피"
DEFAULT_PHONE = "0507-1280-3296"

# 2. 제휴 업체 목록
PARTNER_SHOPS = [
    {"name": "퀸즈홈테라피", "phone": "0507-1280-3296", "category": "VIP 스페셜", "price": "스페셜 60분 100,000원", "img": "01"},
    {"name": "한국미인테라피", "phone": "0507-1280-3140", "category": "한국인 스웨디시", "price": "스웨디시 60분 140,000원", "img": "02"},
    {"name": "오늘밤테라피", "phone": "0507-1280-3199", "category": "전신 아로마", "price": "아로마 60분 70,000원", "img": "03"},
    {"name": "주주테라피", "phone": "0507-1280-3197", "category": "타이 마사지", "price": "타이 60분 60,000원", "img": "04"},
    {"name": "기쁨테라피", "phone": "0507-1280-3183", "category": "VIP 힐링케어", "price": "힐링 60분 90,000원", "img": "05"},
    {"name": "미인클럽테라피", "phone": "0507-1280-3180", "category": "VIP 스페셜", "price": "스페셜 90분 120,000원", "img": "06"}
]

# 3. 경기·서울·인천 시구동 데이터
REGION_DATA = {
    "gyeonggi": {
        "name": "경기도", "short": "경기",
        "districts": {
            "평택시": ["신평동", "원평동", "통복동", "비전동", "세교동", "고덕동", "팽성읍", "안중읍", "포승읍", "청북읍", "진위면", "서탄면", "고덕면", "월곡동", "현덕면", "오성면"],
            "수원시 장안구": ["파장동", "율천동", "정자동", "영화동", "송죽동", "조원동", "연무동"],
            "수원시 권선구": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "권선동", "곡선동"],
            "수원시 팔달구": ["행궁동", "매교동", "매산동", "고등동", "화서동", "지동", "우만동", "인계동"],
            "수원시 영통구": ["매탄동", "원천동", "영통동", "망포동", "광교동"],
            "화성시": ["남양읍", "향남읍", "봉담읍", "동탄동", "진안동", "병점동", "반월동", "새솔동"],
            "오산시": ["중앙동", "대원동", "남촌동", "신장동", "세마동", "초평동"],
            "안성시": ["안성동", "공도읍", "보개면", "대덕면", "미양면", "원곡면", "일죽면"],
            "용인시 처인구": ["중앙동", "역북동", "삼가동", "유림동", "동부동", "포곡읍", "모현읍"],
            "용인시 기흥구": ["신갈동", "영덕동", "구갈동", "상갈동", "보라동", "기흥동", "서농동", "구성동", "동백동", "마북동"],
            "용인시 수지구": ["풍덕천동", "신봉동", "죽전동", "동천동", "상현동", "성복동"],
            "성남시 분당구": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "판교동", "백현동", "운중동"],
            "성남시 수정구": ["신흥동", "태평동", "수진동", "단대동", "산성동", "복정동", "위례동"],
            "성남시 중원구": ["성남동", "중앙동", "금광동", "은행동", "상대원동", "하대원동", "도촌동"],
            "안양시 만안구": ["안양동", "석수동", "박달동"],
            "안양시 동안구": ["비산동", "부흥동", "달안동", "관양동", "평촌동", "호계동", "범계동"],
            "안산시 단원구": ["와동", "고잔동", "호수동", "원곡동", "백운동", "초지동", "선부동", "대부동"],
            "안산시 상록구": ["일동", "이동", "사동", "본오동", "부곡동", "월피동", "성포동", "반월동"],
            "시흥시": ["대야동", "신천동", "은행동", "매화동", "목감동", "군자동", "정왕동", "배곧동", "능곡동"],
            "군포시": ["군포동", "산본동", "금정동", "재궁동", "오금동", "수리동", "대야동"],
            "의왕시": ["고천동", "부곡동", "오전동", "내손동", "청계동"],
            "광명시": ["광명동", "철산동", "하안동", "소하동", "일직동", "학온동"],
            "부천시 원미구": ["심곡동", "원미동", "중동", "상동", "도당동", "춘의동", "약대동", "역곡동"],
            "부천시 소사구": ["소사본동", "범박동", "괴안동", "송내동", "옥길동"],
            "부천시 오정구": ["성곡동", "원종동", "고강동", "오정동", "신흥동"],
            "김포시": ["김포본동", "장기동", "사우동", "풍무동", "구래동", "마산동", "운양동", "고촌읍"],
            "파주시": ["금촌동", "운정동", "교하동", "문산읍", "조리읍", "법원읍", "파주읍"],
            "고양시 일산동구": ["식사동", "중산동", "정발산동", "풍산동", "백석동", "마두동", "장항동", "고봉동"],
            "고양시 일산서구": ["일산동", "주엽동", "탄현동", "대화동", "송포동", "덕이동", "가좌동"],
            "고양시 덕양구": ["주교동", "원신동", "흥도동", "성사동", "화정동", "행주동", "능곡동", "창릉동", "삼송동"],
            "의정부시": ["의정부동", "호원동", "장암동", "신곡동", "송산동", "자금동", "가능동", "흥선동"],
            "양주시": ["양주동", "회천동", "옥정동", "덕정동", "백석읍"],
            "동두천시": ["생연동", "중앙동", "불현동", "송내동"],
            "포천시": ["포천동", "선단동", "소흘읍", "일동면"],
            "구리시": ["갈매동", "동구동", "인창동", "교문동", "수택동"],
            "남양주시": ["와부읍", "진접읍", "화도읍", "진건읍", "오남읍", "별내동", "다산동", "평내동", "호평동"],
            "하남시": ["천현동", "신장동", "덕풍동", "풍산동", "미사동", "감일동", "위례동"],
            "광주시": ["경안동", "송정동", "광남동", "오포동", "초월읍", "곤지암읍"],
            "이천시": ["창전동", "증포동", "중리동", "관고동", "부발읍"],
            "여주시": ["여흥동", "중앙동", "오학동", "가남읍"],
            "과천시": ["중앙동", "갈현동", "별양동", "부림동"],
            "양평군": ["양평읍", "양서면", "용문면", "서종면"],
            "가평군": ["가평읍", "청평면", "설악면"],
            "연천군": ["연천읍", "전곡읍"]
        }
    },
    "seoul": {
        "name": "서울특별시", "short": "서울",
        "districts": {
            "강남구": ["개포동", "대치동", "도곡동", "일원동", "수서동", "자곡동", "삼성동", "청담동", "압구정동", "신사동", "논현동", "역삼동", "세곡동"],
            "서초구": ["서초동", "반포동", "방배동", "양재동", "잠원동", "내곡동"],
            "송파구": ["잠실동", "문정동", "가락동", "방이동", "석촌동", "오금동", "위례동", "신천동", "풍납동", "거여동", "마천동"],
            "강동구": ["강일동", "상일동", "명일동", "고덕동", "암사동", "천호동", "성내동", "둔촌동", "길동"],
            "영등포구": ["영등포동", "여의동", "당산동", "도림동", "문래동", "양평동", "신길동", "대림동"],
            "구로구": ["신도림동", "구로동", "가리봉동", "고척동", "개봉동", "오류동", "수궁동", "항동"],
            "금천구": ["가산동", "독산동", "시흥동"],
            "관악구": ["봉천동", "신림동", "남현동"],
            "동작구": ["노량진동", "상도동", "흑석동", "사당동", "대방동", "신대방동"],
            "마포구": ["공덕동", "아현동", "도화동", "용강동", "대흥동", "서강동", "서교동", "합정동", "망원동", "연남동", "성산동", "상암동"],
            "용산구": ["후암동", "용산동", "남영동", "청파동", "원효로동", "효창동", "용문동", "한강로동", "이촌동", "이태원동", "한남동", "서빙고동", "보광동"],
            "중구": ["소공동", "회현동", "명동", "필동", "장충동", "광희동", "을지로동", "신당동", "다산동", "약수동", "청구동", "동화동", "황학동", "중림동"],
            "종로구": ["청운동", "사직동", "삼청동", "부암동", "평창동", "무악동", "교남동", "가회동", "종로동", "이화동", "혜화동", "창신동", "숭인동"],
            "성동구": ["왕십리동", "마장동", "사근동", "행당동", "응봉동", "금호동", "옥수동", "성수동", "송정동", "용답동"],
            "광진구": ["중곡동", "능동", "구의동", "광장동", "자양동", "화양동", "군자동"],
            "동대문구": ["용신동", "제기동", "전농동", "답십리동", "장안동", "청량리동", "회기동", "휘경동", "이문동"],
            "중랑구": ["면목동", "상봉동", "중화동", "묵동", "망우동", "신내동"],
            "성북구": ["성북동", "삼선동", "동선동", "돈암동", "안암동", "보문동", "정릉동", "길음동", "종암동", "월곡동", "장위동", "석관동"],
            "강북구": ["미아동", "번동", "수유동", "우이동"],
            "도봉구": ["쌍문동", "방학동", "창동", "도봉동"],
            "노원구": ["월계동", "공릉동", "하계동", "중계동", "상계동"],
            "은평구": ["녹번동", "불광동", "갈현동", "구산동", "대조동", "응암동", "역촌동", "신사동", "증산동", "수색동", "진관동"],
            "서대문구": ["충현동", "천연동", "북아현동", "신촌동", "연희동", "홍제동", "홍은동", "남가좌동", "북가좌동"],
            "양천구": ["목동", "신월동", "신정동"],
            "강서구": ["염창동", "등촌동", "화곡동", "가양동", "마곡동", "방화동", "공항동"]
        }
    },
    "incheon": {
        "name": "인천광역시", "short": "인천",
        "districts": {
            "부평구": ["부평동", "산곡동", "청천동", "갈산동", "삼산동", "부개동", "일신동", "십정동"],
            "계양구": ["효성동", "계산동", "작전동", "작전서운동", "계양동"],
            "서구": ["검암경서동", "연희동", "청라동", "가정동", "석남동", "가좌동", "검단동", "원당동", "당하동", "아라동"],
            "남동구": ["구월동", "간석동", "만수동", "서창동", "논현동", "논현고잔동"],
            "연수구": ["옥련동", "선학동", "연수동", "청학동", "동춘동", "송도동"],
            "미추홀구": ["숭의동", "용현동", "학익동", "도화동", "주안동", "관교동", "문학동"],
            "중구": ["신포동", "연안동", "신흥동", "동인천동", "개항동", "영종동", "운서동"],
            "동구": ["만석동", "화수동", "송현동", "송림동"],
            "강화군": ["강화읍", "길상면", "화도면"],
            "옹진군": ["백령면", "영흥면", "연평면"]
        }
    }
}

def render_cards_html(area_label, dong_name=""):
    seed = int(hashlib.md5(f"{area_label}_{dong_name}".encode('utf-8')).hexdigest(), 16)
    shuffled_shops = PARTNER_SHOPS[:]
    start_idx = seed % len(shuffled_shops)
    ordered_shops = shuffled_shops[start_idx:] + shuffled_shops[:start_idx]

    prefixes = [
        f"{dong_name} " if dong_name else "",
        f"{dong_name} 직영 " if dong_name else "",
        "프라이빗 케어 ",
        "후불 안심 ",
        "힐링 스페셜 "
    ]

    cards_html = ""
    for idx, s in enumerate(ordered_shops):
        prefix = prefixes[(seed + idx) % len(prefixes)]
        display_name = f"{prefix}{s['name']}".strip()
        cards_html += f"""
        <article class="shop-card">
          <a class="card-media" href="tel:{s['phone']}" aria-label="{display_name} 전화 문의">
            <span class="media-fallback">{s['category']}</span>
            <picture class="card-picture">
              <source media="(max-width: 680px)" srcset="/assets/cards/therapist-card-{s['img']}-240.webp">
              <img class="card-photo" src="/assets/cards/therapist-card-{s['img']}-512.webp" alt="{display_name} 테라피스트 대표 이미지" width="512" height="320" loading="lazy">
            </picture>
          </a>
          <div class="card-body">
            <div style="display:flex; justify-content:space-between; width:100%; align-items:center; margin-bottom: 4px;">
              <span class="category-tag">{s['category']}</span>
              <span style="font-size: 0.76rem; color: #f59e0b; font-weight: 800;">★ 4.9 (후기 {90 + (seed % 40)})</span>
            </div>
            <h3><a class="card-title-link" href="tel:{s['phone']}">{display_name}</a></h3>
            <p class="address">{area_label} 전 지역 25분 내 안심 신속 방문</p>
            <div class="card-bottom">
              <div><span class="price-label">추천 코스</span><strong class="price">{s['price']}</strong></div>
              <div class="card-actions">
                <a class="detail-link" href="sms:{s['phone']}">문자</a>
                <a class="phone-link" href="tel:{s['phone']}" aria-label="{display_name} 전화하기">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                  <span>전화문의</span>
                </a>
              </div>
            </div>
          </div>
        </article>"""
    return cards_html

def generate_page(title_area, page_path, breadcrumbs, related_links, current_city="gyeonggi", current_district="", current_dong=""):
    full_url = f"{SITE_ORIGIN}{page_path}"
    
    # 요청하신 타이틀 & 메타디스크립션 양식 적용
    page_title = f"{title_area} 출장 완벽케어 마사지 | 지역별 이용 가이드 - 건마1004테라피"
    meta_desc = f"1004테라피 선입금없는 후불제 {title_area}  출장 완벽케어 마사지 안내! 경기서울시 일정과 공간에 맞춰 제휴업체 선택지와 후기 등을 확인하세요."
    
    seed = int(hashlib.md5(f"{title_area}_{page_path}".encode('utf-8')).hexdigest(), 16)
    review_count = str(95 + (seed % 65))
    rating_val = "4.9"

    # 네이버 별점 스니펫용 LocalBusiness Schema
    structured_data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"{title_area} 출장 케어 마사지 - {SITE_NAME}",
        "description": meta_desc,
        "url": full_url,
        "telephone": DEFAULT_PHONE,
        "priceRange": "60,000원 ~ 180,000원",
        "image": f"{SITE_ORIGIN}/assets/cards/therapist-card-01-512.webp",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": current_district or title_area,
            "addressRegion": REGION_DATA[current_city]["name"],
            "addressCountry": "KR"
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": REGION_DATA[current_city]["name"]},
            {"@type": "AdministrativeArea", "name": title_area}
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating_val,
            "reviewCount": review_count,
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    json_ld_string = json.dumps(structured_data, ensure_ascii=False, indent=2)

    nav_chips = "".join([
        f'<a class="area-chip{" is-active" if link.get("active") else ""}" href="{link["path"]}">{link["name"]}</a>'
        for link in related_links
    ])

    cards = render_cards_html(title_area, current_dong)

    district_options = "".join([
        f'<option value="/{current_city}/{urllib.parse.quote(d)}/" {"selected" if d==current_district else ""}>{d}</option>'
        for d in REGION_DATA[current_city]["districts"].keys()
    ])

    dong_options = "".join([
        f'<option value="/{current_city}/{urllib.parse.quote(current_district)}/{urllib.parse.quote(dong)}/" {"selected" if dong==current_dong else ""}>{dong}</option>'
        for dong in REGION_DATA[current_city]["districts"].get(current_district, [])
    ]) if current_district else ""

    map_query = urllib.parse.quote(f"{title_area} 마사지")

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{title_area} 출장마사지, {title_area} 타이마사지, {title_area} 아로마마사지, {title_area} 스웨디시, {SITE_NAME}, 건마1004테라피">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="theme-color" content="#171b3c">
  <link rel="canonical" href="{full_url}">

  <!-- Open Graph -->
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{full_url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">

  <!-- 네이버 별점 및 구조화 데이터 -->
  <script type="application/ld+json">
{json_ld_string}
  </script>

  <style>
    :root {{
      --ink: #1a232d; --ink-soft: #606d7b; --primary: #376ca4; --primary-dark: #2b4664;
      --primary-pale: #edf2f8; --line: #d6dee6; --radius-lg: 16px; --radius-md: 20px;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f9fafb; line-height: 1.6; }}
    a {{ color: inherit; text-decoration: none; }}
    .app-header {{ position: sticky; top: 0; z-index: 20; background: rgba(255,255,255,.94); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }}
    .header-inner, .page-shell {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; }}
    .brand-row {{ display: flex; align-items: center; justify-content: space-between; height: 68px; }}
    .brand {{ font-size: 1.25rem; font-weight: 850; display: inline-flex; align-items: center; gap: 8px; color: var(--primary-dark); }}
    
    .filter-bar {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; padding-bottom: 14px; }}
    .select-wrap select {{ width: 100%; height: 44px; padding: 0 14px; border: 1px solid var(--line); border-radius: 12px; background: #fff; font-size: .88rem; font-weight: 750; cursor: pointer; }}
    
    main {{ padding: 24px 0 48px; }}
    .intro {{ padding: clamp(24px, 4vw, 42px); border-radius: var(--radius-lg); background: #17111f; color: #fff; text-align: center; border-top: 5px solid var(--primary); }}
    h1 {{ font-size: clamp(1.8rem, 3.6vw, 2.6rem); margin: 10px 0; word-break: keep-all; }}
    .intro-copy {{ color: #f7edf2; margin-top: 8px; font-size: 1.05rem; word-break: keep-all; }}
    
    .rating-badge {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); padding: 4px 14px; border-radius: 999px; color: #f59e0b; font-size: 0.88rem; font-weight: 850; margin-top: 8px; }}
    
    .nearby-row {{ display: flex; gap: 8px; overflow-x: auto; padding: 18px 0; justify-content: center; scrollbar-width: none; }}
    .nearby-row::-webkit-scrollbar {{ display: none; }}
    .area-chip {{ padding: 8px 14px; border: 1px solid var(--line); border-radius: 999px; background: #fff; font-size: .88rem; font-weight: 750; flex: 0 0 auto; transition: .18s; }}
    .area-chip:hover {{ border-color: var(--primary); }}
    .area-chip.is-active {{ background: var(--primary-pale); border-color: var(--primary); color: var(--primary-dark); }}
    
    .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 18px; margin-top: 20px; }}
    .shop-card {{ border: 1px solid var(--line); border-radius: var(--radius-md); background: #fff; overflow: hidden; display: flex; flex-direction: column; }}
    .card-media {{ aspect-ratio: 16/10; position: relative; background: #eee; display: block; }}
    .card-photo {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .card-body {{ padding: 18px; text-align: center; display: flex; flex-direction: column; flex: 1; }}
    .category-tag {{ padding: 3px 8px; border-radius: 6px; background: #faeff9; color: #c865bc; font-size: .75rem; font-weight: 850; }}
    .shop-card h3 {{ margin: 0 0 6px; font-size: 1.15rem; }}
    .address {{ color: var(--ink-soft); font-size: .86rem; margin: 0 0 12px; }}
    .card-bottom {{ margin-top: auto; padding-top: 12px; border-top: 1px solid #f0f0f5; display: flex; justify-content: space-between; align-items: center; }}
    .price {{ font-weight: 900; font-size: .96rem; color: var(--primary-dark); }}
    .phone-link {{ padding: 8px 14px; border-radius: 12px; background: var(--ink); color: #fff; font-size: .84rem; font-weight: 800; display: inline-flex; align-items: center; gap: 5px; }}
    .phone-link svg {{ width: 14px; height: 14px; }}
    .detail-link {{ padding: 8px 12px; border-radius: 12px; border: 1px solid var(--line); font-size: .84rem; margin-right: 6px; }}
    
    .content-box {{ margin-top: 36px; padding: clamp(20px, 3.5vw, 32px); background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md); }}
    .content-box h2 {{ margin-top: 0; font-size: 1.35rem; color: var(--primary-dark); }}
    .content-box p {{ font-size: 0.94rem; color: #4b5563; line-height: 1.8; margin-bottom: 12px; }}
    
    .price-table {{ width: 100%; border-collapse: collapse; margin-top: 14px; min-width: 500px; }}
    .price-table th, .price-table td {{ padding: 12px 14px; border-bottom: 1px solid #f0f0f5; text-align: center; font-size: .92rem; }}
    .price-table th {{ background: #f8fafc; color: #64748b; font-weight: 800; }}
    .price-table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 14px; margin-top: 14px; }}
    
    .map-box {{ margin-top: 24px; border-radius: 16px; overflow: hidden; border: 1px solid var(--line); height: 320px; }}
    .site-footer {{ margin-top: 40px; padding: 36px 0; background: #fff; border-top: 1px solid var(--line); text-align: center; color: var(--ink-soft); font-size: .88rem; }}
  </style>
</head>
<body>
  <header class="app-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand" href="/" aria-label="{SITE_NAME} 홈">✨ {SITE_NAME}</a>
        <div style="font-size: .88rem; font-weight: 700; color: var(--ink-soft);">경기·서울 출장 케어 마사지</div>
      </div>
      <div class="filter-bar">
        <div class="select-wrap">
          <select onchange="if(this.value) window.location.href=this.value;">
            <option value="/gyeonggi/" {'selected' if current_city=='gyeonggi' else ''}>경기도</option>
            <option value="/seoul/" {'selected' if current_city=='seoul' else ''}>서울특별시</option>
            <option value="/incheon/" {'selected' if current_city=='incheon' else ''}>인천광역시</option>
          </select>
        </div>
        <div class="select-wrap">
          <select onchange="if(this.value) window.location.href=this.value;">
            <option value="/{current_city}/">구/시 선택 전체</option>
            {district_options}
          </select>
        </div>
        <div class="select-wrap">
          <select onchange="if(this.value) window.location.href=this.value;" {'disabled' if not current_district else ''}>
            <option value="/{current_city}/{urllib.parse.quote(current_district)}/">동 선택 전체</option>
            {dong_options}
          </select>
        </div>
      </div>
    </div>
  </header>

  <main class="page-shell">
    <section class="intro">
      <p style="color: #e6bb72; font-weight: 800; letter-spacing: .08em;">24H PRIVATE CARE</p>
      <h1>{title_area} 출장 케어 마사지<br>선입금 없는 안심 후불제 안내</h1>
      <p class="intro-copy">{title_area} 고객님의 일정과 프라이빗한 공간에 맞춘 1:1 방문 맞춤 테라피! 선입금 요구 없이 도착 후 100% 결제하는 안전 제휴 매장입니다.</p>
      <div class="rating-badge">★ {rating_val} 점 / 5.0 만점 (실시간 이용 후기 {review_count}개 기준)</div>
    </section>

    <!-- 구 / 동 바로가기 네비게이션 칩 -->
    <nav class="nearby-row" aria-label="지역 바로가기">
      {nav_chips}
    </nav>

    <!-- 제휴 매장 리스트 -->
    <section>
      <div style="text-align: center; margin: 24px 0 12px;">
        <h2 style="margin: 0; font-size: 1.45rem;">{title_area} 추천 케어 제휴 업체</h2>
        <p style="margin: 6px 0 0; color: var(--ink-soft); font-size: .9rem;">철저한 위생 관리와 품격 있는 실력파 테라피스트의 프라이빗 힐링</p>
      </div>

      <div class="card-grid">
        {cards}
      </div>
    </section>

    <!-- 5대 코스 및 가격 안내 -->
    <section class="content-box">
      <h2>🔮 {title_area} 정찰제 관리 프로그램 요금표</h2>
      <p>{title_area} 전 지역에서 동일하게 적용되는 기준 가격표입니다. 상담 시 안내된 최종 금액 외에 별도의 유류비나 현장 추가금을 절대 요구하지 않습니다.</p>
      
      <div class="price-table-wrap">
        <table class="price-table">
          <thead>
            <tr><th>프로그램 코스</th><th>60분</th><th>90분</th><th>120분</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>🔮 타이 코스</strong><br><span style="font-size:0.75rem; color:#6b7280;">전신 건식 스트레칭 및 뭉친 근육 이완</span></td>
              <td>60,000원</td>
              <td>80,000원</td>
              <td>100,000원</td>
            </tr>
            <tr>
              <td><strong>🔮 전신 아로마</strong><br><span style="font-size:0.75rem; color:#6b7280;">고급 천연 오일을 이용한 부드러운 림프 케어</span></td>
              <td>70,000원</td>
              <td>90,000원</td>
              <td>110,000원</td>
            </tr>
            <tr>
              <td><strong>🔮 VIP 힐링케어</strong><br><span style="font-size:0.75rem; color:#6b7280;">타이의 시원함 + 아로마의 이완 결합</span></td>
              <td>90,000원</td>
              <td>110,000원</td>
              <td>130,000원</td>
            </tr>
            <tr style="background:#fffbeb;">
              <td><strong>🔮 VIP 스페셜코스 <span style="color:#d97706;">★추천</span></strong><br><span style="font-size:0.75rem; color:#6b7280;">전신 딥티슈 &amp; 감성 릴렉싱 집중 케어</span></td>
              <td style="color:#d97706; font-weight:800;">100,000원</td>
              <td style="color:#d97706; font-weight:800;">120,000원</td>
              <td style="color:#d97706; font-weight:800;">140,000원</td>
            </tr>
            <tr>
              <td><strong>🔮 한국인 스웨디시</strong><br><span style="font-size:0.75rem; color:#6b7280;">20대 한국인 전문 테라피스트 밀착 케어</span></td>
              <td>140,000원</td>
              <td>180,000원</td>
              <td>—</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- 네이버 검색 누락 방지용 본문 설명 -->
    <section class="content-box">
      <h2>✨ {title_area} 건천테라피 이용 안내 및 선택 혜택</h2>
      <p>
        지친 일상의 피로를 풀고 편안한 휴식을 원하시는 고객님을 위해 <strong>{title_area}</strong> 출장 마사지 서비스를 제공합니다. 
        자택, 오피스텔, 호텔 등 원하시는 편안한 공간에서 전화 한 통으로 프라이빗하게 맞춤 테라피를 즐기실 수 있습니다.
      </p>
      <p>
        <strong>1. 100% 선입금 없는 후불제 원칙:</strong> 건천테라피에 등록된 모든 {title_area} 제휴 매장은 고객 보호를 최우선으로 하며, 
        출발 전 예약금이나 보증금을 절대 요구하지 않는 100% 안심 후불제 시스템으로만 운영됩니다.
      </p>
      <p>
        <strong>2. 공간 맞춤형 출장 서비스:</strong> 원하시는 시간과 장소의 상세 위치를 알려주시면, 베테랑 관리사가 
        필요한 모든 위생 용품과 고급 오일을 지참하여 신속하게 방문합니다.
      </p>
      <p>
        <strong>3. 체계적인 힐링 프로그램:</strong> 뭉친 근육을 시원하게 풀어주는 타이 코스부터, 스트레스를 녹여내는 전신 아로마, 
        그리고 감성적인 림프 이완을 선사하는 한국인 스웨디시까지 취향에 맞는 다양한 선택지를 제공합니다.
      </p>
    </section>

    <!-- 동적 구글 지도 -->
    <section class="content-box">
      <h2>📍 {title_area} 방문 가능 권역</h2>
      <p>{title_area} 전 지역과 인접 도로망을 기반으로 신속한 방문이 이루어집니다.</p>
      <div class="map-box">
        <iframe
          width="100%"
          height="100%"
          style="border:0;"
          loading="lazy"
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q={map_query}&t=&z=14&ie=UTF8&iwloc=&output=embed">
        </iframe>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="header-inner">
      <p style="font-weight: 850; font-size: 1.1rem; color: var(--primary-dark); margin: 0 0 8px;">{SITE_NAME}</p>
      <p style="margin: 0 0 12px;">경기·서울·인천 출장 케어 마사지 &amp; 힐링 테라피 플랫폼</p>
      <p style="font-size: .78rem; color: #8a8da3;">{SITE_NAME}는 선입금을 절대 요구하지 않는 100% 안심 후불제 정보 안내 사이트입니다.<br>© 2026 {SITE_NAME}. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""

def main():
    sitemap_urls = [SITE_ORIGIN + "/"]
    os.makedirs("dist", exist_ok=True)

    # 1. 메인 홈페이지 생성 (평택 및 경기·서울 거점 칩 링크)
    home_links = [
        {"name": "평택시", "path": f"/gyeonggi/{urllib.parse.quote('평택시')}/"},
        {"name": "수원 영통", "path": f"/gyeonggi/{urllib.parse.quote('수원시 영통구')}/"},
        {"name": "화성시", "path": f"/gyeonggi/{urllib.parse.quote('화성시')}/"},
        {"name": "오산시", "path": f"/gyeonggi/{urllib.parse.quote('오산시')}/"},
        {"name": "안성시", "path": f"/gyeonggi/{urllib.parse.quote('안성시')}/"},
        {"name": "분당구", "path": f"/gyeonggi/{urllib.parse.quote('성남시 분당구')}/"},
        {"name": "강남구", "path": f"/seoul/{urllib.parse.quote('강남구')}/"},
        {"name": "인천 부평", "path": f"/incheon/{urllib.parse.quote('부평구')}/"}
    ]
    home_bc = [{"name": "홈", "path": "/"}]
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(generate_page("경기 서울", "/", home_bc, home_links, current_city="gyeonggi"))
    print("✓ 메인 페이지(dist/index.html) 생성 완료")

    # 2. 시·도, 구, 동 폴더 및 개별 정적 index.html 생성
    for city_key, city_info in REGION_DATA.items():
        city_path = f"/{city_key}/"
        sitemap_urls.append(SITE_ORIGIN + city_path)
        city_dir = os.path.join("dist", city_key)
        os.makedirs(city_dir, exist_ok=True)

        dist_links = [{"name": d, "path": f"/{city_key}/{urllib.parse.quote(d)}/"} for d in list(city_info["districts"].keys())[:12]]
        city_bc = [{"name": "홈", "path": "/"}, {"name": city_info["short"], "path": city_path}]
        with open(os.path.join(city_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(generate_page(city_info["name"], city_path, city_bc, dist_links, current_city=city_key))

        for district_name, dongs in city_info["districts"].items():
            encoded_dist = urllib.parse.quote(district_name)
            dist_path = f"/{city_key}/{encoded_dist}/"
            sitemap_urls.append(SITE_ORIGIN + dist_path)

            dist_dir = os.path.join(city_dir, district_name)
            os.makedirs(dist_dir, exist_ok=True)

            dong_links = [{"name": d, "path": f"/{city_key}/{encoded_dist}/{urllib.parse.quote(d)}/"} for d in dongs]
            dist_bc = city_bc + [{"name": district_name, "path": dist_path}]

            with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(generate_page(f"{city_info['short']} {district_name}", dist_path, dist_bc, dong_links, current_city=city_key, current_district=district_name))

            for dong_name in dongs:
                encoded_dong = urllib.parse.quote(dong_name)
                dong_path = f"/{city_key}/{encoded_dist}/{encoded_dong}/"
                sitemap_urls.append(SITE_ORIGIN + dong_path)

                dong_dir = os.path.join(dist_dir, dong_name)
                os.makedirs(dong_dir, exist_ok=True)

                dong_bc = dist_bc + [{"name": dong_name, "path": dong_path}]
                sibling_dongs = [
                    {"name": d, "path": f"/{city_key}/{encoded_dist}/{urllib.parse.quote(d)}/", "active": (d == dong_name)}
                    for d in dongs
                ]

                with open(os.path.join(dong_dir, "index.html"), "w", encoding="utf-8") as f:
                    f.write(generate_page(
                        f"{city_info['short']} {district_name} {dong_name}",
                        dong_path,
                        dong_bc,
                        sibling_dongs,
                        current_city=city_key,
                        current_district=district_name,
                        current_dong=dong_name
                    ))

    # 3. sitemap.xml 생성
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_content += f"  <url><loc>{url}</loc><priority>0.8</priority></url>\n"
    sitemap_content += "</urlset>"
    with open("dist/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"✓ sitemap.xml 생성 완료 (총 {len(sitemap_urls)}개 URL)")

    # 4. robots.txt 생성
    with open("dist/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_ORIGIN}/sitemap.xml\n")
    print("✓ robots.txt 생성 완료")

    # 5. assets 복사
    if os.path.exists("assets"):
        shutil.copytree("assets", "dist/assets", dirs_exist_ok=True)
        print("✓ assets 폴더 복사 완료")

if __name__ == "__main__":
    main()