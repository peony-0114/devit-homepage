import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="3-10 반 홈페이지",
    page_icon="💻",
    layout="wide",
)

NUMBERS = [n for n in range(1, 24) if n != 3]  # 1~23번, 3번 제외
ACC_ITEMS = ["펜슬", "유선 마우스", "가방", "충전 어댑터"]
DEVIT_ITEMS = ["자기 번호함에 넣었나요?", "자기 번호의 충전기를 연결했나요?"]
WORKSHEET_NAME = "체크리스트"
ALL_ITEMS = ACC_ITEMS + DEVIT_ITEMS

# ---------- 스타일 ----------
st.markdown(
    """
    <style>
    .main-title { text-align: center; font-size: 2.1rem; font-weight: 800; margin-bottom: 0.2rem; }
    .sub-title { text-align: center; color: #6b7280; margin-bottom: 2rem; }
    .section-box { background-color: #f8f9fb; border: 1px solid #e5e7eb; border-radius: 14px;
                   padding: 1.3rem 1.5rem; margin-bottom: 1.6rem; }
    .section-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.4rem; }
    .source-card { background-color: #eef4ff; border: 1px solid #c7d9ff; border-radius: 12px;
                   padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
    .source-name { font-weight: 700; font-size: 1.05rem; margin-bottom: 0.2rem; }
    .news-card { background: linear-gradient(135deg, #fff7f0, #ffe9e0); border: 1px solid #ffd6c2;
                 border-radius: 16px; padding: 1.4rem 1.5rem; margin-bottom: 1rem; }
    .news-card-title { font-size: 1.1rem; font-weight: 800; color: #c2410c; margin-bottom: 0.6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 구글 시트 연결 ----------
conn = st.connection("gsheets", type=GSheetsConnection)


def load_sheet():
    """구글 시트에서 데이터를 읽어온다. 시트가 비어있으면 기본값으로 채운다."""
    try:
        df = conn.read(worksheet=WORKSHEET_NAME, ttl="30s")
        df = df.dropna(how="all")
    except Exception:
        # 읽기 자체가 실패한 경우: 빈 시트로 착각해 초기화하면 안 되므로 바로 중단
        st.error(
            "지금 구글 시트 연결이 원활하지 않아요 (요청이 많거나 일시적인 오류일 수 있어요). "
            "잠시 후 새로고침(F5)해서 다시 시도해주세요 🙏"
        )
        st.stop()

    if df.empty or "번호" not in df.columns:
        # 자동으로 덮어쓰지 않는다 — 요청 폭주 등으로 읽기가 불안정할 때
        # 실제 데이터가 있는데도 "비었다"고 오판해 지워버리는 사고를 막기 위함
        st.warning(
            "구글 시트에서 체크리스트 데이터를 찾지 못했어요. "
            "실제로 시트가 비어있는 게 맞다면 아래 버튼으로 처음 설정을 진행하고, "
            "그게 아니라면(데이터가 있는데 이 메시지가 뜬 거라면) 새로고침 후 다시 시도해주세요."
        )
        if st.button("📝 시트 처음 설정하기 (기존 데이터를 모두 지우고 새로 만듭니다)"):
            init_df = pd.DataFrame({"번호": NUMBERS})
            for item in ALL_ITEMS:
                init_df[item] = False
            try:
                conn.update(worksheet=WORKSHEET_NAME, data=init_df)
                st.success("초기 설정 완료! 위쪽에서 새로고침 해주세요.")
            except Exception as e:
                st.error(f"설정 중 오류가 발생했어요: {e}")
        st.stop()

    df["번호"] = df["번호"].astype(int)

    def to_bool(v):
        s = str(v).strip().upper()
        if s in ["TRUE", "예"]:
            return True
        if s in ["FALSE", "", "NAN", "NONE"]:
            return False
        try:
            return float(v) != 0  # "1", "1.0", 1, 1.0 등 숫자형 값 처리
        except (ValueError, TypeError):
            return False

    for item in ALL_ITEMS:
        if item not in df.columns:
            df[item] = False
        df[item] = df[item].apply(to_bool)

    return df.set_index("번호").loc[NUMBERS]


if "sheet_df" not in st.session_state:
    st.session_state.sheet_df = load_sheet()


# ---------- 탭 구성 ----------
tab1, tab2 = st.tabs(["📦 디벗·악세사리 정리", "💊 신뢰할 수 있는 건강정보 캠페인"])

# =========================================================
# 탭 1: 디벗 정리
# =========================================================
with tab1:
    full_df = st.session_state.sheet_df

    with st.expander("🔧 디버그: 시트에서 읽어온 원본 데이터 보기 (문제 해결 후 지울 예정)"):
        st.write("변환된 데이터 (앱이 실제로 사용하는 값):")
        st.dataframe(full_df)
        st.write("데이터 타입:")
        st.write(full_df.dtypes)
        st.write("원본 읽기 (raw, 변환 전):")
        try:
            raw = conn.read(worksheet=WORKSHEET_NAME, ttl=0)
            st.dataframe(raw)
            st.write("raw 데이터 타입:", raw.dtypes)
        except Exception as e:
            st.error(f"원본 읽기 실패: {e}")

    st.markdown('<div class="main-title">📦 3-10 디벗이랑 악세사리 정리하자!</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">번호별로 체크박스를 눌러서 확인해요 ✅ (표 안 칸을 바로 클릭하면 돼요)</div>', unsafe_allow_html=True)

    # 항목 1: 악세사리 체크리스트
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎒 1. 악세사리 체크리스트</div>', unsafe_allow_html=True)
    st.caption("왼쪽 열에서 내 번호를 찾아 해당 칸을 체크하세요.")

    acc_column_config = {item: st.column_config.CheckboxColumn(item, default=False) for item in ACC_ITEMS}
    acc_edited = st.data_editor(
        full_df[ACC_ITEMS],
        column_config=acc_column_config,
        use_container_width=True,
        key="acc_editor",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 항목 2: 디벗 체크리스트
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💻 2. 디벗 체크리스트</div>', unsafe_allow_html=True)
    st.caption("왼쪽 열에서 내 번호를 찾아 해당 칸을 체크하세요.")

    devit_column_config = {item: st.column_config.CheckboxColumn(item, default=False) for item in DEVIT_ITEMS}
    devit_edited = st.data_editor(
        full_df[DEVIT_ITEMS],
        column_config=devit_column_config,
        use_container_width=True,
        key="devit_editor",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 변경 사항 확인 (아직 저장은 안 함 — 로컬에서만 비교)
    new_df = pd.concat([acc_edited, devit_edited], axis=1)
    has_changes = not new_df.equals(full_df)

    save_col1, save_col2 = st.columns([1, 3])
    with save_col1:
        save_clicked = st.button("💾 저장하기", type="primary", disabled=not has_changes)
    with save_col2:
        if has_changes:
            st.caption("✏️ 체크한 내용이 아직 저장 전이에요. 다 체크했으면 저장하기를 눌러주세요.")
        else:
            st.caption("✅ 모든 변경 사항이 저장되어 있어요.")

    if save_clicked and has_changes:
        save_df = new_df.reset_index()
        try:
            conn.update(worksheet=WORKSHEET_NAME, data=save_df)
            st.cache_data.clear()  # 저장 직후 캐시를 비워, 새로고침 시 옛날 데이터가 보이지 않도록 함
            st.session_state.sheet_df = new_df
            st.success("저장됐어요!")
            st.rerun()
        except Exception as e:
            if "429" in str(e):
                st.warning("지금 접속자가 많아서 저장이 잠깐 지연되고 있어요. 몇 초 후 다시 눌러주세요 🙏")
            else:
                st.warning(f"저장 중 문제가 발생했어요: {e}")

    # 전체 현황 요약
    total_cells = len(NUMBERS) * len(ALL_ITEMS)
    checked_cells = int(full_df[ALL_ITEMS].sum().sum())
    st.progress(checked_cells / total_cells if total_cells else 0)
    st.caption(f"우리 반 전체 진행률: {checked_cells} / {total_cells}")

    not_done = [n for n in NUMBERS if not full_df.loc[n, ALL_ITEMS].all()]
    if not_done:
        st.info("아직 다 체크하지 않은 번호: " + ", ".join(str(n) + "번" for n in not_done))
    else:
        st.success("전체 다 체크 완료! 오늘도 수고했습니다 🙌")

    if st.button("🔄 새로고침", key="refresh_devit"):
        st.cache_data.clear()
        st.session_state.sheet_df = load_sheet()
        st.rerun()

    # 항목 3: 웨일 수리 자기부담비
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚠️ 3. 웨일북 수리 자기부담비</div>', unsafe_allow_html=True)
    st.caption("파손·분실 시 아래 기준으로 자기부담비가 발생할 수 있어요. 미리 확인하고 소중히 다뤄주세요!")
    st.image("assets/repair_fee.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("3-10반 정보부장 제작 · 매일 하교 전 체크하는 습관을 들여봐요 😊")


# =========================================================
# 탭 2: 신뢰할 수 있는 건강정보 캠페인
# =========================================================
with tab2:
    st.markdown('<div class="main-title">💊 신뢰할 수 있는 건강정보 찾기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">온라인 의약품 오정보 문제, 우리가 먼저 똑똑하게 확인해요</div>',
        unsafe_allow_html=True,
    )

    # 캠페인 소개
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 캠페인 소개</div>', unsafe_allow_html=True)
    st.write(
        "온라인에는 의약품에 대한 부정확한 정보가 많이 떠돌아다녀요. "
        "이 캠페인은 공신력 있는 자료원을 통해 건강정보를 확인하는 습관을 기르고, "
        "특히 청소년 사이에서 잘못 알려진 약물 오남용 문제를 함께 짚어보기 위해 만들어졌습니다."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 신뢰할 수 있는 자료원
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✅ 신뢰할 수 있는 건강정보 자료원</div>', unsafe_allow_html=True)

    sources = [
        {
            "name": "식품의약품안전처 (식약처)",
            "desc": "의약품 허가 정보, 안전성 서한, 의약품 안전 사용 정보를 제공해요.",
            "url": "https://www.mfds.go.kr",
        },
        {
            "name": "질병관리청 (질병청)",
            "desc": "감염병·만성질환 등 국가 공식 건강 통계와 예방 수칙을 제공해요.",
            "url": "https://www.kdca.go.kr",
        },
        {
            "name": "의약품안전나라",
            "desc": "개별 의약품의 허가사항, 첨부문서(효능·부작용)를 검색할 수 있어요.",
            "url": "https://nedrug.mfds.go.kr",
        },
    ]

    for s in sources:
        st.markdown(
            f"""
            <div class="source-card">
                <div class="source-name">{s['name']}</div>
                <div style="color:#374151; margin-bottom:0.4rem;">{s['desc']}</div>
                <a href="{s['url']}" target="_blank">{s['url']}</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.caption("반 게시판(교실 게시판·단체방)에도 위 자료원 링크를 함께 안내하고 있어요.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 카드뉴스: 중추신경자극제 오남용 (이미지 기반)
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 카드뉴스: "공부 잘하는 약", 정말 안전할까?</div>', unsafe_allow_html=True)
    st.caption("카드를 넘기듯 하나씩 읽어보세요.")

    # assets/cardnews/card1.png ~ card5.png (이미지 안에 텍스트가 이미 있어 캡션은 사용하지 않음)
    CARD_COUNT = 5
    card_captions = ["", "", "", "", ""]

    card_cols = st.columns(3)
    missing_cards = []
    for i in range(CARD_COUNT):
        card_path = f"assets/cardnews/card{i + 1}.png"
        with card_cols[i % 3]:
            try:
                st.image(card_path, use_container_width=True, caption=card_captions[i] or None)
            except Exception:
                missing_cards.append(i + 1)
                st.markdown(
                    f"""
                    <div class="news-card" style="text-align:center; color:#9ca3af;">
                        <div class="news-card-title" style="color:#9ca3af;">카드 {i + 1}</div>
                        아직 이미지가 등록되지 않았어요.<br>
                        <code>assets/cardnews/card{i + 1}.png</code>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if missing_cards:
        st.caption(
            f"⏳ 아직 업로드되지 않은 카드: {', '.join(str(n) for n in missing_cards)}번. "
            f"`assets/cardnews/` 폴더에 `card1.png`부터 `card5.png` 순서로 넣어주세요."
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("3-10반 신뢰할 수 있는 건강정보 찾기 캠페인 · 함께 만드는 건강한 정보 환경")
