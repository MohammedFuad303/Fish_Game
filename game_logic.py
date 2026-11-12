
# A function to match the user's guess with the correct answer 
def check_answer(puzzle, guess_fish, guess_chest):
    if guess_fish == puzzle["fish"] and guess_chest == puzzle["chest"]:
        return True
    else:
        return False

# Test cases to verify the function works correctly
if __name__ == "__main__":
    test_puzzle = {"fish": 7, "chest": 3}

    print(check_answer(test_puzzle, 7, 3))  
    print(check_answer(test_puzzle, 5, 3))
    print(check_answer(test_puzzle, 7, 2))