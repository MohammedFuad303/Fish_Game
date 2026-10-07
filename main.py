import game_logic
import api_client



def ask_question(question):
    
    while True:
        text = input(question)
        try:
            number = int(text)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        if number < 0:
            print("Invalid number. Please enter a non-negative number.")
            continue
        return number


def ask_rounds():
    while True:
        rounds = ask_question("Enter the number of rounds you want to play: ")
        if rounds == 0:
            print("The number of rounds must be at least 1.")
            continue
        return rounds

   
def play_round(number_of_round,rounds):


    puzzle = api_client.solve_puzzle()
    print(f"\n--- Round {number_of_round} of {rounds} ---")

    if puzzle is None:
        print("Failed to retrieve puzzle from API.")
        return False

    print("Open the link and count the number of fish and chests:")
    print(puzzle["image_url"])

    guess_fish = ask_question("Enter the number of fish: ")
    guess_chest = ask_question("Enter the number of chests: ")

    if game_logic.check_answer(puzzle, guess_fish, guess_chest):
        print("Congratulations! Your answer is correct.")
        return True
    else:
        print(f"Sorry, your answer is wrong. The correct answer is {puzzle['fish']} fish and {puzzle['chest']} chests.")
        return False


def main():
    score = 0
    rounds = ask_rounds()
    for number_of_round in range(1, rounds + 1):
        if play_round(number_of_round, rounds):
            score += 1
    print(f"\nGame Over! Your final score is {score} out of {rounds}.")


if __name__ == "__main__":
    main()