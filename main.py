# External imports
import os
import json
# Local imports
from dweebo_scraper import get_channel_videos, CHANNEL_ID, filter_videos
from puzzle_getter import (
    download_video, process_video, VIDEO_FILE, PUZZLES_DIR
)
from cwparse import get_puzzle_clues, save_clues_to_file


# Get Videos from Channel and store them in file:
channel_id = CHANNEL_ID  # Replace with the actual channel ID
videos = get_channel_videos(channel_id)
filtered_videos = filter_videos(videos)

# Save the dictionary with puzzle dates and video URLs as JSON
json_filename = 'puzzle_videos_dict.json'
with open(json_filename, 'w') as json_file:
    json.dump(filtered_videos, json_file, indent=2)

# Select a date
puzzle_date = None  # "2024-01-13"

if puzzle_date in filtered_videos:
    # Download video, process frames to get puzzle number and grid
    download_video(filtered_videos[puzzle_date])
    puzzle_number = process_video(VIDEO_FILE)
    print(puzzle_number)
    clues = get_puzzle_clues(puzzle_number)
    clue_file = os.path.join(PUZZLES_DIR, f"{puzzle_number}_clues.txt")
    save_clues_to_file(
        puzzle_number,
        clues,
        clue_file,
        filtered_videos[puzzle_date],
        puzzle_date
    )
