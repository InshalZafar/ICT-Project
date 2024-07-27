import tkinter as tk
from tkinter import messagebox
import random

def play_matchstick_game():
    def update_status():
        """
        Update the status and history labels with the current state of the game.
        """
        status_label.config(text=f"Current matchsticks: {game_data['total_matchsticks']}")
        history_label.config(text=f"Player 1's Picks: {', '.join(map(str, game_data['player1_picks']))}\n"
                                  f"{game_data['player2']}'s Picks: {', '.join(map(str, game_data['player2_picks']))}")
        player_turn_label.config(text=f"Player {game_data['current_player']}'s Turn")
        update_player_entry_label()

    def update_player_entry_label():
        """
        Update the player entry label based on the remaining matchsticks.
        """
        remaining = game_data['total_matchsticks']
        if remaining <= 4:
            player_entry_label.config(text=f"Your turn: How many matchsticks do you pick? (1-{remaining - 1}):")
        else:
            player_entry_label.config(text="Your turn: How many matchsticks do you pick? (1-4):")

    def player_pick(event=None):
        """
        Handle the player's pick and update the game state accordingly.
        """
        try:
            player_choice = int(player_entry.get())
            remaining = game_data['total_matchsticks']
            # Validate the player's choice
            if player_choice < 1 or player_choice >= remaining or player_choice > 4:
                messagebox.showerror("Invalid Input", f"You must pick 1-{min(4, remaining - 1)} matchsticks.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 4.")
            return

        # Update the game state based on the player's choice
        game_data['total_matchsticks'] -= player_choice
        if game_data['current_player'] == 1:
            game_data['player1_picks'].append(player_choice)
            game_data['current_player'] = 2
        else:
            game_data['player2_picks'].append(player_choice)
            game_data['current_player'] = 1
        update_status()
        player_entry.delete(0, tk.END)
        
        if game_data['total_matchsticks'] == 1:
            game_over(f"Player {3 - game_data['current_player']} wins!")
            return
        
        if game_data['mode'] == "Single Player" and game_data['current_player'] == 2:
            computer_pick()

    def computer_pick():
        """
        Handle the computer's pick and update the game state accordingly.
        """
        remaining = game_data['total_matchsticks']
        if game_data['level'] == "Hard":
            # Computer always wins strategy for hard level
            computer_choice = (remaining - 1) % 5 or random.randint(1, min(4, remaining - 1))
        else:
            computer_choice = random.randint(1, min(4, remaining - 1))
        
        game_data['total_matchsticks'] -= computer_choice
        game_data['player2_picks'].append(computer_choice)
        game_data['current_player'] = 1
        update_status()

        if game_data['total_matchsticks'] <= 1:
            game_over("Computer wins!", sad=True)
        else:
            computer_pick_label.config(text=f"Computer picks {computer_choice} matchstick(s).")

    def game_over(message, sad=False):
        """
        Handle the end of the game and prompt the player to play again or exit.
        """
        if sad:
            message += " 😔"
        game_data['score'][game_data['current_player']] += 1
        if messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?"):
            reset_game()
        else:
            messagebox.showinfo("Goodbye", f"Thank you for playing! Final Score: Player 1 - {game_data['score'][1]}, Player 2/Computer - {game_data['score'][2]}")
            root.quit()

    def reset_game():
        """
        Reset the game state to start a new game.
        """
        game_data['total_matchsticks'] = game_data['initial_matchsticks']
        game_data['player1_picks'].clear()
        game_data['player2_picks'].clear()
        game_data['current_player'] = 1
        update_status()
        computer_pick_label.config(text="")

    def set_mode(mode):
        """
        Set the game mode to Single Player or Multiplayer and start the game.
        """
        game_data['mode'] = mode
        if mode == "Single Player":
            game_data['player2'] = "Computer"
        else:
            game_data['player2'] = "Player 2"
        level_menu.pack()

    def set_level(level):
        """
        Set the game difficulty level and reset the game.
        """
        game_data['level'] = level
        if level == "Easy":
            game_data['initial_matchsticks'] = 21
        elif level == "Medium":
            game_data['initial_matchsticks'] = 31
        elif level == "Hard":
            game_data['initial_matchsticks'] = 41
        reset_game()
        start_game()

    def start_game():
        """
        Transition from the main menu to the game frame.
        """
        main_menu.pack_forget()
        level_menu.pack_forget()
        game_frame.pack()

    # Initial game data
    game_data = {
        'total_matchsticks': 21,
        'initial_matchsticks': 21,
        'player1_picks': [],
        'player2_picks': [],
        'current_player': 1,
        'mode': "Single Player",
        'level': "Easy",
        'player2': "Computer",
        'score': {1: 0, 2: 0}
    }

    # Initialize the main window
    root = tk.Tk()
    root.title("Matchstick Game")

    # Set the background color
    root.configure(bg="#282c34")

    # Main Menu
    main_menu = tk.Frame(root, bg="#282c34")
    main_menu.pack(pady=20)

    welcome_label = tk.Label(main_menu, text="Welcome to the Matchstick Game!", font=("Helvetica", 16), fg="white", bg="#282c34")
    welcome_label.pack(pady=10)

    mode_label = tk.Label(main_menu, text="Select Game Mode:", font=("Helvetica", 14), fg="white", bg="#282c34")
    mode_label.pack(pady=5)

    single_player_button = tk.Button(main_menu, text="Single Player", font=("Helvetica", 12), command=lambda: set_mode("Single Player"), bg="#61afef", fg="white")
    single_player_button.pack(pady=5)

    multiplayer_button = tk.Button(main_menu, text="Multiplayer", font=("Helvetica", 12), command=lambda: set_mode("Multiplayer"), bg="#61afef", fg="white")
    multiplayer_button.pack(pady=5)

    # Level Menu
    level_menu = tk.Frame(root, bg="#282c34")
    
    level_label = tk.Label(level_menu, text="Select Level:", font=("Helvetica", 14), fg="white", bg="#282c34")
    level_label.pack(pady=5)

    easy_button = tk.Button(level_menu, text="Easy 🌱 (21 matchsticks)", font=("Helvetica", 12), command=lambda: set_level("Easy"), bg="#61afef", fg="white")
    easy_button.pack(pady=5)

    medium_button = tk.Button(level_menu, text="Medium 🌳 (31 matchsticks)", font=("Helvetica", 12), command=lambda: set_level("Medium"), bg="#61afef", fg="white")
    medium_button.pack(pady=5)

    hard_button = tk.Button(level_menu, text="Hard 🌲 (41 matchsticks)", font=("Helvetica", 12), command=lambda: set_level("Hard"), bg="#61afef", fg="white")
    hard_button.pack(pady=5)

    # Game Frame
    game_frame = tk.Frame(root, bg="#282c34")

    status_label = tk.Label(game_frame, text=f"Current matchsticks: {game_data['total_matchsticks']}", font=("Helvetica", 14), fg="white", bg="#282c34")
    status_label.pack(pady=10)

    history_label = tk.Label(game_frame, text="Player 1's Picks: \nPlayer 2/Computer's Picks: ", font=("Helvetica", 12), fg="white", bg="#282c34", justify=tk.LEFT)
    history_label.pack(pady=10)

    player_turn_label = tk.Label(game_frame, text="Player 1's Turn", font=("Helvetica", 12), fg="white", bg="#282c34")
    player_turn_label.pack(pady=5)

    player_entry_label = tk.Label(game_frame, text="Your turn: How many matchsticks do you pick? (1-4):", font=("Helvetica", 12), fg="white", bg="#282c34")
    player_entry_label.pack(pady=5)

    player_entry = tk.Entry(game_frame, font=("Helvetica", 12))
    player_entry.pack(pady=5)
    player_entry.bind("<Return>", player_pick)  # Bind Enter key to player_pick function

    pick_button = tk.Button(game_frame, text="Pick", font=("Helvetica", 12), command=player_pick, bg="#61afef", fg="white")
    pick_button.pack(pady=10)

    computer_pick_label = tk.Label(game_frame, text="", font=("Helvetica", 12), fg="white", bg="#282c34")
    computer_pick_label.pack(pady=10)

    root.mainloop()

play_matchstick_game()
