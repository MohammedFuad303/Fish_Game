import game_logic
import api_client

puzzle = api_client.solve_puzzle()

if puzzle is None:
    print("Failed to retrieve puzzle from API.")
else:
    print("Open the link and count the number of fish and chests:")
    print(puzzle["image_url"])

    guess_fish = int(input("Enter the number of fish: "))
    guess_chest = int(input("Enter the number of chests: "))

    if game_logic.check_answer(puzzle, guess_fish, guess_chest):
        print("Congratulations! Your answer is correct.")
    else:
        print(f"Sorry, your answer is wrong. The correct answer is {puzzle['fish']} fish and {puzzle['chest']} chests.")