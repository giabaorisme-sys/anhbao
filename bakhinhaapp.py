

import random
import time
from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="SmartBrain Sudoku",
    page_icon="🧠",
    layout="wide",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

CHARACTERS = [
    {"name": "Tung Tung Sahur", "file": "tung_tung_sahur.jfif", "sound": "tung_tung_sahur.mp3"},
    {"name": "Tralalero Tralala", "file": "tralalero_tralala.jfif", "sound": "tralalero_tralala.mp3"},
    {"name": "Brr Brr Patapim", "file": "brr_brr_patapim.jfif", "sound": "brr_brr_patapim.mp3"},
    {"name": "Boneca Ambalabu", "file": "boneca_ambalabu.jfif", "sound": "boneca_ambalabu.mp3"},
    {"name": "Balerina Capuchina", "file": "balerina_capuchina.jfif", "sound": "ballerina_cappuccina.mp3"},
    {"name": "Ninja Cup", "file": "ninja_cup.jfif", "sound": "ninja_cup.mp3"},
    {"name": "Bombardiro Crocodilo", "file": "bombardiro_crocodilo.jfif", "sound": "bombardiro_crocodilo.mp3"},
    {"name": "Lirili Larila", "file": "lirili_larila.jfif", "sound": "liril_laril.mp3"},
    {"name": "Chimpanzini Bananini", "file": "chimpanzini_bananini.jfif", "sound": "chimpanzini_bananini.mp3"},
]

SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.stApp {
    background: radial-gradient(circle at top left, #173b70 0, #09152d 42%, #050b18 100%);
    color: #f2f7ff;
}
.block-container { padding-top: 1.5rem; max-width: 1450px; }
h1, h2, h3, p, label { color: #f2f7ff; }
.hero {
    padding: 1.5rem 1.8rem; border-radius: 24px;
    background: linear-gradient(120deg, rgba(20,58,111,.96), rgba(12,23,48,.96));
    border: 1px solid rgba(105,177,255,.35);
    box-shadow: 0 15px 45px rgba(0,0,0,.22);
    margin-bottom: 1.2rem;
}
.hero h1 { margin: 0; font-size: clamp(2rem, 5vw, 3.7rem); font-weight: 900; letter-spacing: 1px; }
.hero h1 span { color: #55d8ff; }
.hero p { margin: .4rem 0 0; color: #c8ddff; }
.panel {
    padding: 1rem 1.1rem; border-radius: 18px;
    background: rgba(17,35,67,.82); border: 1px solid rgba(105,177,255,.24);
    margin-bottom: .8rem;
}
.small-note { color: #b8c9e5; font-size: .9rem; }
div.stButton > button {
    border-radius: 12px; border: 1px solid #4b9df5;
    background: linear-gradient(135deg, #1a5aa2, #12366d);
    color: white; font-weight: 800; min-height: 2.6rem;
}
div.stButton > button:hover { border-color: #76e4ff; color: white; }
div[data-testid="stSelectbox"] label { color: #c9ddff; }
hr { border-color: rgba(120,170,230,.25); }
</style>
""", unsafe_allow_html=True)


def show_image(filename, width=None):
    path = ASSETS / filename
    if path.exists():
        try:
            st.image(Image.open(path), width=width)
            return True
        except Exception:
            pass
    st.caption(f"Thiếu ảnh: assets/{filename}")
    return False


def audio_html(filename):
    path = ASSETS / filename
    if not path.exists():
        st.warning(f"Chưa tìm thấy âm thanh: assets/{filename}")
        return

    import base64
    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    st.markdown(
        f'<audio controls autoplay style="width:100%" '
        f'src="data:audio/mpeg;base64,{data}"></audio>',
        unsafe_allow_html=True,
    )


def go(page):
    st.session_state.page = page
    st.rerun()


def make_puzzle(level):
    holes = {"Dễ": 34, "Bình thường": 46, "Khó": 54}.get(level, 34)
    puzzle = [row[:] for row in SOLUTION]
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    for r, c in positions[:holes]:
        puzzle[r][c] = 0
    return puzzle


def reset_game():
    st.session_state.puzzle = make_puzzle(st.session_state.level)
    st.session_state.board = [row[:] for row in st.session_state.puzzle]
    st.session_state.notes = 0
    st.session_state.mistakes = 0
    st.session_state.started_at = time.time()
    st.session_state.selected_character = 1
    st.session_state.sound_character = None


def fmt_character(value):
    if value == 0:
        return "⬜ Chọn nhân vật"
    return CHARACTERS[value - 1]["name"]


def board_complete():
    return all(
        st.session_state.board[r][c] == SOLUTION[r][c]
        for r in range(9)
        for c in range(9)
    )


defaults = {
    "page": "home",
    "level": "Dễ",
    "stage": 1,
    "unlocked": 1,
    "notes": 0,
    "mistakes": 0,
    "selected_character": 1,
    "sound_character": None,
    "puzzle": [row[:] for row in SOLUTION],
    "board": [row[:] for row in SOLUTION],
    "started_at": time.time(),
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown(
    '<div class="hero"><h1>SMART<span>BRAIN</span> 🧠</h1>'
    '<p>SUDOKU · RÈN TRÍ TUỆ · THỬ THÁCH BẢN THÂN</p>'
    '<p>Giải Sudoku, mở khóa nhân vật và chinh phục từng màn chơi!</p></div>',
    unsafe_allow_html=True,
)

if st.session_state.page == "home":
    st.markdown("## Chào mừng đến với Sudoku Brainrot!")
    st.markdown(
        '<div class="panel">Mỗi nhân vật đại diện cho một giá trị Sudoku. '
        'Một hàng, một cột và mỗi ô vuông 3×3 không được lặp nhân vật.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🟢 Dễ")
        if st.button("Chọn Dễ", use_container_width=True):
            st.session_state.level = "Dễ"
            go("levels")

    with c2:
        st.markdown("### 🟡 Bình thường")
        if st.button("Chọn Bình thường", use_container_width=True):
            st.session_state.level = "Bình thường"
            go("levels")

    with c3:
        st.markdown("### 🔴 Khó")
        if st.button("Chọn Khó", use_container_width=True):
            st.session_state.level = "Khó"
            go("levels")

    st.divider()
    st.markdown("### Nhân vật trong game")
    gallery = st.columns(9)

    for i, char in enumerate(CHARACTERS):
        with gallery[i]:
            show_image(char["file"], width=82)
            st.caption(f"{i + 1}. {char['name']}")

elif st.session_state.page == "levels":
    left_top, right_top = st.columns([3, 1])

    with left_top:
        st.markdown(f"## 🗺️ Chọn màn chơi · Độ khó: {st.session_state.level}")
        st.caption("Chọn một màn đã mở khóa để bắt đầu.")

    with right_top:
        if st.button("← Trang chủ", use_container_width=True):
            go("home")

    for start in range(1, 6, 2):
        cards = st.columns(2)

        for offset in range(2):
            stage_num = start + offset
            if stage_num > 5:
                continue

            with cards[offset]:
                unlocked = stage_num <= st.session_state.unlocked
                st.markdown(
                    f"### {'🔓' if unlocked else '🔒'} Màn {stage_num}"
                )
                st.write(
                    "Nhân vật: " + CHARACTERS[stage_num - 1]["name"]
                )

                # Không hiển thị ảnh nhân vật lớn ở màn chọn màn chơi.
                if unlocked:
                    if st.button(
                        f"CHƠI MÀN {stage_num}",
                        key=f"stage_{stage_num}",
                        use_container_width=True,
                    ):
                        st.session_state.stage = stage_num
                        reset_game()
                        go("game")
                else:
                    st.button(
                        "Chưa mở khóa",
                        key=f"locked_{stage_num}",
                        disabled=True,
                        use_container_width=True,
                    )

    if st.button("🔄 Đổi độ khó"):
        go("home")

elif st.session_state.page == "game":
    top1, top2, top3, top4 = st.columns([2, 1, 1, 1])

    with top1:
        st.markdown("## 🧠 SUDOKU BRAINROT")
        st.caption(f"Màn {st.session_state.stage}/5 · {st.session_state.level}")

    with top2:
        st.metric("Gợi ý", st.session_state.notes)

    with top3:
        st.metric("Lỗi", st.session_state.mistakes)

    with top4:
        if st.button("← Chọn màn", use_container_width=True):
            go("levels")

    left, right = st.columns([3, 1.15], gap="large")

    with left:
        st.markdown("### 🧩 Bảng Brainrot 9×9")
        st.caption(
            "Ô có sẵn được khóa. Ở ô trống, chọn nhân vật trong danh sách "
            "bên dưới từng ô. Có thể đổi nhân vật ở ô đã điền."
        )

        for r in range(9):
            cols = st.columns(9, gap="small")

            for c in range(9):
                with cols[c]:
                    val = st.session_state.board[r][c]
                    given = st.session_state.puzzle[r][c] != 0
                    key = f"cell_{st.session_state.stage}_{r}_{c}"

                    if val != 0:
                        char = CHARACTERS[val - 1]
                        path = ASSETS / char["file"]

                        if path.exists():
                            st.image(str(path), use_container_width=True)
                        else:
                            st.markdown(f"**{val}**")

                        if not given:
                            chosen = st.selectbox(
                                f"Ô {r + 1},{c + 1}",
                                options=list(range(10)),
                                index=val,
                                format_func=fmt_character,
                                key=key,
                                label_visibility="collapsed",
                            )
                            if chosen != val:
                                st.session_state.board[r][c] = chosen
                                st.rerun()
                        else:
                            st.caption("🔒")
                    else:
                        st.markdown(
                            '<div style="height:38px;display:flex;'
                            'align-items:center;justify-content:center;'
                            'border:1px dashed #4d78ac;border-radius:7px;'
                            'color:#8eb7e8;">?</div>',
                            unsafe_allow_html=True,
                        )

                        chosen = st.selectbox(
                            f"Ô {r + 1},{c + 1}",
                            options=list(range(10)),
                            index=0,
                            format_func=fmt_character,
                            key=key,
                            label_visibility="collapsed",
                        )

                        if chosen != 0:
                            st.session_state.board[r][c] = chosen
                            st.rerun()

            if r in (2, 5):
                st.markdown(
                    '<hr style="margin:3px 0;border-top:2px solid #65baff;">',
                    unsafe_allow_html=True,
                )

        a, b, c = st.columns(3)

        with a:
            if st.button("💡 Gợi ý", use_container_width=True):
                empties = [
                    (r, c)
                    for r in range(9)
                    for c in range(9)
                    if st.session_state.puzzle[r][c] == 0
                    and st.session_state.board[r][c] != SOLUTION[r][c]
                ]

                if empties:
                    r, c = random.choice(empties)
                    st.session_state.board[r][c] = SOLUTION[r][c]
                    st.session_state.notes += 1
                    st.rerun()
                else:
                    st.info("Không còn ô cần gợi ý!")

        with b:
            if st.button("✅ Kiểm tra", use_container_width=True):
                if board_complete():
                    st.session_state.unlocked = min(
                        5,
                        max(
                            st.session_state.unlocked,
                            st.session_state.stage + 1,
                        ),
                    )
                    go("success")
                else:
                    st.session_state.mistakes += 1
                    st.error(
                        "Chưa đúng hết đâu m! Kiểm tra các ô trống hoặc sai nhé."
                    )

        with c:
            if st.button("🔄 Chơi lại", use_container_width=True):
                reset_game()
                st.rerun()

    with right:
        st.markdown("### 🎭 Chọn nhân vật")
        st.caption("Bấm nút dưới ảnh để chọn nhân vật và nghe âm thanh.")

        for i, char in enumerate(CHARACTERS, start=1):
            item_cols = st.columns([1, 1.35])

            with item_cols[0]:
                show_image(char["file"], width=76)

            with item_cols[1]:
                selected = st.session_state.selected_character == i

                if st.button(
                    ("✅ " if selected else "") + char["name"],
                    key=f"select_char_{i}",
                    use_container_width=True,
                ):
                    st.session_state.selected_character = i
                    st.session_state.sound_character = i
                    st.rerun()

                if selected:
                    st.caption("Đang chọn")

        if st.session_state.sound_character:
            idx = st.session_state.sound_character - 1
            st.markdown("**Âm thanh nhân vật đã chọn:**")
            audio_html(CHARACTERS[idx]["sound"])

elif st.session_state.page == "success":
    st.markdown("## 🎉 HOÀN THÀNH!")
    st.markdown(f"### M đã chinh phục màn {st.session_state.stage}/5!")
    st.write("Giỏi lắm! Mở khóa màn tiếp theo và tiếp tục thử thách.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➡️ Màn tiếp theo", use_container_width=True):
            if st.session_state.stage < 5:
                st.session_state.stage += 1
                st.session_state.unlocked = max(
                    st.session_state.unlocked,
                    st.session_state.stage,
                )
                reset_game()
                go("game")
            else:
                go("home")

    with col2:
        if st.button("🗺️ Về chọn màn", use_container_width=True):
            go("levels")
