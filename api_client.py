import requests

url = "http://marcconrad.com/uob/fish/api.php"

# A function to fetch the puzzle data from the API and 
# returns a dictionary containing the image URL, fish count, and chest count
def solve_puzzle():

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return{
            "image_url": data.get("question"),
            "fish": data.get("fish"),
            "chest": data.get("chest")
        }
    else:
        return None


if __name__ == "__main__":        
    puzzle = solve_puzzle()
    print(puzzle)

    if puzzle is not None:
        print("Fish:", puzzle["fish"])