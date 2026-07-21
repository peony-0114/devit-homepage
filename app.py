
App · PY
import json
import os
 
import pandas as pd
import streamlit as st
 
st.set_page_config(
    page_title="3-10 디벗 정리",
    page_icon="💻",
    layout="wide",
)
 
DATA_FILE = "checklist_data.json"
NUMBERS = [n for n in range(1, 24) if n != 3]  # 1~23번, 3번 제외
 
ACC_ITEMS = ["펜슬", "유선 마우스", "가방", "충전 어댑터"]
DEVIT_ITEMS = ["자기 번호함에 넣었나요?", "자기 번호의 충전기를 연결했나요?"]
 
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
        margin-bottom: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
 
 
# ---------- 데이터 불러오기 / 저장 ----------
def default_data():
    return {
        "acc": {str(n): {item: False for item in ACC_ITEMS} for n in NUMBERS},
        "devit": {str(n): {item: False for item in DEVIT_ITEMS} for n in NUMBERS},
    }
 
 
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 번호가 새로 추가/삭제된 경우 대비해 기본값과 병합
            base = default_data()
            for section in ["acc", "devit"]:
                for n in base[section]:
                    if n in data.get(section, {}):
                        base[section][n].update(data[section][n])
            return base
        except Exception:
            return default_data()
    return default_data()
 
 
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
 
 
if "checklist_data" not in st.session_state:
    st.session_state.checklist_data = load_data()
 
data = st.session_state.checklist_data
 
 
def dict_to_df(section, items):
    rows = []
    for n in NUMBERS:
        row = {"번호": n}
        row.update(data[section][str(n)])
        rows.append(row)
    return pd.DataFrame(rows).set_index("번호")
 
 
def df_to_dict(df):
    return {str(n): {item: bool(df.loc[n, item]) for item in df.columns} for n in df.index}
 
 
# ---------- 제목 ----------
st.markdown('<div class="main-title">📦 3-10 디벗이랑 악세사리 정리하자!</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">번호별로 체크박스를 눌러서 확인해요 ✅ (표 안 칸을 바로 클릭하면 돼요)</div>', unsafe_allow_html=True)
 
# ---------- 항목 1: 악세사리 체크리스트 (표) ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎒 1. 악세사리 체크리스트</div>', unsafe_allow_html=True)
st.caption("왼쪽 열에서 내 번호를 찾아 해당 칸을 체크하세요.")
 
acc_df = dict_to_df("acc", ACC_ITEMS)
acc_column_config = {item: st.column_config.CheckboxColumn(item, default=False) for item in ACC_ITEMS}
 
acc_edited = st.data_editor(
    acc_df,
    column_config=acc_column_config,
    use_container_width=True,
    key="acc_editor",
)
 
if not acc_edited.equals(acc_df):
    data["acc"] = df_to_dict(acc_edited)
    save_data(data)
    st.rerun()
 
st.markdown('</div>', unsafe_allow_html=True)
 
# ---------- 항목 2: 디벗 체크리스트 (표) ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💻 2. 디벗 체크리스트</div>', unsafe_allow_html=True)
st.caption("왼쪽 열에서 내 번호를 찾아 해당 칸을 체크하세요.")
 
devit_df = dict_to_df("devit", DEVIT_ITEMS)
devit_column_config = {item: st.column_config.CheckboxColumn(item, default=False) for item in DEVIT_ITEMS}
 
devit_edited = st.data_editor(
    devit_df,
    column_config=devit_column_config,
    use_container_width=True,
    key="devit_editor",
)
 
if not devit_edited.equals(devit_df):
    data["devit"] = df_to_dict(devit_edited)
    save_data(data)
    st.rerun()
 
st.markdown('</div>', unsafe_allow_html=True)
 
# ---------- 전체 현황 요약 ----------
total_cells = len(NUMBERS) * (len(ACC_ITEMS) + len(DEVIT_ITEMS))
checked_cells = sum(
    1
    for n in NUMBERS
    for item in ACC_ITEMS
    if data["acc"][str(n)][item]
) + sum(
    1
    for n in NUMBERS
    for item in DEVIT_ITEMS
    if data["devit"][str(n)][item]
)
st.progress(checked_cells / total_cells if total_cells else 0)
st.caption(f"우리 반 전체 진행률: {checked_cells} / {total_cells}")
 
not_done = [
    n
    for n in NUMBERS
    if not all(data["acc"][str(n)].values()) or not all(data["devit"][str(n)].values())
]
if not_done:
    st.info("아직 다 체크하지 않은 번호: " + ", ".join(str(n) + "번" for n in not_done))
else:
    st.success("전체 다 체크 완료! 오늘도 수고했습니다 🙌")
 
# ---------- 항목 3: 웨일 수리 자기부담비 ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚠️ 3. 웨일북 수리 자기부담비</div>', unsafe_allow_html=True)
st.caption("파손·분실 시 아래 기준으로 자기부담비가 발생할 수 있어요. 미리 확인하고 소중히 다뤄주세요!")
st.image("assets/repair_fee.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
 
st.markdown("---")
st.caption("3-10반 정보부장 제작 · 매일 하교 전 체크하는 습관을 들여봐요 😊")
 
