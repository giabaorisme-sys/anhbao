
import streamlit as st
import random
import time
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="SmartBrain Sudoku",
    page_icon="🧠",
    layout="wide"
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

CHARACTERS = [
    {"name": "Tung Tung Sahur", "file": "tung_tung_sahur.jfif"},
    {"name": "Tralalero Tralala", "file": "tralalero_tralala.jfif"},
    {"name": "Brr Brr Patapim", "file": "brr_brr_patapim.jfif"},
    {"name": "Boneca Ambalabu", "file": "boneca_ambalabu.jfif"},
    {"name": "Balerina Capuchina", "file": "balerina_capuchina.jfif"},
    {"name": "Ninja Cup", "file": "ninja_cup.jfif"},
    {"name": "Bombardiro Crocodilo", "file": "bombardiro_crocodilo.jfif"},
    {"name": "Lirili Larila", "file": "lirili_larila.jfif"},
    {"name": "Chimpanzini Bananini", "file": "chimpanzini_bananini.jfif"},
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


def make_puzzle(level):
    holes = {"Dễ": 34, "Bình thường": 46, "Khó": 54}[level]
    puzzle = [row[:] for row in SOLUTION]
    coords = [(r, c) for r in range(9) for c in range(9)]
    random.Random(27 + holes).shuffle(coords)

    for r, c in coords[:holes]:
        puzzle[r][c] = 0

    return puzzle


def go(page):
    st.session_state.page = page
    st.rerun()


defaults = {
    "page": "home",
    "level": "Dễ",
    "stage": 1,
    "unlocked": 1,
    "notes": 0,
    "mistakes": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def cell_key(stage, r, c):
    return f"brainrot_cell_{stage}_{r}_{c}"


def sync_widget_keys(board, stage):
    for r in range(9):
        for c in range(9):
            if st.session_state.puzzle[r][c] == 0:
                st.session_state[cell_key(stage, r, c)] = board[r][c]


def give_hint():
    if "board" not in st.session_state or "puzzle" not in st.session_state:
        return

    puzzle = st.session_state.puzzle
    current = [row[:] for row in st.session_state.board]

    empty_cells = [
        (r, c)
        for r in range(9)
        for c in range(9)
        if puzzle[r][c] == 0 and current[r][c] != SOLUTION[r][c]
    ]

    if not empty_cells:
        st.session_state.hint_message = "Không còn ô nào cần gợi ý!"
        return

    r, c = random.choice(empty_cells)
    value = SOLUTION[r][c]
    current[r][c] = value
    st.session_state.board = current

    key = cell_key(st.session_state.stage, r, c)
    st.session_state[key] = value
    st.session_state.notes += 1
    st.session_state.hint_message = "💡 Đã điền một nhân vật đúng!"


def reset_current_game():
    if "puzzle" not in st.session_state:
        return

    board = [row[:] for row in st.session_state.puzzle]
    st.session_state.board = board
    st.session_state.hint_message = ""
    sync_widget_keys(board, st.session_state.stage)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #123e83 0, transparent 38%),
        radial-gradient(ellipse at 90% 10%, #172b70 0, transparent 35%),
        linear-gradient(145deg, #04142f, #071c43 55%, #06132c);
    color: #f6fbff;
    font-family: 'Nunito', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero {
    border: 1px solid #2b7cff;
    border-radius: 26px;
    padding: 35px 24px;
    text-align: center;
    background: linear-gradient(135deg, #0a387c, #0f1646);
    box-shadow: 0 0 28px #147bff30;
}
.logo {
    font-size: clamp(2.8rem, 7vw, 5.5rem);
    font-weight: 1000;
    letter-spacing: -3px;
    line-height: 1.1;
    color: white;
    text-shadow: 0 4px 0 #164b9e, 0 0 20px #6adfff;
}
.logo span { color: #ffd23f; }
.tagline { color: #c7e5ff; font-weight: 900; margin-top: 12px; }
.panel {
    border: 1px solid #2476d9;
    border-radius: 22px;
    padding: 20px;
    background: linear-gradient(145deg, #092b61, #061938);
    box-shadow: 0 0 22px #1676ff22;
}
.character {
    border: 1px solid #217fc4;
    border-radius: 17px;
    padding: 12px;
    text-align: center;
    background: linear-gradient(160deg, #103b70, #071a39);
    margin-bottom: 12px;
}
.character img { width: 100%; max-height: 160px; object-fit: contain; }
.pill {
    display: inline-block;
    border: 1px solid #21f1d1;
    border-radius: 999px;
    padding: 6px 18px;
    color: #a9fff2;
    background: #087b7799;
    font-weight: 900;
}
.success {
    border: 1px solid #ffc928;
    border-radius: 24px;
    padding: 28px;
    text-align: center;
    background: radial-gradient(circle at 50% 0%, #6d4b14, #091d43 65%);
    box-shadow: 0 0 35px #ffc9282c;
}
div.stButton > button {
    border-radius: 999px;
    border: 1px solid #ffdf70;
    color: #132449;
    font-weight: 900;
    background: linear-gradient(180deg, #ffe875, #ffad24);
    min-height: 2.8rem;
}
div.stButton > button:hover {
    border-color: #fff3a4;
    color: #061b3b;
    box-shadow: 0 0 18px #ffd24d80;
}
div[data-testid="stSelectbox"] > div > div {
    background: #0b2a56;
    border-color: #2875c7;
    border-radius: 10px;
}
hr { border-color: #23518c; }
[data-testid="stMetric"] {
    background: #092654;
    padding: 14px;
    border: 1px solid #1d5fa8;
    border-radius: 14px;
}
.sudoku-note { color: #b9d7ff; text-align: center; }
</style>
""", unsafe_allow_html=True)


def show_image(filename, width=None):
    path = ASSETS / filename

    if path.exists():
        try:
            image = Image.open(path)

            if width is not None:
                st.image(image, width=width)
            else:
                st.image(image, use_container_width=True)

        except Exception:
            st.warning(f"Không thể mở ảnh: assets/{filename}")
    else:
        st.info(f"Chưa tìm thấy ảnh: assets/{filename}")


def topbar(title, subtitle=""):
    left, right = st.columns([1, 5])

    with left:
        if st.button("← Quay lại", key=f"back_{st.session_state.page}"):
            if st.session_state.page == "difficulty":
                go("home")
            elif st.session_state.page == "levels":
                go("difficulty")
            else:
                go("levels")

    with right:
        st.markdown(
            f"<h2 style='text-align:center;margin:0'>{title}</h2>"
            f"<p style='text-align:center;color:#a9c9f3'>{subtitle}</p>",
            unsafe_allow_html=True,
        )


def render_characters():
    st.markdown("### 🌟 Bộ sưu tập nhân vật")
    cols = st.columns(3)

    for i, character in enumerate(CHARACTERS):
        with cols[i % 3]:
            st.markdown("<div class='character'>", unsafe_allow_html=True)
            show_image(character["file"])
            st.markdown(f"**{character['name']}**")
            st.markdown("</div>", unsafe_allow_html=True)


def start_stage(stage):
    st.session_state.stage = stage
    st.session_state.puzzle = make_puzzle(st.session_state.level)
    st.session_state.board = [row[:] for row in st.session_state.puzzle]
    st.session_state.notes = 0
    st.session_state.mistakes = 0
    st.session_state.hint_message = ""
    st.session_state.started_at = time.time()

    for r in range(9):
        for c in range(9):
            key = cell_key(stage, r, c)

            if key in st.session_state:
                del st.session_state[key]

            if st.session_state.puzzle[r][c] == 0:
                st.session_state[key] = 0

    go("game")


# TRANG CHỦ
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div style="font-size:3.5rem">🧠✨</div>
        <div class="logo">SMART<span>BRAIN</span></div>
        <div class="tagline">SUDOKU · RÈN TRÍ TUỆ · THỬ THÁCH BẢN THÂN</div>
        <p style="color:#d7eaff;font-size:1.1rem;margin-top:20px">
            Giải Sudoku, mở khóa nhân vật và chinh phục từng màn chơi!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button("▶  BẮT ĐẦU", use_container_width=True):
            go("difficulty")

    st.markdown("""
    <div class="panel">
        <h3 style="text-align:center">🌟 Khám phá SmartBrain</h3>
        <p style="text-align:center;color:#b9d7ff">
            3 cấp độ · 5 màn chơi · 9 nhân vật · Sudoku 9×9
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")


# CHỌN ĐỘ KHÓ
elif st.session_state.page == "difficulty":
    topbar("CHỌN ĐỘ KHÓ", "Hãy chọn cấp độ phù hợp với bạn")

    options = [
        ("Dễ", "🟢", "⭐☆☆", "Dành cho người mới bắt đầu"),
        ("Bình thường", "🔵", "⭐⭐☆", "Thử thách vừa phải"),
        ("Khó", "🟣", "⭐⭐⭐", "Dành cho người chơi có kinh nghiệm"),
    ]

    cols = st.columns(3)

    for col, option in zip(cols, options):
        name, emoji, stars, description = option

        with col:
            st.markdown(
                f"""
                <div class="panel" style="text-align:center;min-height:210px">
                    <div style="font-size:2.6rem">{emoji}</div>
                    <h3>{name}</h3>
                    <h3 style="color:#ffd34d">{stars}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Chọn {name}",
                key=f"level_{name}",
                use_container_width=True
            ):
                st.session_state.level = name
                go("levels")


# CHỌN MÀN CHƠI
elif st.session_state.page == "levels":
    topbar("CHỌN MÀN CHƠI", f"Độ khó: {st.session_state.level}")

    st.markdown(
        f"<p style='text-align:center'><span class='pill'>✦ {st.session_state.level} ✦</span></p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(5)

    for i in range(1, 6):
        with cols[i - 1]:
            character = CHARACTERS[i - 1]
            unlocked = i <= st.session_state.unlocked

            st.markdown("<div class='character'>", unsafe_allow_html=True)
            st.markdown(f"### Màn {i}")

            # Đã bỏ ảnh nhân vật lớn ở trang chọn màn chơi.
            st.markdown(f"**{character['name']}**")
            st.caption("⭐ Có thể chơi" if unlocked else "🔒 Đã khóa")
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button(
                "▶ Chơi" if unlocked else "🔒 Đã khóa",
                key=f"stage_{i}",
                disabled=not unlocked,
                use_container_width=True,
            ):
                start_stage(i)


# CHƠI SUDOKU
elif st.session_state.page == "game":
    topbar(
        "🧠 SUDOKU BRAINROT",
        f"Màn {st.session_state.stage}/5 • {st.session_state.level}"
    )

    puzzle = st.session_state.puzzle
    board = st.session_state.board

    def get_character_file(value):
        if value == 0:
            return None
        return ASSETS / CHARACTERS[value - 1]["file"]

    def get_character_label(value):
        if value == 0:
            return "⬜ Chọn nhân vật"
        return CHARACTERS[value - 1]["name"]

    st.markdown("""
    <div class="panel">
        <h3 style="text-align:center">🧩 BẢNG BRAINROT 9×9</h3>
        <p style="text-align:center;color:#b9d7ff">
            Mỗi nhân vật đại diện cho một giá trị. Không được trùng nhân vật
            trong cùng hàng, cột hoặc vùng 3×3.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([3, 1])

    with left:
        with st.form("brainrot_board_form"):
            updated_board = []

            for r in range(9):
                cols = st.columns(9, gap="small")
                row = []

                for c in range(9):
                    with cols[c]:
                        value = puzzle[r][c]

                        if value != 0:
                            path = get_character_file(value)

                            if path and path.exists():
                                st.image(str(path), width=46)
                            else:
                                st.markdown("❓")

                            row.append(value)

                        else:
                            key = cell_key(st.session_state.stage, r, c)

                            if key not in st.session_state:
                                st.session_state[key] = st.session_state.board[r][c]

                            selected = st.selectbox(
                                f"Ô {r+1}-{c+1}",
                                options=list(range(10)),
                                format_func=get_character_label,
                                key=key,
                                label_visibility="collapsed",
                            )

                            if selected != 0:
                                path = get_character_file(selected)

                                if path and path.exists():
                                    st.image(str(path), width=46)
                                else:
                                    st.caption("Thiếu ảnh")
                            else:
                                st.caption("⬜")

                            row.append(selected)

                updated_board.append(row)

            save = st.form_submit_button(
                "💾 LƯU BÀN CHƠI",
                use_container_width=True
            )

        if save:
            st.session_state.board = [row[:] for row in updated_board]
            st.session_state.hint_message = "✅ Đã lưu lựa chọn nhân vật!"
            st.rerun()

    with right:
        st.markdown("### 🌟 Nhân vật")

        for character in CHARACTERS:
            path = ASSETS / character["file"]

            if path.exists():
                st.image(str(path), width=90)

            st.caption(character["name"])

        if st.session_state.get("hint_message"):
            st.info(st.session_state.hint_message)

        st.button(
            "💡 Gợi ý",
            use_container_width=True,
            on_click=give_hint
        )

        if st.button("✓ KIỂM TRA", use_container_width=True):
            current_board = [row[:] for row in st.session_state.board]

            for r in range(9):
                for c in range(9):
                    if puzzle[r][c] == 0:
                        current_board[r][c] = st.session_state.get(
                            cell_key(st.session_state.stage, r, c),
                            0
                        )

            st.session_state.board = current_board

            if any(
                current_board[r][c] == 0
                for r in range(9)
                for c in range(9)
            ):
                st.warning("Bạn vẫn còn ô trống. Hãy điền đủ các ô trước khi kiểm tra.")

            elif current_board == SOLUTION:
                st.session_state.page = "success"
                st.rerun()

            else:
                st.session_state.mistakes += 1
                st.warning("Chưa đúng hết! Hãy kiểm tra các nhân vật rồi thử lại.")

        st.button(
            "↻ Chơi lại",
            use_container_width=True,
            on_click=reset_current_game
        )


# MÀN HÌNH CHIẾN THẮNG
elif st.session_state.page == "success":
    st.markdown(
        f"""
        <div class="success">
            <div style="font-size:4rem">🏆✨</div>
            <h1 style="color:#ffd44f">HOÀN THÀNH!</h1>
            <h3>Bạn đã chinh phục màn {st.session_state.stage}/5 ({st.session_state.level})</h3>
            <p>Thật tuyệt vời — trí tuệ của bạn đang lên cấp!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    a, b, c = st.columns(3)

    a.metric("Độ khó", st.session_state.level)
    b.metric("Ghi chú đã dùng", f"{st.session_state.notes} lần")
    c.metric("Điểm thưởng", 100 + max(0, 50 - st.session_state.notes * 5))

    st.write("")

    if st.session_state.stage < 5:
        if st.button("➡ TIẾP THEO", use_container_width=True):
            st.session_state.unlocked = max(
                st.session_state.unlocked,
                st.session_state.stage + 1
            )

            next_stage = st.session_state.stage + 1
            start_stage(next_stage)

    else:
        st.session_state.unlocked = 5
        st.balloons()
        st.success("Bạn đã hoàn thành toàn bộ 5 màn chơi!")

    if st.button("🏠 Về trang chủ", use_container_width=True):
        go("home")
