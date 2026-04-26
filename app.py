import streamlit as st
import os
import json
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="엘케이리드인 학습 리포트", layout="centered")

HISTORY_FILE = "student_history.json"

# --- [부교재 1: 뿌리깊은 초등국어 정밀 DB] ---
SUB_BOOK_INFO = {
    "4단계": {
        "9회차": "부정을 나타내는 '안'과 '않'의 맞춤법 구분을 완벽히 익히고, '훈훈, 넉넉, 만만, 눅눅, 답답, 꼼꼼' 등 상태 어휘를 학습했습니다.",
        "26회차": "지구 중심 방향으로 당기는 힘인 '무게'와 물체의 본바탕인 '질량'의 차이를 이해하고 과학 핵심 용어를 정리했습니다.",
    },
    "5단계": {
        "6회차": "처음 만드는 '창제'와 그것을 세상에 널리 퍼뜨리는 '반포'의 역사적 의미 차이를 명확히 배우고 한글 창제 정신을 정리했습니다.",
        "7회차": "국가에서 정하여 쉬는 '공휴일'의 정의와 특별히 축하하거나 애도하기 위해 쉬는 날의 의미를 배우고 관련 사회적 어휘를 익혔습니다.",
    }
}

VOCAB_LITERACY_LEVELS = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2", "5-1", "5-2", "6-1", "6-2"]

# --- [데이터 로드] ---
history = {}
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    except: history = {}

# --- [UI 메인] ---
if "page" not in st.session_state: st.session_state.page = 'input'

if st.session_state.page == 'input':
    st.title("📚 학습 리포트 생성기")

    # 기본 정보
    name = st.text_input("학생 이름")
    grade = st.selectbox("학년", ["초등", "중등", "고등"])
    report_date = st.date_input("학습일", value=datetime.today())

    st.divider()
    st.subheader("📝 주교재 진단 (1차/2차)")
    v_book = st.text_input("도서명", value="리드인 독서")
    selected_level = st.selectbox("진단 레벨", ["기초레벨"] + [f"{i}레벨" for i in range(1, 11)], index=0)
    
    # 1차 진단
    st.write("**[1차 진단]**")
    cv1, cv2, cv3, cv4 = st.columns(4)
    v_unit1 = cv1.selectbox("회차", [f"{i}회차" for i in range(1, 5)], key="v1")
    v_corr1 = cv2.number_input("맞은 개수", 0, 10, 10, key="c1")
    v_tot1 = cv3.number_input("전체 개수", 1, 10, 10, key="t1")
    v_status1 = cv4.selectbox("결과", ["통과", "미통과"], key="s1")

    # 2차 진단 (필요 시 선택)
    st.write("**[2차 진단 (선택)]**")
    cv21, cv22, cv23, cv24 = st.columns(4)
    v_unit2 = cv21.selectbox("회차 ", ["선택 안 함"] + [f"{i}회차" for i in range(1, 5)], key="v2")
    v_corr2 = cv22.number_input("맞은 개수 ", 0, 10, 10, key="c2")
    v_tot2 = cv23.number_input("전체 개수 ", 1, 10, 10, key="t2")
    v_status2 = cv24.selectbox("결과 ", ["통과", "미통과"], key="s2")

    st.divider()
    st.subheader("📖 부교재 기록")

    # --- 1. 뿌리깊은 초등국어 ---
    sub1_final = ""
    if st.checkbox("뿌리깊은 초등국어 포함"):
        s1_step = st.selectbox("단계", [f"{i}단계" for i in range(1, 7)])
        s1_unit = st.selectbox("회차  ", [f"{i}회차" for i in range(1, 41)])
        s1_time = st.selectbox("소요시간(분)", [f"{i}분" for i in range(61)], key="tm1")
        db_val = SUB_BOOK_INFO.get(s1_step, {}).get(s1_unit, f"{s1_step} {s1_unit} 학습을 완료했습니다.")
        sub1_msg = st.text_area("학습 포인트", value=db_val, key=f"a1_{s1_step}_{s1_unit}")
        sub1_final = f"• 부교재: 뿌리깊은초등국어 [{s1_step}-{s1_unit}] ({s1_time})\n[학습 포인트]\n{sub1_msg}\n\n"

    # --- 2. 어휘가 문해력이다 ---
    sub2_final = ""
    if st.checkbox("어휘가 문해력이다 포함"):
        s2_lv = st.selectbox("레벨", VOCAB_LITERACY_LEVELS)
        s2_ut = st.selectbox("회차   ", [f"{i}회차" for i in range(1, 41)])
        s2_time = st.selectbox("소요시간(분) ", [f"{i}분" for i in range(61)], key="tm2")
        sub2_custom = st.text_area("✨ 어휘가 문해력이다 상세 활동", placeholder="배운 단어나 활동 내용을 적으세요.", key=f"a2_{s2_lv}_{s2_ut}")
        sub2_final = f"• 부교재: 어휘가 문해력이다 [{s2_lv}-{s2_ut}] ({s2_time})\n  - 활동: {sub2_custom}\n\n"

    # --- 3. 독서평설 & 4. 신문 ---
    sub3_final = ""; sub4_final = ""
    if st.checkbox("독서평설 포함"):
        s3_type = st.selectbox("구분", ["초등", "중등"])
        sub3_msg = st.text_area("독서평설 내용", key="a3")
        sub3_final = f"• 부교재: 독서평설({s3_type})\n  - 내용: {sub3_msg}\n\n"

    if st.checkbox("신문 포함"):
        sub4_msg = st.text_area("신문 활동 내용", key="a4")
        sub4_final = f"• 부교재: 신문 활동\n  - 내용: {sub4_msg}\n\n"

    st.divider()
    comment = st.text_area("선생님 피드백", value="아이에게 '읽은 책 자랑'을 시켜주세요~ 더불어 많은 칭찬과 격려부탁드립니다. 감사합니다!")

    if st.button("🚀 리포트 생성"):
        if not name:
            st.error("이름을 입력하세요.")
        else:
            # 진단 결과 문구 생성
            diag_result = f"■ 도서명: {v_book}\n - 1차 진단: [{v_unit1}] [{v_status1}] {v_corr1}/{v_tot1}"
            if v_unit2 != "선택 안 함":
                diag_result += f"\n - 2차 진단: [{v_unit2}] [{v_status2}] {v_corr2}/{v_tot2}"
            
            total_sub = sub1_final + sub2_final + sub3_final + sub4_final
            report_text = f"""[ 엘케이리드인독서논술학원 학습 리포트 ]

■ 대상: {grade} {name} 학생
■ 학습일: {report_date}

1. 주교재 도서진단 결과
{diag_result}

2. 학습 내용 상세
• 주교재: 리드인 독서 [{selected_level}]
{total_sub}
[선생님 피드백]
{comment}"""
            st.session_state.final_text = report_text
            st.session_state.page = 'result'; st.rerun()

elif st.session_state.page == 'result':
    st.title("📄 생성된 리포트")
    st.text_area("복사용", st.session_state.final_text, height=600)
    if st.button("돌아가기"):
        st.session_state.page = 'input'; st.rerun()
