import streamlit as st
import chess
import chess.svg
import re
import time
import random
import json
from pathlib import Path
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Chess Opening Memorization Trainer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Progress tracking file
PROGRESS_FILE = Path.home() / ".chess_opening_progress.json"

def load_progress():
    """Load progress data from file"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_progress(progress):
    """Save progress data to file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def get_opening_status(opening_name, progress):
    """Get the status of an opening"""
    if opening_name not in progress:
        progress[opening_name] = {
            'mastered': False,
            'last_reviewed': None,
            'review_count': 0
        }
    return progress[opening_name]

def update_review(opening_name, progress):
    """Update review timestamp"""
    status = get_opening_status(opening_name, progress)
    status['last_reviewed'] = datetime.now().isoformat()
    status['review_count'] += 1
    save_progress(progress)

def toggle_mastered(opening_name, progress):
    """Toggle mastered status"""
    status = get_opening_status(opening_name, progress)
    status['mastered'] = not status['mastered']
    save_progress(progress)

def should_review(opening_name, progress):
    """Check if opening should be reviewed (spaced repetition)"""
    status = get_opening_status(opening_name, progress)
    if status['mastered']:
        return False
    if status['last_reviewed'] is None:
        return True

    last_review = datetime.fromisoformat(status['last_reviewed'])
    review_count = status['review_count']

    # Spaced repetition intervals: 1 day, 3 days, 7 days, 14 days, 30 days
    intervals = [1, 3, 7, 14, 30]
    interval_index = min(review_count, len(intervals) - 1)
    next_review = last_review + timedelta(days=intervals[interval_index])

    return datetime.now() >= next_review

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

# Load progress
progress = load_progress()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_opening' not in st.session_state:
    st.session_state.selected_opening = None
if 'mode' not in st.session_state:
    st.session_state.mode = '📖 Study'

# Sidebar
with st.sidebar:
    st.title("♟️ Opening Trainer")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("---")

    # Stats
    total = len(OPENINGS)
    mastered = sum(1 for o in OPENINGS if get_opening_status(o, progress)['mastered'])
    needs_review = sum(1 for o in OPENINGS if should_review(o, progress))

    st.metric("Mastered", f"{mastered}/{total}")
    if needs_review > 0:
        st.metric("Need Review", needs_review)

    if st.session_state.page == 'training' and st.session_state.selected_opening:
        st.markdown("---")
        st.markdown(f"**Current:**")
        st.caption(st.session_state.selected_opening.replace('White - ', '').replace('Black - ', ''))

#  HOME PAGE
if st.session_state.page == 'home':
    st.title("♟️ Chess Opening Memorization Trainer")
    st.markdown("### Master your repertoire through active practice")

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Openings", total)
    with col2:
        st.metric("Mastered", mastered, delta=f"{int(mastered/total*100)}%")
    with col3:
        if needs_review > 0:
            st.metric("Due for Review", needs_review, delta="🔔")
        else:
            st.metric("All Current", "✅")

    st.markdown("---")

    # Priority reviews
    if needs_review > 0:
        st.markdown("## 🔔 Priority Review")

        cols = st.columns(2)
        idx = 0
        for opening in OPENINGS:
            if should_review(opening, progress):
                with cols[idx % 2]:
                    status = get_opening_status(opening, progress)
                    name = opening.replace('White - ', '').replace('Black - ', '')
                    st.markdown(f"### {name}")

                    if status['last_reviewed']:
                        days = (datetime.now() - datetime.fromisoformat(status['last_reviewed'])).days
                        st.caption(f"Last reviewed {days} days ago")

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if st.button("📖 Study", key=f"pr_s_{opening}", use_container_width=True):
                            st.session_state.page = 'training'
                            st.session_state.selected_opening = opening
                            st.session_state.mode = '📖 Study'
                            st.rerun()
                    with c2:
                        if st.button("🎯 Quiz", key=f"pr_q_{opening}", use_container_width=True):
                            st.session_state.page = 'training'
                            st.session_state.selected_opening = opening
                            st.session_state.mode = '🎯 Quiz'
                            st.rerun()
                    with c3:
                        if st.button("🎲 Test", key=f"pr_t_{opening}", use_container_width=True):
                            st.session_state.page = 'training'
                            st.session_state.selected_opening = opening
                            st.session_state.mode = '🎲 Random Test'
                            st.rerun()
                    st.markdown("---")
                idx += 1

        st.markdown("---")

    # All openings
    st.markdown("## 📚 Your Repertoire")

    # White
    st.markdown("### ⚪ As White")
    white = [k for k in OPENINGS if k.startswith("White")]
    cols = st.columns(len(white))
    for i, opening in enumerate(white):
        with cols[i]:
            status = get_opening_status(opening, progress)
            name = opening.replace('White - ', '')
            check = "✅" if status['mastered'] else "⬜"

            st.markdown(f"### {check} {name}")
            st.caption(f"Reviewed {status['review_count']} times" if status['review_count'] > 0 else "Not started")

            if st.button("📖 Study", key=f"w_s_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '📖 Study'
                st.rerun()
            if st.button("🎯 Quiz", key=f"w_q_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '🎯 Quiz'
                st.rerun()
            if st.button("🎲 Test", key=f"w_t_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '🎲 Random Test'
                st.rerun()

    st.markdown("---")

    # Black vs e4
    st.markdown("### ⚫ As Black vs 1.e4")
    e4 = [k for k in OPENINGS if "Caro-Kann" in k]
    cols = st.columns(len(e4))
    for i, opening in enumerate(e4):
        with cols[i]:
            status = get_opening_status(opening, progress)
            name = opening.replace('Black - ', '')
            check = "✅" if status['mastered'] else "⬜"

            st.markdown(f"### {check} {name}")
            st.caption(f"Reviewed {status['review_count']} times" if status['review_count'] > 0 else "Not started")

            if st.button("📖 Study", key=f"e_s_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '📖 Study'
                st.rerun()
            if st.button("🎯 Quiz", key=f"e_q_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '🎯 Quiz'
                st.rerun()
            if st.button("🎲 Test", key=f"e_t_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '🎲 Random Test'
                st.rerun()

    st.markdown("---")

    # Black vs d4
    st.markdown("### ⚫ As Black vs 1.d4")
    d4 = [k for k in OPENINGS if k.startswith("Black") and "Caro-Kann" not in k]
    cols = st.columns(len(d4))
    for i, opening in enumerate(d4):
        with cols[i]:
            status = get_opening_status(opening, progress)
            name = opening.replace('Black - ', '')
            check = "✅" if status['mastered'] else "⬜"

            st.markdown(f"### {check} {name}")
            st.caption(f"Reviewed {status['review_count']} times" if status['review_count'] > 0 else "Not started")

            if st.button("📖 Study", key=f"d_s_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '📖 Study'
                st.rerun()
            if st.button("🎯 Quiz", key=f"d_q_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '🎯 Quiz'
                st.rerun()
            if st.button("🎲 Test", key=f"d_t_{i}", use_container_width=True):
                st.session_state.page = 'training'
                st.session_state.selected_opening = opening
                st.session_state.mode = '🎲 Random Test'
                st.rerun()

    st.markdown("---")

    # Tips
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**📖 Study Mode**\n\nLearn moves step-by-step")
    with c2:
        st.markdown("**🎯 Quiz Mode**\n\nTest your knowledge")
    with c3:
        st.markdown("**🎲 Random Test**\n\nJump to random positions")

# TRAINING PAGE
elif st.session_state.page == 'training':
    if not st.session_state.selected_opening:
        st.session_state.page = 'home'
        st.rerun()

    opening = st.session_state.selected_opening
    data = OPENINGS[opening]
    status = get_opening_status(opening, progress)
    mode = st.session_state.mode

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(opening)
    with col2:
        if st.button("✅ Mastered" if not status['mastered'] else "⬜ Learning", use_container_width=True):
            toggle_mastered(opening, progress)
            st.rerun()
        st.caption(f"Reviews: {status['review_count']}")

    # Mode selector
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📖 Study", use_container_width=True, type="primary" if mode == '📖 Study' else "secondary"):
            st.session_state.mode = '📖 Study'
            st.rerun()
    with c2:
        if st.button("🎯 Quiz", use_container_width=True, type="primary" if mode == '🎯 Quiz' else "secondary"):
            st.session_state.mode = '🎯 Quiz'
            st.rerun()
    with c3:
        if st.button("🎲 Test", use_container_width=True, type="primary" if mode == '🎲 Random Test' else "secondary"):
            st.session_state.mode = '🎲 Random Test'
            st.rerun()

    st.markdown("---")

    # Update review
    update_review(opening, progress)

    # Parse moves
    moves_str = re.sub(r'\d+\.', '', data["moves"])
    moves = [m.strip() for m in moves_str.split() if m.strip()]

    # Initialize states
    for key, default in [
        ('move_idx', 0), ('auto_play', False), ('quiz_correct', 0),
        ('quiz_total', 0), ('show_answer', False), ('user_guess', ''),
        ('random_idx', None)
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # Mode content
    if mode == '🎲 Random Test':
        st.markdown("### 🎲 Random Position Test")

        if st.button("🎲 Generate Random Position"):
            st.session_state.random_idx = random.randint(1, len(moves) - 1)
            st.session_state.show_answer = False

        if st.session_state.random_idx:
            idx = st.session_state.random_idx
            board = chess.Board()
            for m in moves[:idx]:
                board.push_san(m)

            st.markdown(f"**Position after move {idx}. What's next?**")
            st.image(chess.svg.board(board, size=450), use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                guess = st.text_input("Your move:", key="rnd_guess")
            with c2:
                if st.button("Check"):
                    if guess.strip() == moves[idx]:
                        st.success(f"✅ Correct! {moves[idx]}")
                        st.session_state.quiz_correct += 1
                    else:
                        st.error(f"❌ Wrong. Answer: {moves[idx]}")
                    st.session_state.quiz_total += 1
                    st.session_state.show_answer = True

            if st.session_state.show_answer:
                st.info(f"Continues: {' '.join(moves[idx:min(idx+3, len(moves))])}...")

            st.metric("Score", f"{st.session_state.quiz_correct}/{st.session_state.quiz_total}")

    elif mode == '🎯 Quiz':
        st.markdown("### 🎯 Quiz Mode")

        if st.session_state.move_idx >= len(moves) - 1:
            st.success("🎉 Completed!")
            if st.button("Restart"):
                st.session_state.move_idx = 0
                st.session_state.show_answer = False
                st.rerun()
        else:
            board = chess.Board()
            for m in moves[:st.session_state.move_idx + 1]:
                board.push_san(m)

            st.markdown(f"**Move {st.session_state.move_idx + 2}/{len(moves)}**")
            st.image(chess.svg.board(board, size=450), use_container_width=True)
            st.caption(f"Moves: {' '.join(moves[:st.session_state.move_idx + 1])}")

            if not st.session_state.show_answer:
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    guess = st.text_input("Next move?", key="quiz_in")
                with c2:
                    if st.button("✅ Check", use_container_width=True):
                        correct = moves[st.session_state.move_idx + 1]
                        if guess.strip() == correct:
                            st.session_state.quiz_correct += 1
                        st.session_state.quiz_total += 1
                        st.session_state.user_guess = guess.strip()
                        st.session_state.show_answer = True
                        st.rerun()
                with c3:
                    if st.button("💡 Reveal", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()
            else:
                correct = moves[st.session_state.move_idx + 1]
                if st.session_state.user_guess == correct:
                    st.success(f"✅ Correct! {correct}")
                else:
                    if st.session_state.user_guess:
                        st.error(f"❌ You: {st.session_state.user_guess}")
                    st.info(f"Answer: {correct}")

                # Show key idea
                for idea in data["key_ideas"]:
                    if f"Move {st.session_state.move_idx + 2}" in idea:
                        st.markdown(f"💡 {idea}")

                if st.button("➡️ Next"):
                    st.session_state.move_idx += 1
                    st.session_state.show_answer = False
                    st.session_state.user_guess = ''
                    st.rerun()

            st.metric("Score", f"{st.session_state.quiz_correct}/{st.session_state.quiz_total}")

    else:  # Study mode
        st.markdown("### 📖 Study Mode")
        st.markdown(f"**Move {st.session_state.move_idx + 1}/{len(moves)}**")

        # Navigation
        cols = st.columns([1,1,1,1,1,1,1,1], gap="small")
        if cols[0].button("⏮️", key="start", use_container_width=True):
            st.session_state.move_idx = 0
            st.session_state.auto_play = False  # Pause auto-play on manual navigation
            st.rerun()
        if cols[2].button("◀️", key="prev", use_container_width=True):
            if st.session_state.move_idx > 0:
                st.session_state.move_idx -= 1
                st.session_state.auto_play = False  # Pause auto-play on manual navigation
                st.rerun()
        if cols[4].button("▶️", key="next", use_container_width=True):
            if st.session_state.move_idx < len(moves) - 1:
                st.session_state.move_idx += 1
                st.session_state.auto_play = False  # Pause auto-play on manual navigation
                st.rerun()
        if cols[6].button("⏭️", key="end", use_container_width=True):
            st.session_state.move_idx = len(moves) - 1
            st.session_state.auto_play = False  # Pause auto-play on manual navigation
            st.rerun()

        new_idx = st.slider("Jump", 0, len(moves)-1, st.session_state.move_idx, label_visibility="collapsed")
        if new_idx != st.session_state.move_idx:
            st.session_state.move_idx = new_idx
            st.session_state.auto_play = False  # Pause auto-play on manual navigation

        # Board
        board = chess.Board()
        for m in moves[:st.session_state.move_idx + 1]:
            board.push_san(m)

        st.image(chess.svg.board(board, size=450), use_container_width=True)
        st.caption(f"Moves: {' '.join(moves[:st.session_state.move_idx + 1])}")

        # Auto-play
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.session_state.auto_play:
                if st.button("⏸️ Pause", use_container_width=True):
                    st.session_state.auto_play = False
                    st.rerun()
            else:
                if st.button("▶️ Auto", use_container_width=True):
                    st.session_state.auto_play = True
                    st.rerun()
        with c2:
            speed = st.select_slider("Speed", [0.5, 1.0, 1.5, 2.0, 3.0], 1.5,
                                    format_func=lambda x: f"{x}s", label_visibility="collapsed")

        if st.session_state.auto_play and st.session_state.move_idx < len(moves) - 1:
            time.sleep(speed)
            st.session_state.move_idx += 1
            st.rerun()
        elif st.session_state.auto_play:
            st.session_state.auto_play = False

        # Info
        st.markdown("---")
        with st.expander("🎯 Key Ideas"):
            for idea in data["key_ideas"]:
                st.markdown(f"- {idea}")
        with st.expander("📋 Plan"):
            st.info(data["plan"])
        with st.expander("♟️ Full Sequence"):
            st.code(data["moves"])

# Footer
st.markdown("---")
st.caption("**Active practice beats passive study** • Quiz yourself • Track progress")
