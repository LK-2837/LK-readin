import streamlit as st
import os
import json
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="엘케이리드인독서논술학원 학습 리포트", layout="centered")

HISTORY_FILE = "student_history.json"

# --- [부교재 1: 뿌리깊은 초등국어 정밀 데이터베이스] ---
SUB_BOOK_INFO = {
    "1단계": {
        "1회차": "맑은 상태인 '투명'과 기준에 따른 '구분'의 개념을 익히고, 시간의 흐름인 '동안'과 '다음'의 정확한 쓰임을 학습했습니다.",
        "2회차": "전래 풍속인 '민속' 어휘를 배우고, 설날·추석·동지의 풍습과 관련된 어휘를 정리했습니다.",
        "3회차": "상대를 청하는 '초대'와 기쁜 날의 '잔치', '축하'와 '연락'의 의미 차이를 파악하며 상황별 어휘력을 높였습니다.",
        "4회차": "웃는 모양 '생글생글'과 코를 벌리는 '발름발름' 등 의태어를 통해 모양을 흉내 내는 말의 생동감을 체득했습니다.",
        "5회차": "빠른 변화를 뜻하는 '갑자기'와 간절한 바람인 '제발' 등의 부사 어휘를 통해 문장의 미세한 뉘앙스를 파악했습니다.",
        "9회차": "불안한 마음 '조마조마'와 남김없이 벗는 '홀딱' 등 상태 묘사 어휘를 배우고 감각적 표현 능력을 길렀습니다.",
        **{f"{i}회차": f"1단계 {i}회차 해설의 어휘 정의를 바탕으로 문맥 속 낱말의 쓰임과 문장 연결 관계를 익히는 학습을 진행했습니다." for i in range(1, 41) if i not in [1, 2, 3, 4, 5, 9]}
    },
    "2단계": {
        "1회차": "목적 달성 수단인 '방법', 원인인 '까닭', 기본 규칙인 '원칙'의 차이를 배우고 육하원칙 문장 구성을 연습했습니다.",
        "2회차": "짐승을 기르는 '사육'과 보살피는 '관리', '생활'의 의미를 비교하며 직업 관련 전문 어휘를 습득했습니다.",
        "10회차": "남의 말에 동조하는 '맞장구', 형제자매 이름의 '돌림자', '기발하다, 만장일치' 등 관계 어휘를 보강했습니다.",
        **{f"{i}회차": f"2단계 {i}회차 어법·어휘 해설을 통해 주어와 서술어의 호응 및 문맥에 맞는 어휘 선택 훈련을 진행했습니다." for i in range(1, 41) if i not in [1, 2, 10]}
    },
    "3단계": {
        "1회차": "미리 주의를 주는 '경고', 의사의 '진찰'과 병에 따른 '처방'의 단계별 의미 차이를 학습하여 실생활 어휘력을 보강했습니다.",
        "2회차": "서로 다른 '차이', 특징에 따른 '종류', 순서에 맞게 바로잡는 '정리'의 논리적 개념을 익히고 실무 어휘를 습득했습니다.",
        **{f"{i}회차": f"3단계 {i}회차 해설지의 다의어와 유의어 설명을 바탕으로 상황에 알맞은 어휘 선택과 문장 활용 능력을 다졌습니다." for i in range(1, 41) if i not in [1, 2]}
    },
    "4단계": {
        "1회차": "순우리말, 한자어, 귀화어, 외래어의 분류 기준을 배우고 가깝게 맞닿은 '밀접하다'와 '귀화'의 뜻을 익혔습니다.",
        "2회차": "나라 기관인 '관공서', 규칙적인 '규칙적', 겉에 적는 '표기'의 의미를 배우고 도로명 주소 체계 어휘를 습득했습니다.",
        "9회차": "부정을 나타내는 '안'과 '않'의 맞춤법 구분을 완벽히 익히고, '훈훈, 넉넉, 만만, 눅눅, 답답, 꼼꼼' 등 상태 어휘를 학습했습니다.",
        "26회차": "지구 중심 방향으로 당기는 힘인 '무게'와 물체의 본바탕인 '질량'의 차이를 이해하고 과학 핵심 용어를 정리했습니다.",
        **{f"{i}회차": f"4단계 {i}회차 해설을 통해 지문에 직접 드러나지 않은 의미를 논리적으로 추론하고 배경지식을 확장하는 어휘 학습을 했습니다." for i in range(1, 41) if i not in [1, 2, 9, 26]}
    },
    "5단계": {
        "1회차": "일에 익숙해지는 '길들이다', 호화로운 '호사스럽다', 자주 일어나는 '빈번하다' 등 상태 묘사 어휘를 학습했습니다.",
        "6회차": "처음 만드는 '창제'와 그것을 세상에 널리 퍼뜨리는 '반포'의 역사적 의미 차이를 명확히 배우고 한글 창제 정신을 정리했습니다.",
        "7회차": "국가에서 정하여 쉬는 '공휴일'의 정의와 특별히 축하하거나 애도하기 위해 쉬는 날의 의미를 배우고 관련 사회적 어휘를 익혔습니다.",
        **{f"{i}회차": f"5단계 {i}회차의 어법·어휘 해설을 바탕으로 논설문의 주장을 뒷받침하는 타당한 근거 어휘와 논리적 연결어를 학습했습니다." for i in range(1, 41) if i not in [1, 6, 7]}
    },
    "6단계": {
        "1회차": "불특정 다수에게 보내는 '스팸'과 현실을 비꼬는 '풍자', 발생 과정 '유래' 등 비문학 지문의 핵심 어휘를 완벽 습득했습니다.",
        **{f"{i}회차": f"6단계 {i}회차의 어법·어휘 해설을 통해 전문적인 학술 용어들을 체득하는 훈련을 진행했습니다." for i in range(2, 41)}
    }
}

VOCAB_LITERACY_LEVELS = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2", "5-1", "5-2", "6-1", "6-2"]

# --- [기능 함수] ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# --- [데이터 정의] ---
LEVEL_LIST = ["기초레벨"] + [f"{i}레벨" for i in range(1, 11)]
SUB_BOOK_STEPS = [f"{i}단계" for i in range(1, 7)]
UNITS_40 = [f"{i}회차" for i in range(1, 41)]
UNITS_4 = [f"{i}회차" for i in range(1, 5)]
PASS_STATUS = ["통과", "미통과"]
TIME_MIN = [f"{i}분" for i in range(0, 61)]
TIME_SEC = [f"{i}초" for i in range(0, 60)]

# --- [메인 로직] ---
if "page" not in st.session_state: st.session_state.page = 'input'
history = load_history()

if st.session_state.page == 'input':
    st.title("📚 엘케이리드인독서논술학원")
    st.subheader("학습 리포트 생성기")

    with st.expander("🔍 기존 학생 정보 불러오기", expanded=False):
        all_st = sorted(list(history.keys()))
        search = st.selectbox("학생 선택", ["직접 입력"] + all_st)
        last_rec = history.get(search, {}) if search != "직접 입력" else {}

    st.divider()

    # 1. 기본 정보
    st.subheader("📍 1. 기본 정보")
    report_date = st.date_input("학습일 선택", value=datetime.today())
    c1, c2 = st.columns(2)
    grade = c1.selectbox("학년", ["초등", "중등", "고등"], index=["초등", "중등", "고등"].index(last_rec.get("grade", "초등")))
    name = c2.text_input("학생 이름", value=search if search != "직접 입력" else "")

    st.divider()

    # 2. 주교재 도서진단테스트
    st.subheader("📝 2. 주교재 도서진단테스트")
    selected_level = st.selectbox("주교재 레벨 선택", LEVEL_LIST, index=LEVEL_LIST.index(last_rec.get("level", "기초레벨")) if last_rec.get("level") in LEVEL_LIST else 0)
    v_book_name = st.text_input("도서명 입력", value=last_rec.get("v_book", ""))
    
    st.write("**[1차 진단 기록]**")
    cv1_1, cv1_2, cv1_3, cv1_4 = st.columns(4)
    v_unit1 = cv1_1.selectbox("회차", UNITS_4, key="v_unit1")
    v_corr1 = cv1_2.number_input("맞은 개수", min_value=0, step=1, key="v_corr1")
    v_tot1 = cv1_3.number_input("전체 개수", min_value=1, value=10, step=1, key="v_tot1")
    v_status1 = cv1_4.selectbox("결과", PASS_STATUS, key="v_status1")

    st.write("**[2차 진단 기록] (필요 시 입력)**")
    cv2_1, cv2_2, cv2_3, cv2_4 = st.columns(4)
    v_unit2 = cv2_1.selectbox("회차 ", ["선택 안 함"] + UNITS_4, key="v_unit2")
    v_corr2 = cv2_2.number_input("맞은 개수 ", min_value=0, step=1, key="v_corr2")
    v_tot2 = cv2_3.number_input("전체 개수 ", min_value=1, value=10, step=1, key="v_tot2")
    v_status2 = cv2_4.selectbox("결과 ", PASS_STATUS, key="v_status2")

    st.divider()

    # 3. [부교재 1] 뿌리깊은 초등국어
    st.subheader("📖 3. [부교재 1] 뿌리깊은 초등국어")
    use_sub1 = st.checkbox("뿌리깊은 초등국어 포함", value=False)
    final_sub1_content = ""; sub1_time_text = ""
    if use_sub1:
        cs1, cs2 = st.columns(2)
        sub1_step = cs1.selectbox("단계 선택", SUB_BOOK_STEPS)
        sub1_unit = cs2.selectbox("회차 선택", UNITS_40)
        tm1, tm2 = st.columns(2)
        sub1_min = tm1.selectbox("분 ", TIME_MIN, key="sub1_min")
        sub1_sec = tm2.selectbox("초 ", TIME_SEC, key="sub1_sec")
        sub1_time_text = f"({sub1_min} {sub1_sec})"
        db_content = SUB_BOOK_INFO.get(sub1_step, {}).get(sub1_unit, f"{sub1_step} {sub1_unit} 학습을 통해 핵심 어휘와 문장 구조를 익혔습니다.")
        final_sub1_content = st.text_area("학습 포인트 확인 및 수정", value=db_content, height=120, key=f"sub1_{sub1_step}_{sub1_unit}")

    st.divider()

    # 4. [부교재 2] 어휘가 문해력이다 (자유 입력 추가)
    st.subheader("📖 4. [부교재 2] 어휘가 문해력이다")
    use_sub2 = st.checkbox("어휘가 문해력이다 포함", value=False)
    sub2_info_text = ""
    if use_sub2:
        cs3, cs4 = st.columns(2)
        sub2_level = cs3.selectbox("레벨 선택", VOCAB_LITERACY_LEVELS)
        sub2_unit = cs4.selectbox("회차 선택  ", UNITS_40)
        tm3, tm4 = st.columns(2)
        sub2_min = tm3.selectbox("분  ", TIME_MIN, key="sub2_min")
        sub2_sec = tm4.selectbox("초  ", TIME_SEC, key="sub2_sec")
        sub2_content = st.text_area("활동 상세 내용 (어휘)", placeholder="학습한 어휘나 문해 활동 내용을 입력하세요.", key="sub2_text")
        sub2_info_text = f"• 부교재: 어휘가 문해력이다 [{sub2_level} - {sub2_unit}] ({sub2_min} {sub2_sec})\n  - 활동: {sub2_content}\n"

    st.divider()

    # 5. [부교재 3] 독서평설 (자유 입력)
    st.subheader("📖 5. [부교재 3] 독서평설")
    use_sub3 = st.checkbox("독서평설 포함", value=False)
    sub3_info_text = ""
    if use_sub3:
        sub3_type = st.selectbox("구분", ["초등", "중등"])
        sub3_content = st.text_area("학습 내용 (독서평설)", placeholder="독서평설 학습 주제나 내용을 입력하세요.", key="sub3_text")
        sub3_info_text = f"• 부교재: 독서평설({sub3_type})\n  - 활동: {sub3_content}\n"

    st.divider()

    # 6. [부교재 4] 신문 (자유 입력)
    st.subheader("📖 6. [부교재 4] 신문")
    use_sub4 = st.checkbox("신문 포함", value=False)
    sub4_info_text = ""
    if use_sub4:
        sub4_content = st.text_area("학습 내용 (신문)", placeholder="신문 기사 요약이나 활동 내용을 입력하세요.", key="sub4_text")
        sub4_info_text = f"• 부교재: 신문 활동\n  - 활동: {sub4_content}\n"

    st.divider()

    # 7. 선생님 피드백
    st.subheader("✍️ 7. 선생님 피드백")
    footer = "아이에게 '읽은 책 자랑'을 꼭 시켜주세요~ 더불어 많은 칭찬과 격려부탁드립니다. 감사합니다!"
    teacher_comment = st.text_area("종합 코멘트", value=footer, height=150)

    if st.button("🚀 리포트 생성", type="primary"):
        if not name: st.warning("이름을 입력하세요.")
        else:
            diag_lines = []
            if v_book_name:
                diag_lines.append(f"■ 도서명: {v_book_name}")
                diag_lines.append(f" - 1차 진단: [{v_unit1}] [{v_status1}] {v_corr1}/{v_tot1}")
                if v_unit2 != "선택 안 함": diag_lines.append(f" - 2차 진단: [{v_unit2}] [{v_status2}] {v_corr2}/{v_tot2}")
            
            sub_part = ""
            if use_sub1: sub_part += f"• 부교재: 뿌리깊은초등국어 [{sub1_step} - {sub1_unit}] {sub1_time_text}\n[학습 포인트]\n{final_sub1_content}\n\n"
            if use_sub2: sub_part += sub2_info_text
            if use_sub3: sub_part += sub3_info_text
            if use_sub4: sub_part += sub4_info_text
            
            report = f"""[ 엘케이리드인독서논술학원 학습 리포트 ]

■ 대상: {grade} {name} 학생
■ 학습일: {report_date}

1. 주교재 도서진단 결과
{chr(10).join(diag_lines) if diag_lines else "- 기록 없음"}

2. 학습 내용 상세
• 주교재: 리드인 독서 [{selected_level}]
{sub_part}
[선생님 피드백]
{teacher_comment}"""
            
            history[name] = {"grade": grade, "v_book": v_book_name, "level": selected_level}
            save_history(history)
            st.session_state.final_text = report; st.session_state.page = 'result'; st.rerun()

elif st.session_state.page == 'result':
    st.title("📄 생성된 리포트")
    st.text_area("내용 복사", st.session_state.final_text, height=650)
    if st.button("처음으로 돌아가기"): st.session_state.page = 'input'; st.rerun()
