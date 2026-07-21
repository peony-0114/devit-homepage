# 3-10 디벗 정리 홈페이지

반 친구들에게 디벗·악세사리 관리 및 웨일북 수리 자기부담비를 안내하는 Streamlit 페이지입니다.

## 폴더 구조
```
devit-homepage/
├── app.py              # 메인 앱 코드
├── requirements.txt    # 필요한 패키지 목록
├── assets/
│   └── repair_fee.png  # 자기부담비 안내 이미지
└── README.md
```

## 1. 로컬에서 먼저 확인하기 (선택)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 2. GitHub에 올리기
1. GitHub에서 새 저장소(Repository)를 만듭니다. (예: `devit-homepage`)
2. 이 폴더(`devit-homepage`) 전체를 저장소에 업로드합니다.
   - GitHub Desktop을 쓰거나, 웹에서 "Add file → Upload files"로 `app.py`, `requirements.txt`, `assets/repair_fee.png`를 그대로 올리면 됩니다.
   - 터미널을 쓴다면:
     ```bash
     git init
     git add .
     git commit -m "디벗 정리 홈페이지 첫 업로드"
     git branch -M main
     git remote add origin https://github.com/내계정/devit-homepage.git
     git push -u origin main
     ```

## 3. Streamlit Community Cloud로 배포하기
1. https://share.streamlit.io 접속 후 GitHub 계정으로 로그인합니다.
2. "New app" 버튼 클릭
3. 방금 올린 저장소(`devit-homepage`)와 브랜치(`main`)를 선택합니다.
4. Main file path에 `app.py`를 입력합니다.
5. "Deploy" 클릭하면 몇 분 안에 `https://내앱이름.streamlit.app` 같은 주소가 생성됩니다.
6. 그 주소를 반 친구들에게 공유하면 끝!

## 나중에 내용 수정하고 싶을 때
`app.py`의 리스트 부분만 수정하면 됩니다.
```python
acc_items = ["펜슬", "유선 마우스", "가방", "충전 어댑터"]
devit_items = ["자기 번호에 넣었나요?", "자기 번호의 충전기를 연결했나요?"]
```
수정 후 GitHub에 다시 push하면 Streamlit Cloud에 자동으로 반영됩니다.
