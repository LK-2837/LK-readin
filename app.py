import streamlit as st
import os
import json
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="엘케이리드인독서논술학원 학습 리포트", layout="centered")

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

# --- [UI 로직] ---
if "page" not in st.session_state: st.session_state.page = 'input'

if st.session_state.page == 'input':
    st.title("📚 엘케이리드인독서논술학원")
    st.subheader("학습 리포트 생성기")

    # 1. 기본 정보
    st.divider()
    name = st.text_input("학생 이름")
    grade = st.selectbox("학년", ["초등", "중등", "고등"])
    report_date = st.date_input("학습일", value=datetime.today())

    # 2. 주교재 진단
    st.divider()
    st.subheader("📝 주교재 진단")
    v_book = st.text_input("도서명", value="리드인 독서")
    cv1, cv2, cv3 = st.columns(3)
    v_unit = cv1.selectbox("회차", [f"{i}회차" for i in range(1, 5)])
    v_score = cv2.number_input("맞은 개수", 0, 10, 10)
    v_status = cv3.selectbox("결과", ["통과", "미통과"])

    # 3. 부교재 상세 입력 (여기가 핵심입니다)
    st.divider()
    st.subheader("📖 부교재 학습 (해당 교재를 체크하세요)")

    # --- 부교재 1: 뿌리깊은 초등국어 ---
    sub1_final = ""
    if st.checkbox("1. 뿌리깊은 초등국어 포함"):
        c1, c2 = st.columns(2)
        step = c1.selectbox("단계", [f"{i}단계" for i in range(1, 7)])
        unit = c2.selectbox("회차 ", [f"{i}회차" for i in range(1, 41)])
        s1_time = st.selectbox("소요시간(분)", [f"{i}분" for i in range(61)], key="time1")
        
        # 실제 해설지 데이터 가져오기
        db_val = SUB_BOOK_INFO.get(step, {}).get(unit, f"{step} {unit} 어휘 및 어법 학습을 진행했습니다.")
        sub1_msg = st.text_area("학습 포인트 (해설지 내용)", value=db_val, key=f"area1_{step}_{unit}")
        sub1_final = f"• 부교재: 뿌리깊은초등국어 [{step}-{unit}] ({s1_time})\n[학습 포인트]\n{sub1_msg}\n\n"

    # --- 부교재 2: 어휘가 문해력이다 (선생님이 고대하시던 입력칸!) ---
    sub2_final = ""
    if st.checkbox("2. 어휘가 문해력이다 포함"):
        c3, c4 = st.columns(2)
        lv = c3.selectbox("레벨", VOCAB_LITERACY_LEVELS)
        ut = c4.selectbox("회차  ", [f"{i}회차" for i in range(1, 41)])
        s2_time = st.selectbox("소요시간(분) ", [f"{i}분" for i in range(61)], key="time2")
        
        # ❗ 이 상자가 바로 나타나야 합니다 ❗
        sub2_custom = st.text_area("어휘가 문해력이다 - 상세 활동 내용 입력", 
                                   placeholder="배운 어휘나 문장 만들기 활동 등 상세 내용을 적어주세요.",
                                   key=f"area2_{lv}_{ut}")
        sub2_final = f"• 부교재: 어휘가 문해력이다 [{lv}-{ut}] ({s2_time})\n  - 활동: {sub2_custom}\n\n"

    # --- 부교재 3: 독서평설 ---
    sub3_final = ""
    if st.checkbox("3. 독서평설 포함"):
        s3_type = st.selectbox("구분", ["초등", "중등"])
        sub3_msg = st.text_area("독서평설 학습 주제 및 내용", key="area3")
        sub3_final = f"• 부교재: 독서평설({s3_type})\n  - 내용: {sub3_msg}\n\n"

    # --- 부교재 4: 신문 ---
    sub4_final = ""
    if st.checkbox("4. 신문 포함"):
        sub4_msg = st.text_area("신문 기사 요약 및 활동 내용", key="area4")
        sub4_final = f"• 부교재: 신문 활동\n  - 내용: {sub4_msg}\n\n"

    st.divider()
    footer = "아이에게 '읽은 책 자랑'을 꼭 시켜주세요~ 더불어 많은 칭찬과 격려부탁드립니다. 감사합니다!"
    comment = st.text_area("종합 피드백", value=footer)

    if st.button("🚀 리포트 생성하기", type="primary"):
        if not name:
            st.error("이름을 입력해야 리포트가 생성됩니다!")
        else:
            all_subs = sub1_final + sub2_final + sub3_final + sub4_final
            final_report = f"""[ 엘케이리드인독서논술학원 학습 리포트 ]

■ 대상: {grade} {name} 학생
■ 학습일: {report_date}

1. 주교재 도서진단 결과
■ 도서명: {v_book}
 - 진단결과: [{v_unit}] [{v_status}] {v_score}/10

2. 학습 내용 상세
• 주교재: 리드인 독서
{all_subs}
[선생님 피드백]
{comment}"""
            st.session_state.final_text = final_report
            st.session_state.page = 'result'
            st.rerun()

elif st.session_state.page == 'result':
    st.title("📄 생성된 리포트")
    st.text_area("복사해서 사용하세요", st.session_state.final_text, height=600)
    if st.button("처음으로 돌아가기"):
        st.session_state.page = 'input'
        st.rerun()
