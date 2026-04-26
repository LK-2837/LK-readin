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
    with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)

# --- [UI 메인] ---
if "page" not in st.session_state: st.session_state.page = 'input'

if st.session_state.page == 'input':
    st.title("📚 학습 리포트 생성기")

    # 기본 정보
    name = st.text_input("학생 이름")
    grade = st.selectbox("학년", ["초등", "중등", "고등"])
    report_date = st.date_input("학습일", value=datetime.today())

    st.divider()
    st.subheader("📝 주교재 진단")
    v_book = st.text_input("도서명", value="리드인 독서")
    v_unit = st.selectbox("회차", [f"{i}회차" for i in range(1, 5)])
    v_score = st.number_input("맞은 개수", 0, 10, 10)

    st.divider()
    st.subheader("📖 부교재 기록 (체크하면 입력창이 뜹니다)")

    # --- 1. 뿌리깊은 초등국어 ---
    sub1_final = ""
    if st.checkbox("뿌리깊은 초등국어 포함"):
        s1_step = st.selectbox("단계", [f"{i}단계" for i in range(1, 7)])
        s1_unit = st.selectbox("회차 ", [f"{i}회차" for i in range(1, 41)])
        s1_time = st.selectbox("소요시간", [f"{i}분" for i in range(61)], key="t1")
        db_val = SUB_BOOK_INFO.get(s1_step, {}).get(s1_unit, f"{s1_step} {s1_unit} 학습을 완료했습니다.")
        sub1_msg = st.text_area("학습 포인트", value=db_val, key=f"a1_{s1_step}_{s1_unit}")
        sub1_final = f"• 부교재: 뿌리깊은초등국어 [{s1_step}-{s1_unit}] ({s1_time})\n[학습 포인트]\n{sub1_msg}\n\n"

    # --- 2. 어휘가 문해력이다 (여기가 핵심!) ---
    sub2_final = ""
    st.write("---")
    use_sub2 = st.checkbox("어휘가 문해력이다 포함")
    
    if use_sub2:
        # 이 영역이 체크를 누르면 무조건 보여야 합니다.
        st.info("💡 아래 레벨과 회차를 고르고, 활동 내용을 입력하세요.")
        s2_lv = st.selectbox("레벨", VOCAB_LITERACY_LEVELS)
        s2_ut = st.selectbox("회차  ", [f"{i}회차" for i in range(1, 41)])
        s2_time = st.selectbox("소요시간 ", [f"{i}분" for i in range(61)], key="t2")
        
        # ❗ 이 상자가 안 보인다면 코드가 실행되지 않은 것입니다.
        sub2_custom = st.text_area("✨ 어휘가 문해력이다 상세 활동 내용", 
                                   placeholder="배운 단어나 활동 내용을 여기에 적어주세요.",
                                   key=f"a2_{s2_lv}_{s2_ut}")
        
        sub2_final = f"• 부교재: 어휘가 문해력이다 [{s2_lv}-{s2_ut}] ({s2_time})\n  - 활동: {sub2_custom}\n\n"

    st.divider()
    comment = st.text_area("선생님 피드백", value="아이에게 '읽은 책 자랑'을 시켜주세요~")

    if st.button("🚀 리포트 생성"):
        if not name:
            st.error("이름을 입력하세요.")
        else:
            total_sub = sub1_final + sub2_final
            report_text = f"""[ 학습 리포트 ]
■ 대상: {grade} {name}
■ 학습일: {report_date}

1. 주교재 진단
■ 도서명: {v_book}
 - 결과: [{v_unit}] {v_score}/10

2. 학습 내용 상세
{total_sub}
[선생님 피드백]
{comment}"""
            st.session_state.final_text = report_text
            st.session_state.page = 'result'; st.rerun()

elif st.session_state.page == 'result':
    st.title("📄 리포트 결과")
    st.text_area("복사용", st.session_state.final_text, height=500)
    if st.button("돌아가기"):
        st.session_state.page = 'input'; st.rerun()
