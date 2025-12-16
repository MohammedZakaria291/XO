import streamlit as st
import math

# Add custom CSS to make the board responsive and larger on mobile
st.markdown("""
<style>
    /* Center the board and make it responsive */
    div[data-testid="column"]:has(> div > div > button[kind="secondary"]) {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Style the buttons to be square, larger, and touch-friendly */
    button[kind="secondary"] {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        font-size: 4rem !important;  /* Large X/O */
        padding: 0 !important;
        margin: 5px 0 !important;
    }
    
    /* Make the grid container responsive */
    div[data-testid="stHorizontalBlock"] {
        max-width: 90vw !important;
        margin: 0 auto !important;
    }
    
    /* Larger text for displayed X/O */
    div[style*="font-size: 60px"] {
        font-size: 4rem !important;
    }
    
    /* Media query for smaller screens (mobile) */
    @media (max-width: 768px) {
        button[kind="secondary"] {
            font-size: 3.5rem !important;
            margin: 8px 0 !important;
        }
        div[style*="font-size: 60px"] {
            font-size: 3.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🎮 Tic-Tac-Toe (XO)")
st.markdown("**You play as X** | **Computer plays as O**")
st.markdown("The computer is unbeatable (it will always win or draw) thanks to the Minimax algorithm with Alpha-Beta Pruning.")

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

# Check for a winner
def check_winner(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8], # Rows
        [0,3,6], [1,4,7], [2,5,8], # Columns
        [0,4,8], [2,4,6] # Diagonals
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] == player:
            return True
    return False

# Check for draw
def check_draw(board):
    return " " not in board

# Minimax with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    if check_winner(board, "O"):
        return 10 - depth
    if check_winner(board, "X"):
        return depth - 10
    if check_draw(board):
        return 0
    if maximizingPlayer: # Computer (O)
        max_eval = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                eval_score = minimax(board, depth + 1, alpha, beta, False)
                board[i] = " "
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else: # Player (X)
        min_eval = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                eval_score = minimax(board, depth + 1, alpha, beta, True)
                board[i] = " "
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval

# Computer's best move
def computer_move():
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if st.session_state.board[i] == " ":
            st.session_state.board[i] = "O"
            score = minimax(st.session_state.board, 0, -math.inf, math.inf, False)
            st.session_state.board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        st.session_state.board[best_move] = "O"

# Player's move
def make_move(pos):
    if st.session_state.board[pos] == " " and not st.session_state.game_over:
        st.session_state.board[pos] = "X"
       
        # Check if player won
        if check_winner(st.session_state.board, "X"):
            st.session_state.game_over = True
            st.session_state.winner = "Congratulations! You won! 🎉"
        # Check for draw
        elif check_draw(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "It's a draw! 😐"
        else:
            # Computer's turn with loading spinner
            with st.spinner("Computer is thinking... 💭"):
                computer_move()
           
            # Re-check after computer's move
            if check_winner(st.session_state.board, "O"):
                st.session_state.game_over = True
                st.session_state.winner = "Computer wins! 😢"
            elif check_draw(st.session_state.board):
                st.session_state.game_over = True
                st.session_state.winner = "It's a draw! 😐"
           
            # Force rerun to update the board immediately
            st.rerun()

# Display the board with 3 columns
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        cell_value = st.session_state.board[i]
        if cell_value == " " and not st.session_state.game_over:
            if st.button(" ", key=f"btn_{i}", use_container_width=True):
                make_move(i)
        else:
            # Display X or O centered and large
            st.markdown(f"<div style='text-align: center; height: 100%; display: flex; align-items: center; justify-content: center;'>{cell_value}</div>", unsafe_allow_html=True)
            # Disabled button to maintain grid alignment
            st.button(cell_value or " ", key=f"disabled_{i}", disabled=True, use_container_width=True)

# Game result
if st.session_state.game_over:
    st.success(f"### {st.session_state.winner}")
    if st.button("Play Again"):
        st.session_state.board = [" " for _ in range(9)]
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()
else:
    st.markdown("---")
    st.caption("Click on any empty cell to make your move.")

# Sidebar
with st.sidebar:
    st.header("Game Info")
    st.write("- You: **X**")
    st.write("- Computer: **O**")
    st.write("- Algorithm: Minimax + Alpha-Beta Pruning")
    st.write("- The computer is **unbeatable**!")
