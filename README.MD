# Crpytics Scraper
## Intro

This is a tool that generates a list of cryptics crosswords from The Times magazine. It does so by analyzing videos from [David Webb's Youtube channel](https://www.youtube.com/@dweebovision) to get the layout and puzzle number, and calling [TimesForTheTimes](https://timesforthetimes.co.uk) to get the clues.

## Setup 

Clone the repo, install python 3.8+, install the requirements, get a youtube API key, and obtain dweebovision's channel ID.  
Create a file "secrety_secrets.py" and fill it with   
```python
API_KEY = "<your API key here>"
CHANNEL_ID = "<desired Youtube Channel ID here>"
TESSERACT_PATH = "<your tesseract.exe path \ file here>"
```
where you replace the desired values in the tags.


## Execution

Run main.py, this will generate a table of dates and links in a file `puzzle_videos_dict.json`. Pick a date from there and put it in `puzzle_date` as a string in that format (replace None).  

Run the script again, it will download the video, attempt to find the puzzle number and layout from a couple of frames from the video.
It will then look up the puzzle number on timesforthetimes.co.uk, scrape the clues and put it in a text file.

In total it will generate three folders: `/frames/` , `/videos/` and `/puzzles/`. While the former two will be overwritten every time the script is run, every new puzzle will be added as a grid and a textfile of clues in the latter.

## Rights and Legalese

This repo uses the YouTube API and as such is subject to the [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service) which in particular require me to inclued them in this package. By using this repo therefore you accept the terms and conditions thereof.  
The usage of the YouTube API to download videos from other channels is *in general prohibited* with some exceptions. One of those being downloading for **personal, non-commercial use** which this is. Keep that in mind if you inted to fork this repo.  
This repo is published under an MIT license.  
I have written permission from David Webb to use the content from his website for this project.  
All data generated from this repo is publically freely available, it is automation of collection of public data.

## ToDo
- type annotations
- refactoring
- testing
- docstrings
- comments
- replace prints with logger
- error handling
- github actions
- improve readme file
- lint
- pre-commit
- tox
- formatting or redrawing grid image file
