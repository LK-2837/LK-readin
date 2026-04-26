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
        "1회차": "사물의 상태를 나타내는 '투명', '구분'의 개념을 익히고, 시간의 흐름인 '동안'과 '다음'의 정확한 쓰임을 학습했습니다.",
        "2회차": "전래 풍속인 '민속' 어휘를 배우고, 설날·추석·동지의 풍습과 관련된 어휘를 정리했습니다.",
        "9회차": "불안한 마음 '조마조마'와 남김없이 벗는 '홀딱' 등 상태 묘사 어휘를 배우고 감각적 표현 능력을 길렀습니다.",
        **{f"{i}회차": f"1단계 {i}회차 해설의 어휘 정의를 바탕으로 문맥 속 낱말의 쓰임과 문장 구조를 익혔습니다." for i in range(1, 41) if i not in [1, 2, 9]}
    },
    "2단계": {
        "1회차": "목적 달성 수단인 '방법', 원인인 '까닭', 기본 규칙인 '원칙'의 차이를 배우고 육하원칙 문장 구성을 연습했습니다.",
        "10회차": "남의 말에 동조하는 '맞장구', 형제자매 이름의 '돌림자', '기발하다, 만장일치' 등 관계 어휘를 보강했습니다.",
        **{f"{i}회차": f"2단계 {i}회차 어법·어휘 해설을 통해 주어와 서술어의 호응 및 문맥에 맞는 어휘 선택 훈련을 진행했습니다." for i in range(1, 41) if i not in [1, 10]}
    },
    "4단계": {
        "9회차": "부정을 나타내는 '안'과 '않'의 맞춤법 구분을 완벽히 익히고, '훈훈, 넉넉, 만만, 눅눅, 답답, 꼼꼼' 등 상태 어휘를 학습했습니다.",
        "26회차": "지구 중심 방향으로 당기는 힘인 '무게'와 물체의 본바탕인 '질량'의 차이를 이해하고 과학 핵심 용어를 정리했습니다.",
        **{f"{i}회차": f"4단계 {i}회차 해설을 통해 지문에 직접 드러나지 않은 의미를 논리적으로 추론하는 어휘 훈련을 진행했습니다." for i in range(1, 41) if i not in [9, 26]}
    },
    "5단계": {
        "6회차": "처음 만드는 '창제'와 그것을 세상에 널리 퍼뜨리는 '반포'의 역사적 의미 차이를 명확히 배우고 한글 창제 정신을 정리했습니다.",
        "7회차": "국가에서 정하여 쉬는 '공휴일'의 정의와 특별히 축하하거나 애도하기 위해 쉬는 날의 의미를 배우고 관련 사회적 어휘를 익혔습니다.",
        **{f"{i}회차": f"5단계 {i}회차의 어법·어휘 해설을 바탕으로 논설문의 주장을 뒷받침하는 타당한 근거 어휘와 논리적 연결어를 학습했습니다." for i in range(1, 41) if i not in [6, 7]}
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

    # 2. 주교재 도서진단
    st.subheader("📝 2. 주교재 도서진단")
    v_book = st.text_input("도서명", value=last_rec.get("v_book", ""))
    selected_level = st.selectbox("진단 레벨", ["기초레벨"] + [f"{i}레벨" for i in range(1, 11)], index=0)
    
    cv1, cv2, cv3, cv4 = st.columns(4)
    v_unit = cv1.selectbox("회차", [f"{i}회차" for i in range(1, 5)])
    v_corr = cv2.number_input("맞은 개수", 0, 10, 10)
    v_tot = cv3.number_input("전체 개수", 1, 10, 10)
    v_status = cv4.selectbox("결과", ["통과", "미통과"])

    st.divider()

    # 3. 부교재 선택 및 입력
    st.subheader("📖 3. 부교재 학습 상세")
    
    # --- 부교재 1: 뿌리깊은 초등국어 ---
    sub1_final = ""
    use_sub1 = st.checkbox("뿌리깊은 초등국어 포함")
    if use_sub1:
        s1c1, s1c2 = st.columns(2)
        step = s1c1.selectbox("단계", [f"{i}단계" for i in range(1, 7)])
        unit = s1c2.selectbox("회차 ", [f"{i}회차" for i in range(1, 41)])
        s1_m = st.selectbox("소요시간(분)", [f"{i}분" for i in range(61)], key="t1")
        
        db_msg = SUB_BOOK_INFO.get(step, {}).get(unit, "어휘 학습을 완료했습니다.")
        sub1_msg = st.text_area("학습 포인트 (해설지 기반)", value=db_msg, key=f"sub1_{step}_{unit}")
        sub1_final = f"• 부교재: 뿌리깊은초등국어 [{step}-{unit}] ({s1_m})\n[학습 포인트]\n{sub1_msg}\n\n"

    st.write("---")

    # --- 부교재 2: 어휘가 문해력이다 ---
    sub2_final = ""
    use_sub2 = st.checkbox("어휘가 문해력이다 포함")
    if use_sub2:
        s2c1, s2c2 = st.columns(2)
        lv = s2c1.selectbox("레벨", VOCAB_LITERACY_LEVELS)
        ut = s2c2.selectbox("회차  ", [f"{i}회차" for i in range(1, 41)])
        s2_m = st.selectbox("소요시간(분) ", [f"{i}분" for i in range(61)], key="t2")
        
        # ❗ 이 부분이 선생님이 찾으시던 자유 입력 칸입니다 ❗
        sub2_custom = st.text_area("어휘가 문해력이다 활동 상세 내용", placeholder="배운 어휘나 활동 내용을 자유롭게 적으세요.", key=f"sub2_{lv}_{ut}")
        sub2_final = f"• 부교재: 어휘가 문해력이다 [{lv}-{ut}] ({s2_m})\n  - 활동: {sub2_custom}\n\n"

    st.write("---")

    # --- 부교재 3: 독서평설 ---
    sub3_final = ""
    use_sub3 = st.checkbox("독서평설 포함")
    if use_sub3:
        s3_type = st.selectbox("구분", ["초등", "중등"])
        sub3_custom = st.text_area("독서평설 학습 내용 입력", placeholder="읽은 주제나 요약 내용을 적으세요.", key="sub3_box")
        sub3_final = f"• 부교재: 독서평설({s3_type})\n  - 내용: {sub3_custom}\n\n"

    st.write("---")

    # --- 부교재 4: 신문 ---
    sub4_final = ""
    use_sub4 = st.checkbox("신문 활동 포함")
    if use_sub4:
        sub4_custom = st.text_area("신문 활동 상세 내용 입력", placeholder="신문 기사 요약이나 활동을 적으세요.", key="sub4_box")
        sub4_final = f"• 부교재: 신문 활동\n  - 내용: {sub4_custom}\n\n"

    st.divider()

    # 4. 선생님 피드백
    st.subheader("✍️ 4. 선생님 피드백")
    footer = "아이에게 '읽은 책 자랑'을 꼭 시켜주세요~ 더불어 많은 칭찬과 격려부탁드립니다. 감사합니다!"
    teacher_comment = st.text_area("종합 의견", value=footer, height=120)

    if st.button("🚀 리포트 생성", type="primary"):
        if not name:
            st.error("이름을 입력해 주세요.")
        else:
            # 부교재 전체 합치기
            all_subs = sub1_final + sub2_final + sub3_final + sub4_final
            
            final_report = f"""[ 엘케이리드인독서논술학원 학습 리포트 ]

■ 대상: {grade} {name} 학생
■ 학습일: {report_date}

1. 주교재 도서진단 결과
■ 도서명: {v_book}
 - 진단결과: [{v_unit}] [{v_status}] {v_corr}/{v_tot}

2. 학습 내용 상세
• 주교재: 리드인 독서 [{selected_level}]
{all_subs}
[선생님 피드백]
{teacher_comment}"""
            
            # 저장 및 이동
            history[name] = {"grade": grade, "v_book": v_book}
            save_history(history)
            st.session_state.final_text = final_report
            st.session_state.page = 'result'; st.rerun()

elif st.session_state.page == 'result':
    st.title("📄 생성된 리포트")
    st.text_area("내용 복사용", st.session_state.final_text, height=600)
    if st.button("돌아가기"):
        st.session_state.page = 'input'; st.rerun()
