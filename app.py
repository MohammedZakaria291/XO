import streamlit as st
import math
import random
from collections import deque

# Custom CSS
st.markdown("""
<style>
    div[data-testid="column"] button[kind="secondary"] {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        font-size: 4.5rem !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 8px 0 !important;
        border: 3px solid #cccccc !important;
        border-radius: 12px !important;
        background-color: #f9f9f9 !important;
    }
    div[data-testid="column"] button[kind="secondary"]:disabled {
        background-color: #f0f0f0 !important;
        opacity: 1 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        max-width: 90vw !important;
        margin: 20px auto !important;
    }
    @media (max-width: 768px) {
        div[data-testid="column"] button[kind="secondary"] {
            font-size: 3.8rem !important;
            margin: 10px 0 !important;
            border-width: 4px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🎮 Tic-Tac-Toe Championship (Best of 5)")

# Difficulty selection (DFS instead of Random)
st.markdown("### Choose Computer Difficulty")
difficulty = st.radio(
    "Select how smart the computer should be:",
    options=["DFS (Easy)", "Greedy (Medium)", "Minimax (Unbeatable)"],
    index=2  # Default to Unbeatable
)

st.markdown("**You play as X** | **Computer plays as O** | **First to 3 points wins!**")

# Initialize session state
if 'scores' not in st.session_state:
    st.session_state.scores = {"Player": 0, "Computer": 0}
if 'board' not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'match_over' not in st.session_state:
    st.session_state.match_over = False

# Check winner and draw
def check_winner(board, player):
    win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(board[a] == board[b] == board[c] == player for a,b,c in win_conditions)

def check_draw(board):
    return " " not in board

def get_empty_cells(board):
    return [i for i in range(9) if board[i] == " "]

# DFS Algorithm (Depth-First Search) - Explores first possible winning path
def dfs_move():
    board = st.session_state.board.copy()
    stack = [(board, 0)]  # (current_board, depth)
    
    while stack:
        current_board, depth = stack.pop()
        if check_winner(current_board, "O"):
            # Backtrack to find the move that led to win
            return find_dfs_move()
        if check_draw(current_board):
            continue
            
        for i in get_empty_cells(current_board):
            new_board = current_board.copy()
            new_board[i] = "O"
            stack.append((new_board, depth + 1))
    
    # If no win found, pick first available
    return get_empty_cells(st.session_state.board)[0]

def find_dfs_move():
    # Simple fallback: try to win first, else first available
    board = st.session_state.board
    for i in get_empty_cells(board):
        board[i] = "O"
        if check_winner(board, "O"):
            board[i] = " "
            return i
        board[i] = " "
    return get_empty_cells(board)[0]

# Minimax (Unbeatable)
def minimax(board, depth, alpha, beta, maximizingPlayer):
    if check_winner(board, "O"): return 10 - depth
    if check_winner(board, "X"): return depth - 10
    if check_draw(board): return 0

    if maximizingPlayer:
        max_eval = -math.inf
        for i in get_empty_cells(board):
            board[i] = "O"
            eval_score = minimax(board, depth + 1, alpha, beta, False)
            board[i] = " "
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = math.inf
        for i in get_empty_cells(board):
            board[i] = "X"
            eval_score = minimax(board, depth + 1, alpha, beta, True)
            board[i] = " "
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha: break
        return min_eval

def minimax_move():
    best_score = -math.inf
    best_move = None
    for i in get_empty_cells(st.session_state.board):
        st.session_state.board[i] = "O"
        score = minimax(st.session_state.board, 0, -math.inf, math.inf, False)
        st.session_state.board[i] = " "
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

# Greedy move
def greedy_move():
    board = st.session_state.board
    # Try to win
    for i in get_empty_cells(board):
        board[i] = "O"
        if check_winner(board, "O"):
            board[i] = " "
            return i
        board[i] = " "
    # Block player win
    for i in get_empty_cells(board):
        board[i] = "X"
        if check_winner(board, "X"):
            board[i] = " "
            return i
        board[i] = " "
    # Center preference, then corners, then edges
    center = 4
    corners = [0,2,6,8]
    edges = [1,3,5,7]
    
    if center in get_empty_cells(board): return center
    for c in corners:
        if c in get_empty_cells(board): return c
    return get_empty_cells(board)[0]

# Computer move based on difficulty
def computer_move():
    if difficulty == "DFS (Easy)":
        move = dfs_move()
    elif difficulty == "Greedy (Medium)":
        move = greedy_move()
    else:  # Minimax
        move = minimax_move()
    
    if move is not None:
        st.session_state.board[move] = "O"

# Player move
def make_move(pos):
    if st.session_state.board[pos] == " " and not st.session_state.game_over:
        st.session_state.board[pos] = "X"
        
        if check_winner(st.session_state.board, "X"):
            st.session_state.game_over = True
            st.session_state.winner = "You win this round! 🎉"
            st.session_state.scores["Player"] += 1
        elif check_draw(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "Draw this round! 😐"
        else:
            with st.spinner("Computer is thinking... 💭"):
                computer_move()
            
            if check_winner(st.session_state.board, "O"):
                st.session_state.game_over = True
                st.session_state.winner = "Computer wins this round! 😢"
                st.session_state.scores["Computer"] += 1
            elif check_draw(st.session_state.board):
                st.session_state.game_over = True
                st.session_state.winner = "Draw this round! 😐"
        
        # Check if match is over (first to 3)
        if st.session_state.scores["Player"] >= 3:
            st.session_state.match_over = True
            st.session_state.winner = "🏆 CHAMPION! You win the match! 🏆"
        elif st.session_state.scores["Computer"] >= 3:
            st.session_state.match_over = True
            st.session_state.winner = "💻 Computer wins the match! 💻"
        
        st.rerun()

# Display scores
col1, col2 = st.columns(2)
with col1:
    st.metric("Your Score (X)", st.session_state.scores["Player"])
with col2:
    st.metric("Computer Score (O)", st.session_state.scores["Computer"])

# Display board
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        cell_value = st.session_state.board[i]
        if cell_value == " " and not st.session_state.game_over:
            if st.button(" ", key=f"btn_{i}", use_container_width=True):
                make_move(i)
        else:
            st.button(cell_value, key=f"cell_{i}", disabled=True, use_container_width=True)

# Game/Match result
if st.session_state.game_over:
    st.success(f"### {st.session_state.winner}")
    
    if st.button("Next Round"):
        # Reset for next round
        st.session_state.board = [" " for _ in range(9)]
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

# Match over - final screen
if st.session_state.match_over:
    st.balloons()
    st.markdown("### 🎊 Match Complete! 🎊")
    if st.button("New Championship"):
        # Reset everything
        st.session_state.scores = {"Player": 0, "Computer": 0}
        st.session_state.board = [" " for _ in range(9)]
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.match_over = False
        st.rerun()
else:
    st.markdown("---")
    st.caption("Click on any empty cell to make your move.")

# Sidebar
with st.sidebar:
    st.header("🏆 Championship Info")
    st.write("- **Format**: First to 3 points wins!")
    st.write("- You: **X**")
    st.write("- Computer: **O**")
    st.write(f"- Difficulty: **{difficulty}**")
    st.markdown("---")
    st.markdown("**Algorithms:**")
    st.write("• **DFS**: Explores depth-first (easy)")
    st.write("• **Greedy**: Smart immediate moves")
    st.write("• **Minimax**: Perfect AI")
