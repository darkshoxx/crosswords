import os
from pytube import YouTube
from PIL import Image, ImageStat
import pytesseract
import json
import re
import cv2

HERE = os.path.abspath(os.path.dirname(__file__))
OUTPUT = os.path.join(HERE, "videos")
DICT_FILE = os.path.join(HERE, "puzzle_videos_dict.json")
VIDEO_FILE = os.path.join(OUTPUT, "temp_video.mp4")
PUZZLES_DIR = os.path.join(HERE, "puzzles")
INTERVAL = 0.5
RANGE = (130, 230)
MAX_FRAMES = 10
pytesseract.pytesseract.tesseract_cmd = (
    r"E:\Program Files\Tesseract-OCR\tesseract.exe"
)
# Create a directory to store frames
FRAMES_DIR = os.path.join(HERE, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)


# Function to calculate average brightness of an image
def calculate_average_brightness(image):
    stat = ImageStat.Stat(image)
    r, g, b = stat.mean
    return (r + g + b) / 3


# Function to check if the average brightness is within a specified range
def is_brightness_within_range(image, target_range):
    brightness = calculate_average_brightness(image)
    print(brightness)
    return target_range[0] <= brightness <= target_range[1]


def find_leftmost_pixel(frame_image, height):
    width, _ = frame_image.size
    pixel_data = frame_image.load()

    for x in range(width):
        pixel_color = pixel_data[x, height]
        pixel_brightness = sum(pixel_color)/3
        black_block_passed = False

        # Ignore the first set of black pixels (if they exist)
        if pixel_brightness < 10 and not black_block_passed:
            continue

        black_block_passed = True

        # Ignore the block of white pixels
        if pixel_brightness > 250:
            continue

        # Return the x-coordinate of the first non-white pixel
        return x

    # Return -1 if no suitable pixel is found
    return -1


# Function to extract frames from the video at a specific interval
def extract_frames(video_path, max_frames=MAX_FRAMES, interval=INTERVAL):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return []

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frames = []
    for i in range(0, total_frames, int(fps * interval)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = cap.read()
        frames.append(frame)

        if len(frames) >= max_frames:
            break

    cap.release()
    return frames


# Function to download the video
def download_video(video_url):
    youtube = YouTube(video_url)
    video_stream = youtube.streams.filter(file_extension="mp4").first()
    print("commencing download")
    video_path = video_stream.download(
        output_path=OUTPUT,
        filename='temp_video.mp4'
        )
    print("download complete")
    return video_path


# Function to save frames to a directory
def save_frames(frames, directory):
    for i, frame in enumerate(frames):
        frame_path = os.path.join(directory, f"frame_{i}.png")
        cv2.imwrite(frame_path, frame)


# Function to perform OCR on an image with cropping
def perform_ocr(frame_image, leftmost_pixel):
    # Crop the image to the specified coordinates
    crop_coordinates = (leftmost_pixel, 0, 230, 20)
    cropped_image = frame_image.crop(crop_coordinates)

    # Perform OCR on the cropped image
    ocr_result = pytesseract.image_to_string(cropped_image, config='--psm 10')
    puzzle_number = re.search(r'\b\d+\b', ocr_result)
    return puzzle_number.group() if puzzle_number else None


# Function to process video for a given puzzle number
def process_video(video_path):
    print("Checking frames for brightness...")

    # Extract frames from the video
    video_frames = extract_frames(video_path)

    if not video_frames:
        print("No frames found. Exiting process_video.")
        return None

    # Check frames for brightness
    for i, frame in enumerate(video_frames):
        frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if is_brightness_within_range(frame_image, RANGE):
            # Save frames for debugging purposes
            frame_path = os.path.join(FRAMES_DIR, f"frame_{i}.png")
            frame_image.save(frame_path)

            # Use OCR to find the puzzle number in the frame
            leftmost_pixel = find_leftmost_pixel(frame_image, 100)
            puzzle_number = perform_ocr(frame_image, leftmost_pixel)

            if puzzle_number:

                puzz_frame = extract_and_scale_puzzle_grid(
                    frame_image,
                    leftmost_pixel
                    )
                grid_path = os.path.join(
                    PUZZLES_DIR, f"{puzzle_number}_grid.png"
                    )
                os.makedirs(PUZZLES_DIR, exist_ok=True)
                puzz_frame.save(grid_path)
                print(f"Puzzle number for video: {puzzle_number}")
                return puzzle_number

    print("No suitable frames found to extract puzzle number.")
    return None


# Function to extract puzzle grid from a frame
def extract_and_scale_puzzle_grid(frame, leftmost_pixel, scale_factor=4):
    # Crop the frame to the specified grid coordinates
    grid_coordinates = (leftmost_pixel, 19, 336, 237)
    left, upper, right, lower = grid_coordinates
    grid_image = frame.crop((left, upper, right, lower))

    # Resize the grid image
    scaled_grid_image = grid_image.resize(
        (
            grid_image.width * scale_factor, grid_image.height * scale_factor
        ),
        Image.NEAREST
    )

    return scaled_grid_image


# Main script
if __name__ == "__main__":

    # Step 5-8: Process a specific puzzle (replace 'desired_puzzle_date'
    # with the actual puzzle number)
    puzzle_date = '2023-10-28'  # Replace with the actual puzzle number
    # Load data from the JSON file
    json_filename = DICT_FILE
    with open(json_filename, 'r') as json_file:
        filtered_videos = json.load(json_file)

    # Example: Print the puzzle numbers and corresponding video URLs
    if puzzle_date in filtered_videos:

        download_video(filtered_videos[puzzle_date])
        puzzle_number = process_video(VIDEO_FILE)

        # frame_path = os.path.join(FRAMES_DIR, "frame_7.png")
        # frame_image = Image.open(frame_path)
        # puzz_num = perform_ocr(frame_image)
        # puzz_frame = extract_and_scale_puzzle_grid(frame_image)
        # grid_path = os.path.join(FRAMES_DIR, f"grid_7.png")
        # puzz_frame.save(grid_path)

    else:
        print(f"Video for puzzle {puzzle_date} not found.")
