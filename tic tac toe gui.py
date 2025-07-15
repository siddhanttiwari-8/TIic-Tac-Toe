import tkinter as tk
from tkinter import messagebox
import random
import winsound

def play_sound(freq, duration):
    winsound.Beep(freq, duration)

def on_click(r, c):
    global player, mode, countdown_seconds, timer_id

    if buttons[r][c]["text"] == " ":
        buttons[r][c]["text"] = player
        play_sound(600, 100)
        stop_timer()
        if check_win(player):
            highlight_win(player)
            update_score(player)
            play_sound(800, 300)
            winner_name = get_player_name(player)
            messagebox.showinfo("Game Over", f"{winner_name} ({player}) wins!")
            reset_board()
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            player = "O" if player == "X" else "X"
            start_timer()
            if mode.get() == "AI" and player == ai_mark.get():
                window.after(500, ai_move)

def get_player_name(mark):
    if mode.get() == "AI":
        return player1_name.get() if mark == user_mark.get() else player2_name.get()
    else:
        return player1_name.get() if mark == user_mark.get() else player2_name.get()

def check_win(mark):
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] == mark:
            return [(i,0), (i,1), (i,2)]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] == mark:
            return [(0,i), (1,i), (2,i)]
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == mark:
        return [(0,0), (1,1), (2,2)]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == mark:
        return [(0,2), (1,1), (2,0)]
    return None

def check_draw():
    for row in buttons:
        for btn in row:
            if btn["text"] == " ":
                return False
    return True

def highlight_win(mark):
    win_coords = check_win(mark)
    if win_coords:
        for (i,j) in win_coords:
            buttons[i][j]["bg"] = "lightgreen"

def reset_board():
    global player
    player = user_mark.get()
    for row in buttons:
        for btn in row:
            btn["text"] = " "
            btn["bg"] = "white"
    start_timer()

def update_score(winner):
    if winner == "X":
        scores["X"] += 1
    elif winner == "O":
        scores["O"] += 1
    update_score_labels()

def update_score_labels(*args):
    score_label_X.config(text=f"{get_player_name('X')} (X): {scores['X']}")
    score_label_O.config(text=f"{get_player_name('O')} (O): {scores['O']}")

def ai_move():
    if difficulty.get() == "Easy":
        empty_cells = [(i,j) for i in range(3) for j in range(3) if buttons[i][j]["text"] == " "]
        move = random.choice(empty_cells)
        on_click(move[0], move[1])
    else:
        best_score = -float('inf')
        move = None
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == " ":
                    buttons[i][j]["text"] = ai_mark.get()
                    score = minimax(False)
                    buttons[i][j]["text"] = " "
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        if move:
            on_click(move[0], move[1])

def minimax(is_maximizing):
    if check_win(ai_mark.get()):
        return 1
    if check_win(user_mark.get()):
        return -1
    if check_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == " ":
                    buttons[i][j]["text"] = ai_mark.get()
                    score = minimax(False)
                    buttons[i][j]["text"] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == " ":
                    buttons[i][j]["text"] = user_mark.get()
                    score = minimax(True)
                    buttons[i][j]["text"] = " "
                    best_score = min(score, best_score)
        return best_score

def start_timer():
    global countdown_seconds, timer_id
    countdown_seconds = 10
    update_timer()

def update_timer():
    global countdown_seconds, timer_id
    timer_label.config(text=f"Timer: {countdown_seconds}")
    if countdown_seconds > 0:
        countdown_seconds -= 1
        timer_id = window.after(1000, update_timer)
    else:
        messagebox.showinfo("Time's up!", f"{get_player_name(player)} ({player}) ran out of time!")
        player_switch()
        start_timer()

def stop_timer():
    global timer_id
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None

def player_switch():
    global player
    player = "O" if player == "X" else "X"

def update_ai_mark(*args):
    ai_mark.set("O" if user_mark.get() == "X" else "X")
    update_score_labels()

# Main window setup
window = tk.Tk()
window.title("Tic Tac Toe Final Enhanced")

player = "X"
buttons = []
scores = {"X": 0, "O": 0}
countdown_seconds = 10
timer_id = None

# Player name inputs
tk.Label(window, text="Player 1 Name:").grid(row=0, column=0)
player1_name = tk.Entry(window)
player1_name.insert(0, "Player 1")
player1_name.grid(row=0, column=1)

tk.Label(window, text="Player 2 Name / AI:").grid(row=0, column=2)
player2_name = tk.Entry(window)
player2_name.insert(0, "Player 2 / AI")
player2_name.grid(row=0, column=3)

player1_name.bind("<KeyRelease>", update_score_labels)
player2_name.bind("<KeyRelease>", update_score_labels)

# Mode toggle
mode = tk.StringVar(value="AI")
tk.Radiobutton(window, text="Player vs AI", variable=mode, value="AI").grid(row=1, column=0)
tk.Radiobutton(window, text="Player vs Player", variable=mode, value="PvP").grid(row=1, column=1)

# Difficulty toggle
difficulty = tk.StringVar(value="Hard")
tk.Label(window, text="Difficulty:").grid(row=1, column=2)
tk.OptionMenu(window, difficulty, "Easy", "Hard").grid(row=1, column=3)

# Choose X or O
tk.Label(window, text="You play:").grid(row=2, column=0)
user_mark = tk.StringVar(value="X")
tk.OptionMenu(window, user_mark, "X", "O").grid(row=2, column=1)
ai_mark = tk.StringVar(value="O" if user_mark.get()=="X" else "X")
user_mark.trace("w", update_ai_mark)

# Score labels
score_label_X = tk.Label(window, text=f"{get_player_name('X')} (X): 0", font=('normal', 12))
score_label_X.grid(row=2, column=2)
score_label_O = tk.Label(window, text=f"{get_player_name('O')} (O): 0", font=('normal', 12))
score_label_O.grid(row=2, column=3)

# Timer label
timer_label = tk.Label(window, text="Timer: 10", font=('normal', 12), fg='red')
timer_label.grid(row=3, column=0, columnspan=4)

# Restart button
restart_btn = tk.Button(window, text="Restart", font=('normal', 12), command=reset_board, bg='lightblue')
restart_btn.grid(row=4, column=0, columnspan=4, sticky='we')

# Create board buttons
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text=" ", font=('normal', 40), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c), bg='white')
        btn.grid(row=i+5, column=j)
        row.append(btn)
    buttons.append(row)

start_timer()
window.mainloop()
