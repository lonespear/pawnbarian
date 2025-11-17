import streamlit as st
import chess
import chess.svg
import re

# Page configuration
st.set_page_config(
    page_title="Chess Opening Explorer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Opening repertoire data
OPENINGS = {
    "White - Catalan Closed": {
        "moves": "1.d4 d5 2.c4 e6 3.Nf3 Nf6 4.g3 Be7 5.Bg2 O-O 6.O-O Nbd7 7.Qc2 c6 8.Nbd2 b6 9.e4 Bb7 10.e5 Ne8 11.cxd5 cxd5 12.Nb3 Rc8 13.Qe2 Nc7 14.Bf4 Ba6 15.Qe3",
        "key_ideas": [
            "Move 7. Qc2: Queen supports e4 advance and eyes h7",
            "Move 9. e4: THE key plan! Get space in center",
            "Move 11. cxd5: Open lines for pieces, Bg2 becomes powerful",
            "Move 14. Bf4: Develop with tempo, control central squares"
        ],
        "plan": "Control center with d4-e5 pawns. Bg2 pressures queenside. Look for tactics on d5. Improve pieces (Rooks to c1/e1)."
    },
    "White - Catalan Open": {
        "moves": "1.d4 d5 2.c4 e6 3.Nf3 Nf6 4.g3 dxc4 5.Bg2 a6 6.O-O Nc6 7.e3 Bd6 8.Qe2 b5 9.a4 Rb8 10.Nbd2 O-O 11.Nxc4 Bb7 12.Nxd6 Qxd6 13.Bd2 Rfd8 14.Rfc1 Ne7 15.Bc3",
        "key_ideas": [
            "Move 5-6: Black takes c4 pawn - don't panic! Better development compensates",
            "Move 7. e3: Flexible, supports center and prepares Qe2",
            "Move 9. a4: CRITICAL! Stop Black's ...b4 expansion",
            "Move 11. Nxc4: Finally win pawn back, trade Black's good bishop"
        ],
        "plan": "Better piece coordination. Control c-file. Look for d5 breakthrough. Bg2 aims at Black's king."
    },
    "White - Italian Game": {
        "moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.c3 Nf6 5.d4 exd4 6.cxd4 Bb4+ 7.Bd2 Bxd2+ 8.Nbxd2 d5 9.exd5 Nxd5 10.Qb3 Nce7 11.O-O O-O 12.Rfe1 c6 13.a4",
        "key_ideas": [
            "Move 4. c3: Prepares d4 break - THE key move",
            "Move 5. d4: Central break when better developed",
            "Move 6. cxd4: Recapture toward center, strong d4 pawn",
            "Move 8. Nbxd2: Knight supports center, can jump to f3/e4",
            "Move 10. Qb3: Attacks d5 and b7 simultaneously"
        ],
        "plan": "Small advantage from isolated d4 pawn. Activate rooks on e-file and c-file. Create threats before Black stabilizes."
    },
    "Black - Caro-Kann Classical": {
        "moves": "1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4 Bf5 5.Ng3 Bg6 6.h4 h6 7.Nf3 Nd7 8.h5 Bh7 9.Bd3 Bxd3 10.Qxd3 e6 11.Bd2 Ngf6 12.O-O-O Be7 13.Ne4 Nxe4 14.Qxe4 Nf6 15.Qe2 O-O",
        "key_ideas": [
            "Move 1...c6: Supports d5, keeps bishop diagonal open",
            "Move 3...dxe4: Trade center pawns for solid structure",
            "Move 4...Bf5: KEY MOVE! Bishop out BEFORE ...e6",
            "Move 6...h6: Stop White's h5 push",
            "Move 9...Bxd3: Trade dangerous dark-squared bishop"
        ],
        "plan": "Solid position with no weaknesses. Complete development (...Ngf6, ...Be7, ...O-O). Look for ...c5 break. Slightly cramped but very solid."
    },
    "Black - Caro-Kann Advance": {
        "moves": "1.e4 c6 2.d4 d5 3.e5 Bf5 4.Nf3 e6 5.Be2 c5 6.Be3 Nc6 7.c3 Qb6 8.Qb3 c4 9.Qxb6 axb6 10.Nbd2 b5 11.O-O b4",
        "key_ideas": [
            "Move 3...Bf5: Same idea - bishop out early before ...e6",
            "Move 5...c5: Attack center immediately! Undermine e5 and d4",
            "Move 7...Qb6: Dual purpose - attacks b2 and pressures d4",
            "Move 8...c4: Lock center, gives queenside space"
        ],
        "plan": "Minority attack on queenside with ...b5-b4. White has more space but position is solid. Develop ...Nd7, ...Ne7, ...Rc8. Eventually ...f6 to challenge e5."
    },
    "Black - QGD Orthodox": {
        "moves": "1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Bg5 Be7 5.e3 O-O 6.Nf3 Nbd7 7.Rc1 c6 8.Bd3 dxc4 9.Bxc4 Nd5 10.Bxe7 Qxe7 11.O-O Nxc3 12.Rxc3 e5 13.dxe5 Nxe5 14.Nxe5 Qxe5",
        "key_ideas": [
            "Move 2...e6: QGD formation - solid center, protects d5",
            "Move 4...Be7: Simple development",
            "Move 7...c6: IMPORTANT! Supports d5, prepares minority attack ideas",
            "Move 8...dxc4: Wait for Bd3, then trade it off",
            "Move 9...Nd5: Jump to center, force trade of good bishop"
        ],
        "plan": "Solid symmetrical position. Trade pieces when behind in space. Develop light-squared bishop to b7/e6. Look for ...c5 break eventually."
    },
    "Black - King's Indian": {
        "moves": "1.d4 Nf6 2.c4 g6 3.Nc3 Bg7 4.e4 d6 5.Nf3 O-O 6.Be2 e5 7.O-O Nc6 8.d5 Ne7 9.Ne1 Nd7 10.f3 f5 11.Be3 f4 12.Bf2 g5 13.Nd3 Ng6 14.c5",
        "key_ideas": [
            "Moves 1-3: King's Indian setup - fianchetto dark-squared bishop",
            "Move 5...O-O: Castle quickly for safety",
            "Move 6...e5: KEY MOVE! Play for kingside attack, not classical center",
            "Move 9...Nd7: Maneuver knight to kingside (Nd7-f6-h5/g4)",
            "Move 10...f5: ATTACK! This is KID spirit - play for checkmate"
        ],
        "plan": "SHARP! Both sides attack opposite flanks. Attack White's king with ...g5-g4, ...Ng6-f4/h5. It's a RACE to checkmate. Only play when feeling sharp!"
    }
}

# Title and introduction
st.title("♟️ Chess Opening Explorer")
st.markdown("### Interactive guide to your personalized opening repertoire")
st.markdown("---")

# Sidebar for opening selection
with st.sidebar:
    st.header("Your Repertoire")

    st.subheader("As White")
    white_openings = [k for k in OPENINGS.keys() if k.startswith("White")]

    st.subheader("As Black vs 1.e4")
    black_e4_openings = [k for k in OPENINGS.keys() if "Caro-Kann" in k]

    st.subheader("As Black vs 1.d4")
    black_d4_openings = [k for k in OPENINGS.keys() if k.startswith("Black") and "Caro-Kann" not in k]

    selected_category = st.radio(
        "Select category:",
        ["White Openings", "Black vs 1.e4", "Black vs 1.d4"]
    )

    if selected_category == "White Openings":
        opening_choice = st.selectbox("Choose opening:", white_openings)
    elif selected_category == "Black vs 1.e4":
        opening_choice = st.selectbox("Choose opening:", black_e4_openings)
    else:
        opening_choice = st.selectbox("Choose opening:", black_d4_openings)

    st.markdown("---")
    st.markdown("**Study Tips:**")
    st.markdown("- Focus on understanding, not memorizing")
    st.markdown("- Play 3 games for every 1 hour of study")
    st.markdown("- Review your games")

# Main content
opening_data = OPENINGS[opening_choice]

# Display opening name
st.header(opening_choice)

# Parse moves first (needed for navigation)
moves_str = opening_data["moves"]
# Use regex to extract only the actual moves, removing move numbers
# Pattern: remove anything like "1." or "10." etc.
moves_str_clean = re.sub(r'\d+\.', '', moves_str)
# Split by spaces and filter empty strings
moves_only = [m.strip() for m in moves_str_clean.split() if m.strip()]

# Initialize session state
if 'move_index' not in st.session_state:
    st.session_state.move_index = 0

# Navigation controls - compact for mobile
st.markdown("### 🎮 Move Navigation")
st.markdown(f"**Move {st.session_state.move_index + 1} of {len(moves_only)}**")

# Navigation buttons in a single HTML row for guaranteed horizontal layout
button_html = f"""
<style>
.nav-buttons {{
    display: flex;
    justify-content: space-between;
    gap: 5px;
    margin-bottom: 10px;
}}
.nav-buttons button {{
    flex: 1;
    padding: 10px;
    font-size: 20px;
    background-color: #262730;
    color: white;
    border: 1px solid #464646;
    border-radius: 5px;
    cursor: pointer;
}}
.nav-buttons button:hover {{
    background-color: #464646;
}}
</style>
"""
st.markdown(button_html, unsafe_allow_html=True)

# Actual buttons using Streamlit columns with gap control
btn_cols = st.columns([1, 1, 1, 1], gap="small")

with btn_cols[0]:
    if st.button("⏮️ Start", key="start", use_container_width=True):
        st.session_state.move_index = 0
        st.rerun()

with btn_cols[1]:
    if st.button("◀️ Prev", key="prev", use_container_width=True):
        if st.session_state.move_index > 0:
            st.session_state.move_index -= 1
            st.rerun()

with btn_cols[2]:
    if st.button("Next ▶️", key="next", use_container_width=True):
        if st.session_state.move_index < len(moves_only) - 1:
            st.session_state.move_index += 1
            st.rerun()

with btn_cols[3]:
    if st.button("End ⏭️", key="end", use_container_width=True):
        st.session_state.move_index = len(moves_only) - 1
        st.rerun()

# Slider below buttons for precise control
new_index = st.slider(
    "Jump to move",
    0,
    len(moves_only) - 1,
    st.session_state.move_index,
    label_visibility="collapsed"
)
if new_index != st.session_state.move_index:
    st.session_state.move_index = new_index

st.markdown("---")

# Board visualization section
st.subheader("♟️ Board Position")

# Create board and apply moves
board = chess.Board()
moves_to_apply = moves_only[:st.session_state.move_index + 1]

try:
    for move in moves_to_apply:
        board.push_san(move)

    # Display board - responsive sizing
    board_svg = chess.svg.board(board, size=450)
    st.image(board_svg, use_container_width=True)

    # Show moves played
    if moves_to_apply:
        st.caption(f"Moves: {' '.join(moves_to_apply)}")

except Exception as e:
    st.error(f"Error displaying board: {e}")
    st.text("Board display requires valid chess moves")

st.markdown("---")

# Collapsible sections for ideas and plan - better for mobile
with st.expander("🎯 Key Ideas", expanded=False):
    for idea in opening_data["key_ideas"]:
        st.markdown(f"- {idea}")

with st.expander("📋 Your Plan", expanded=False):
    st.info(opening_data["plan"])

with st.expander("♟️ Full Move Sequence", expanded=False):
    st.code(opening_data["moves"], language=None)

with st.expander("⚙️ Technical Details", expanded=False):
    st.text(f"FEN: {board.fen()}")

# Footer
st.markdown("---")
st.caption("""
**Remember:** Understanding beats memorization • Don't hang pieces - tactics are still #1 priority
""")
