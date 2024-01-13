import requests
from bs4 import BeautifulSoup

def get_puzzle_solutions(puzzle_id):
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
            solutions = [extract_solutions_from_table(table) for table in tables]

            return solutions
        else:
            return "Tables not found on page"

    else:
        return f"failed to fetch page. Status code {response.status_code}"

def extract_solutions_from_table(table):
    solutions = {}
    rows = table.find_all('tr')[1:] # skip header for now
    for row in rows:
        cells = row.find_all('td')
        number = cells[0].text.strip()
        clue = cells[1].text.strip()
        if number:
            solutions[number] = clue
    return solutions

# Example usage
puzzle_id = 28779 # replace with desired ID
solutions = get_puzzle_solutions(puzzle_id)

if isinstance(solutions, list):
    for idx, solution_set in enumerate(solutions, start=1):
        print(f"soulutions for puzzle {puzzle_id}, Table {idx}:")
        for number, clue in solution_set.items():
            print(f"{number}. {clue}")
        print("\n")
else:
    print(solutions)