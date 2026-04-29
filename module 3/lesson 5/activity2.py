import random

while True:
    user_action = input("Enter a choice(rock,paper,scissors): ")
    possible_actions = ["rock", "paper","scissors"]
    computer_actions = random.choice(possible_actions)
    print(f"\nYou chose {user_action}, computer chose {computer_actions}.\n")

    if user_action ==computer_actions:
        print(f"both players selected {user_action}, Its a tie!")
    elif user_action == "rock":
        if computer_actions == "scissors":
            print("rock smashes scissors! You win!")
        else:
            print("Paper covers rock! You lose")
    elif user_action == "paper":
        if computer_actions == "rock":
            print("paper covers rock! You win!")
        else:
            print("scissors cut paper! You lose")
    elif user_action == "scissors":
        if computer_actions == "paper":
            print("scissors cut paper! You win!")
        else:
            print("rock smashes scissors! you lose")
    play_again = input("Play again? (y/n): ")
    if play_again == "n":
        break