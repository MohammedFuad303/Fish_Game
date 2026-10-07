import requests

url = "http://marcconrad.com/uob/fish/api.php"


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
    # Optional: Download the puzzle image to disk
    #img_response = requests.get(image_url)
    #if img_response.status_code == 200:
    #    with open("puzzle.png", "wb") as f:
    #        f.write(img_response.content)
    #    print("Downloaded puzzle.png successfully!")