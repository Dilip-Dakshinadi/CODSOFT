import tkinter as tk
from tkinter import messagebox
import random

BG_DARK = "#0a0e17"
CARD_BG = "#131c2e"
CARD_BORDER = "#1e293b"
TEXT_LIGHT = "#f8fafc"
TEXT_MUTED = "#94a3b8"

COLOR_ROCK = "#f43f5e"
COLOR_PAPER = "#06b6d4"
COLOR_SCISSORS = "#10b981"
COLOR_EMERALD = "#10b981"
COLOR_GOLD = "#f59e0b"
COLOR_PURPLE = "#a855f7"
COLOR_BLUE = "#3b82f6"

CHOICE_DATA = {
    "Rock": {
        "symbol": "🪨",
        "battle_emoji": "✊",
        "name": "Rock",
        "color": COLOR_ROCK,
        "beats": "Scissors",
        "verb": "crushes"
    },
    "Paper": {
        "symbol": "📄",
        "battle_emoji": "✋",
        "name": "Paper",
        "color": COLOR_PAPER,
        "beats": "Rock",
        "verb": "covers"
    },
    "Scissors": {
        "symbol": "✂️",
        "battle_emoji": "✌️",
        "name": "Scissors",
        "color": COLOR_SCISSORS,
        "beats": "Paper",
        "verb": "cuts"
    }
}

CHOICES = ["Rock", "Paper", "Scissors"]

user_score = 0
computer_score = 0
ties = 0
current_streak = 0
best_streak = 0
total_rounds = 0
is_animating = False
history_log = []

def set_buttons_state(state):
    for btn in choice_buttons:
        btn.config(state=state)
    reset_btn.config(state=state)

def animate_duel_step(user_choice, final_computer_choice, step=0):
    global is_animating

    rolling_symbols = ["✊", "✋", "✌️", "🪨", "📄", "✂️"]
    countdown_texts = [
        "⚡ ROCK...",
        "⚡ PAPER...",
        "⚡ SCISSORS...",
        "💥 SHOOT!"
    ]

    if step < 10:
        random_sym = random.choice(rolling_symbols)
        bot_symbol_label.config(text=random_sym, fg=random.choice([COLOR_ROCK, COLOR_PAPER, COLOR_SCISSORS]))
        
        user_symbol_label.config(text="✊", fg=COLOR_GOLD)

        countdown_idx = min(step // 3, len(countdown_texts) - 1)
        result_label.config(
            text=f"{countdown_texts[countdown_idx]}  [{step * 10}%]",
            fg=COLOR_PURPLE
        )

        vs_label.config(text="💥" if step % 2 == 0 else "⚔️")

        delay = 50 + (step * 8)
        root.after(delay, lambda: animate_duel_step(user_choice, final_computer_choice, step + 1))
    else:
        finish_round(user_choice, final_computer_choice)

def play_game(user_choice):
    global is_animating
    if is_animating:
        return

    is_animating = True
    set_buttons_state(tk.DISABLED)

    user_data = CHOICE_DATA[user_choice]
    user_name_badge.config(text=f"{user_data['symbol']} {user_data['name']}", fg=user_data['color'])
    bot_name_badge.config(text="🤖 Computing...", fg=TEXT_MUTED)

    computer_choice = random.choice(CHOICES)

    animate_duel_step(user_choice, computer_choice)

def pulse_winner_animation(widget, primary_color, secondary_color, count=6):
    if count > 0:
        next_color = primary_color if count % 2 == 0 else secondary_color
        widget.config(fg=next_color)
        root.after(110, lambda: pulse_winner_animation(widget, primary_color, secondary_color, count - 1))
    else:
        widget.config(fg=primary_color)

def finish_round(user_choice, computer_choice):
    global user_score, computer_score, ties, current_streak, best_streak, total_rounds, is_animating

    total_rounds += 1
    user_data = CHOICE_DATA[user_choice]
    bot_data = CHOICE_DATA[computer_choice]

    user_symbol_label.config(text=user_data["battle_emoji"], fg=user_data["color"])
    bot_symbol_label.config(text=bot_data["battle_emoji"], fg=bot_data["color"])
    bot_name_badge.config(text=f"{bot_data['symbol']} {bot_data['name']}", fg=bot_data["color"])
    vs_label.config(text="⚔️")

    if user_choice == computer_choice:
        ties += 1
        outcome_symbol = "🤝"
        outcome_text = f"DRAW! Both threw {user_data['name']}!"
        banner_color = COLOR_BLUE
        pulse_winner_animation(result_label, COLOR_BLUE, "#93c5fd", count=4)
        history_entry = f"R{total_rounds}: {user_data['symbol']} vs {bot_data['symbol']} (Draw)"

    elif user_data["beats"] == computer_choice:
        user_score += 1
        current_streak += 1
        if current_streak > best_streak:
            best_streak = current_streak
        outcome_symbol = "🎉"
        outcome_text = f"VICTORY! {user_data['name']} {user_data['verb']} {bot_data['name']}!"
        banner_color = COLOR_EMERALD
        pulse_winner_animation(result_label, COLOR_EMERALD, COLOR_GOLD, count=6)
        history_entry = f"R{total_rounds}: {user_data['symbol']} > {bot_data['symbol']} (Win)"

    else:
        computer_score += 1
        current_streak = 0
        outcome_symbol = "💀"
        outcome_text = f"DEFEAT! {bot_data['name']} {bot_data['verb']} {user_data['name']}!"
        banner_color = COLOR_ROCK
        pulse_winner_animation(result_label, COLOR_ROCK, "#fca5a5", count=6)
        history_entry = f"R{total_rounds}: {user_data['symbol']} < {bot_data['symbol']} (Loss)"

    result_label.config(
        text=f"{outcome_symbol} {outcome_text}",
        fg=banner_color
    )

    score_user_val.config(text=str(user_score))
    score_bot_val.config(text=str(computer_score))
    score_ties_val.config(text=str(ties))
    score_streak_val.config(text=f"{current_streak} (Best: {best_streak})")

    win_rate = (user_score / total_rounds * 100) if total_rounds > 0 else 0
    stats_rate_label.config(text=f"🎯 Win Rate: {win_rate:.1f}%  |  🎮 Total Rounds: {total_rounds}")

    history_log.insert(0, history_entry)
    if len(history_log) > 4:
        history_log.pop()
    history_ticker.config(text="  •  ".join(history_log))

    is_animating = False
    set_buttons_state(tk.NORMAL)

def reset_game():
    global user_score, computer_score, ties, current_streak, total_rounds, history_log, is_animating
    if is_animating:
        return

    user_score = 0
    computer_score = 0
    ties = 0
    current_streak = 0
    total_rounds = 0
    history_log.clear()

    score_user_val.config(text="0")
    score_bot_val.config(text="0")
    score_ties_val.config(text="0")
    score_streak_val.config(text="0 (Best: " + str(best_streak) + ")")
    stats_rate_label.config(text="🎯 Win Rate: 0.0%  |  🎮 Total Rounds: 0")

    user_symbol_label.config(text="❔", fg=TEXT_MUTED)
    bot_symbol_label.config(text="❔", fg=TEXT_MUTED)
    user_name_badge.config(text="Ready to Play", fg=TEXT_MUTED)
    bot_name_badge.config(text="Standing By", fg=TEXT_MUTED)
    vs_label.config(text="⚔️")

    result_label.config(
        text="✨ Choose your move below to enter the arena!",
        fg=TEXT_LIGHT
    )
    history_ticker.config(text="No recent duels yet")

def exit_game():
    if messagebox.askyesno("Exit Battle Arena", "Are you sure you want to quit the duel?"):
        root.destroy()

def attach_hover_effect(widget, default_bg, hover_bg, default_fg, hover_fg):
    def on_enter(e):
        if str(widget["state"]) != str(tk.DISABLED):
            widget.config(bg=hover_bg, fg=hover_fg, cursor="hand2")
    def on_leave(e):
        widget.config(bg=default_bg, fg=default_fg)
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

root = tk.Tk()
root.title("⚔️ Cyber Duel: Rock • Paper • Scissors ⚔️")
root.geometry("540x730")
root.resizable(False, False)
root.configure(bg=BG_DARK)
root.protocol("WM_DELETE_WINDOW", exit_game)

header_frame = tk.Frame(root, bg=BG_DARK)
header_frame.pack(fill="x", pady=(14, 6))

title_label = tk.Label(
    header_frame,
    text="⚡ ROCK • PAPER • SCISSORS ⚡",
    font=("Segoe UI", 18, "bold"),
    bg=BG_DARK,
    fg=COLOR_GOLD
)
title_label.pack()

subtitle_label = tk.Label(
    header_frame,
    text="🎮 ULTIMATE BATTLE ARENA  •  HUMAN vs CYBER AI",
    font=("Segoe UI", 9, "bold"),
    bg=BG_DARK,
    fg=COLOR_PAPER
)
subtitle_label.pack(pady=(2, 0))

score_card = tk.Frame(root, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
score_card.pack(fill="x", padx=18, pady=8)

stats_grid = tk.Frame(score_card, bg=CARD_BG)
stats_grid.pack(fill="x", padx=10, pady=10)

def create_score_tile(parent, col, icon, title, initial_val, color):
    tile = tk.Frame(parent, bg=CARD_BG)
    tile.grid(row=0, column=col, sticky="nsew", padx=6)
    parent.grid_columnconfigure(col, weight=1)

    tk.Label(
        tile,
        text=f"{icon} {title}",
        font=("Segoe UI", 9, "bold"),
        bg=CARD_BG,
        fg=TEXT_MUTED
    ).pack()

    val_label = tk.Label(
        tile,
        text=initial_val,
        font=("Segoe UI", 15, "bold"),
        bg=CARD_BG,
        fg=color
    )
    val_label.pack(pady=(2, 0))
    return val_label

score_user_val = create_score_tile(stats_grid, 0, "👤", "YOU", "0", COLOR_PAPER)
score_bot_val = create_score_tile(stats_grid, 1, "🤖", "CYBERBOT", "0", COLOR_ROCK)
score_ties_val = create_score_tile(stats_grid, 2, "⚖️", "TIES", "0", COLOR_BLUE)
score_streak_val = create_score_tile(stats_grid, 3, "🔥", "STREAK", "0", COLOR_GOLD)

stats_rate_label = tk.Label(
    score_card,
    text="🎯 Win Rate: 0.0%  |  🎮 Total Rounds: 0",
    font=("Segoe UI", 8, "bold"),
    bg=CARD_BG,
    fg=TEXT_MUTED
)
stats_rate_label.pack(pady=(0, 6))

arena_frame = tk.Frame(root, bg=BG_DARK)
arena_frame.pack(fill="x", padx=18, pady=6)
arena_frame.columnconfigure(0, weight=4)
arena_frame.columnconfigure(1, weight=1)
arena_frame.columnconfigure(2, weight=4)

user_card = tk.Frame(arena_frame, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
user_card.grid(row=0, column=0, sticky="nsew", padx=(0, 4), pady=4)

tk.Label(
    user_card,
    text="👤 PLAYER (YOU)",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=COLOR_PAPER
).pack(pady=(10, 4))

user_symbol_label = tk.Label(
    user_card,
    text="❔",
    font=("Segoe UI Emoji", 48),
    bg=CARD_BG,
    fg=TEXT_MUTED
)
user_symbol_label.pack(pady=4)

user_name_badge = tk.Label(
    user_card,
    text="Ready to Play",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_MUTED
)
user_name_badge.pack(pady=(0, 10))

vs_box = tk.Frame(arena_frame, bg=BG_DARK)
vs_box.grid(row=0, column=1, sticky="nsew")

vs_label = tk.Label(
    vs_box,
    text="⚔️",
    font=("Segoe UI Emoji", 26),
    bg=BG_DARK,
    fg=COLOR_GOLD
)
vs_label.pack(expand=True)

bot_card = tk.Frame(arena_frame, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
bot_card.grid(row=0, column=2, sticky="nsew", padx=(4, 0), pady=4)

tk.Label(
    bot_card,
    text="🤖 CYBERBOT (AI)",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=COLOR_ROCK
).pack(pady=(10, 4))

bot_symbol_label = tk.Label(
    bot_card,
    text="❔",
    font=("Segoe UI Emoji", 48),
    bg=CARD_BG,
    fg=TEXT_MUTED
)
bot_symbol_label.pack(pady=4)

bot_name_badge = tk.Label(
    bot_card,
    text="Standing By",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_MUTED
)
bot_name_badge.pack(pady=(0, 10))

result_banner_frame = tk.Frame(root, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
result_banner_frame.pack(fill="x", padx=18, pady=8)

result_label = tk.Label(
    result_banner_frame,
    text="✨ Choose your move below to enter the arena!",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_BG,
    fg=TEXT_LIGHT,
    wraplength=500,
    justify="center"
)
result_label.pack(pady=12, padx=10)

controls_frame = tk.Frame(root, bg=BG_DARK)
controls_frame.pack(fill="x", padx=18, pady=8)
controls_frame.columnconfigure((0, 1, 2), weight=1)

choice_buttons = []

def create_action_button(parent, col, choice_key, shortcut_key):
    info = CHOICE_DATA[choice_key]
    btn_color = info["color"]

    btn = tk.Button(
        parent,
        text=f"{info['symbol']} {info['name']}\n[{shortcut_key}]",
        font=("Segoe UI", 12, "bold"),
        bg=CARD_BG,
        fg=btn_color,
        activebackground=btn_color,
        activeforeground="#ffffff",
        bd=0,
        highlightbackground=btn_color,
        highlightthickness=2,
        relief="flat",
        cursor="hand2",
        pady=8,
        command=lambda: play_game(choice_key)
    )
    btn.grid(row=0, column=col, padx=5, sticky="nsew")

    attach_hover_effect(btn, CARD_BG, btn_color, btn_color, "#ffffff")
    choice_buttons.append(btn)
    return btn

btn_rock = create_action_button(controls_frame, 0, "Rock", "R")
btn_paper = create_action_button(controls_frame, 1, "Paper", "P")
btn_scissors = create_action_button(controls_frame, 2, "Scissors", "S")

root.bind("<r>", lambda e: play_game("Rock"))
root.bind("<R>", lambda e: play_game("Rock"))
root.bind("<p>", lambda e: play_game("Paper"))
root.bind("<P>", lambda e: play_game("Paper"))
root.bind("<s>", lambda e: play_game("Scissors"))
root.bind("<S>", lambda e: play_game("Scissors"))
root.bind("<space>", lambda e: reset_game())

history_frame = tk.Frame(root, bg=BG_DARK)
history_frame.pack(fill="x", padx=18, pady=4)

tk.Label(
    history_frame,
    text="📜 BATTLE LOG:",
    font=("Segoe UI", 8, "bold"),
    bg=BG_DARK,
    fg=TEXT_MUTED
).pack(anchor="w")

history_ticker = tk.Label(
    history_frame,
    text="No recent duels yet",
    font=("Segoe UI", 9),
    bg=BG_DARK,
    fg=TEXT_MUTED
)
history_ticker.pack(anchor="w", pady=(1, 4))

footer_frame = tk.Frame(root, bg=BG_DARK)
footer_frame.pack(fill="x", padx=18, pady=(8, 14))
footer_frame.columnconfigure((0, 1), weight=1)

reset_btn = tk.Button(
    footer_frame,
    text="🔄 Reset Scores  [Space]",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=COLOR_GOLD,
    activebackground=COLOR_GOLD,
    activeforeground=BG_DARK,
    bd=0,
    highlightbackground=COLOR_GOLD,
    highlightthickness=1,
    relief="flat",
    cursor="hand2",
    pady=6,
    command=reset_game
)
reset_btn.grid(row=0, column=0, padx=6, sticky="nsew")
attach_hover_effect(reset_btn, CARD_BG, COLOR_GOLD, COLOR_GOLD, BG_DARK)

exit_btn = tk.Button(
    footer_frame,
    text="🚪 Exit Duel",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_BG,
    fg=COLOR_ROCK,
    activebackground=COLOR_ROCK,
    activeforeground="#ffffff",
    bd=0,
    highlightbackground=COLOR_ROCK,
    highlightthickness=1,
    relief="flat",
    cursor="hand2",
    pady=6,
    command=exit_game
)
exit_btn.grid(row=0, column=1, padx=6, sticky="nsew")
attach_hover_effect(exit_btn, CARD_BG, COLOR_ROCK, COLOR_ROCK, "#ffffff")

if __name__ == "__main__":
    root.mainloop()
