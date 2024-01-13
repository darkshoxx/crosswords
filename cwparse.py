import requests
from bs4 import BeautifulSoup


def get_puzzle_clues(puzzle_id):
    # Construct the URL for the given puzzle ID
    url = f"https://timesforthetimes.co.uk/times-{puzzle_id}"

    # send GET request
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tables on the page
        tables = soup.find_all('table')

        if tables:
            clues = [extract_clues_from_table(table) for table in tables]

            return clues
        else:
            return "Tables not found on page"

    else:
        return f"failed to fetch page. Status code {response.status_code}"


def extract_clues_from_table(table):
    clues = {}
    rows = table.find_all('tr')[1:]  # skip header for now
    for row in rows:
        cells = row.find_all('td')
        number = cells[0].text.strip()
        clue = cells[1].text.strip()
        if number:
            clues[number] = clue
    return clues


def save_clues_to_file(puzz_id, clues, path, link, date):
    output_file_path = path

    if isinstance(clues, list):
        with open(output_file_path, 'w', encoding="utf-8") as file:
            file.write(
                f"Dweebovision Cryptic puzzle {puzz_id} from {date}\n{link}\n"
            )
            for idx, clue_set in enumerate(clues, start=1):
                file.write(f"Clues for Table {idx}:\n")
                for number, clue in clue_set.items():
                    file.write(f"{number}. {clue}\n")
                file.write("\n")
        print(f"Clues saved to {output_file_path}")
    else:
        print(clues)


# Main script
if __name__ == "__main__":
    # Example usage
    puzzle_id = 28513  # replace with desired ID
    clues = get_puzzle_clues(puzzle_id)
