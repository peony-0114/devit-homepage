import streamlit as st

st.set_page_config(
    page_title="3-10 디벗 정리",
    page_icon="💻",
    layout="centered",
)

# ---------- 스타일 ----------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .section-box {
        background-color: #f8f9fb;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1.6rem;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 제목 ----------
st.markdown('<div class="main-title">📦 3-10 디벗이랑 악세사리 정리하자!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">하교 전, 체크리스트로 한 번씩 확인해요 ✅</div>', unsafe_allow_html=True)

# ---------- 항목 1: 악세사리 체크리스트 ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎒 1. 악세사리 체크리스트</div>', unsafe_allow_html=True)

acc_items = ["펜슬", "유선 마우스", "가방", "충전 어댑터"]
acc_checked = []
for item in acc_items:
    checked = st.checkbox(item, key=f"acc_{item}")
    acc_checked.append(checked)

acc_done = sum(acc_checked)
st.progress(acc_done / len(acc_items))
st.caption(f"{acc_done} / {len(acc_items)} 개 확인 완료")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- 항목 2: 디벗 체크리스트 ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💻 2. 디벗 체크리스트</div>', unsafe_allow_html=True)

devit_items = ["자기 번호에 넣었나요?", "자기 번호의 충전기를 연결했나요?"]
devit_checked = []
for item in devit_items:
    checked = st.checkbox(item, key=f"devit_{item}")
    devit_checked.append(checked)

devit_done = sum(devit_checked)
st.progress(devit_done / len(devit_items))
st.caption(f"{devit_done} / {len(devit_items)} 개 확인 완료")
st.markdown('</div>', unsafe_allow_html=True)

# 전체 완료 메시지
total_done = acc_done + devit_done
total_items = len(acc_items) + len(devit_items)
if total_done == total_items:
    st.success("모든 항목을 확인했어요! 오늘도 수고했습니다 🙌")

# ---------- 항목 3: 웨일 수리 자기부담비 ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚠️ 3. 웨일북 수리 자기부담비</div>', unsafe_allow_html=True)
st.caption("파손·분실 시 아래 기준으로 자기부담비가 발생할 수 있어요. 미리 확인하고 소중히 다뤄주세요!")
st.image("assets/repair_fee.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("3-10반 정보부장 제작 · 매일 하교 전 체크하는 습관을 들여봐요 😊")
