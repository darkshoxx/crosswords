# External imports
import requests
import os
from bs4 import BeautifulSoup

# Directories
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_FILE = os.path.join(HERE, "testfile.txt")


def final_tables_parser(clues: list[dict]):
    new_clues = []
    for table in clues:
        long_text_string = ""
        for value in table.values():
            long_text_string += value
        if len(long_text_string) < 200:
            print(f"table {table} contains less than 200 characters, dropping")
        elif len(set(long_text_string)) < 15:
            print(
                f"table {table} contains less than 15 unique symbols, dropping"
                )
        else:
            new_clues.append(table)
    return new_clues


def parse_html_for_tables(response):
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    if tables:
        clues = [extract_clues_from_table(table) for table in tables]

        return clues
    else:
        raise Exception("Tables not found on page")


def get_puzzle_clues(puzzle_id):
    # Construct the URL for the given puzzle ID
    url = f"https://timesforthetimes.co.uk/times-{puzzle_id}"

    # send GET request
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:

        clues = parse_html_for_tables(response)
        clues = final_tables_parser(clues)

        return clues
    else:
        raise Exception(
            f"failed to fetch page. Status code {response.status_code}"
            )


def extract_clues_from_table(table):
    clues = {}
    rows = table.find_all('tr')[1:]
    for row in rows:
        cells = row.find_all('td')
        number = cells[0].text.strip()
        clue = cells[1].text.strip()
        if number:
            clues[number] = clue
    return clues


def save_clues_to_file(puzz_id, clues, path=TEST_FILE, link="", date=""):
    output_file_path = path

    if isinstance(clues, list):
        with open(output_file_path, 'w', encoding="utf-8") as file:
            file.write(
                f"Dweebovision Cryptic puzzle {puzz_id} from {date}\n{link}\n"
            )
            for idx, clue_set in enumerate(clues, start=1):
                file.write(f"Clues for Table {idx}:\n")
                if idx == 1:
                    file.write("(Probably) Across\n")
                elif idx == 2:
                    file.write("(Probably) Down\n")
                else:
                    file.write("more than two tables?\n")
                for number, clue in clue_set.items():
                    file.write(f"{number}. {clue}\n")
                file.write("\n")
        print(f"Clues saved to {output_file_path}")
    else:
        raise Exception(f"Clues {clues} not returned in valid format.")


# Main script
if __name__ == "__main__":
    # Example usage
    puzzle_id = 28513  # replace with desired ID
    clues = get_puzzle_clues(puzzle_id)
    save_clues_to_file(puzzle_id, clues)
