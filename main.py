import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from yars.yars import YARS
from trello.board import Board

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.basicConfig(
    filename=os.path.join(PROJECT_DIR, "run.log"),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize the YARS Reddit miner
miner = YARS()

# Trello Board IDs
WEEKLY_TASKS_BOARD_ID = "646dd9fdff15415ec19515aa"
RESEARCH_BOARD_ID = "662bb890493f5d3919f029ba"

# Initialise Trello Boards
weekly = Board(WEEKLY_TASKS_BOARD_ID)
research_day = Board(RESEARCH_BOARD_ID)

# Store info about Reddit list
reddit_list = research_day.get_list_id_by_name("Reddit")

GITHUB_SUBSTRING = "github.com"
SUBREDDITS = [
    "StableDiffusion",
    "musiconcrete",
    "tinycode",
    "p5js",
    "generative",
    "artandcode",
    "creativecoding",
    "PlotterArt",
    "fractals",
    "puredata",
    "plugdata",
    "comfyuiAudio",
    "proceduralgeneration",
    "musicprogramming",
    "cellular_automata",
]
REDDIT_URL_PREFIX = "https://www.reddit.com"


# Function to scrape subreddit post details and comments and save to Trello
def scrape_subreddit_data(subreddit_name: str, limit:int = 5):
    try:
        subreddit_posts = miner.fetch_subreddit_posts(
            subreddit_name, limit=limit, category="top", time_filter="week"
        )

        # Scrape details and comments for each post
        for i, post in enumerate(subreddit_posts, 1):
            permalink = post["permalink"]
            post_details = miner.scrape_post_details(permalink)
            time.sleep(5)

            print(f"Processing post {i} from {subreddit_name}")

            if post_details:
                post_data = {
                    "title": post.get("title", ""),
                    "author": post.get("author", ""),
                    "created_utc": post.get("created_utc", ""),
                    "num_comments": post.get("num_comments", 0),
                    "score": post.get("score", 0),
                    "permalink": post.get("permalink", ""),
                    "body": post_details.get("body", ""),
                    "comments": post_details.get("comments", []),
                }

                # Append new post data to existing data
                if GITHUB_SUBSTRING in post_data["body"]:

                    link = REDDIT_URL_PREFIX + post_data["permalink"]

                    if research_day.not_already_in_list(reddit_list, link):

                        # Add a link to the trello board
                        code = research_day.add_card_to_list(
                            reddit_list,
                            link,
                            "",
                            "link",
                        )

                        # Record failure
                        if code != 200:
                            print("Trello problem.")
                            logging.error(
                                f"Failed to add to Trello: {REDDIT_URL_PREFIX}{permalink}"
                            )
            else:
                print("Probably too many Reddit requests...")
                logging.error(
                    f"Failed to scrape details for post: {REDDIT_URL_PREFIX}{permalink}"
                )

    except Exception as e:
        print("Couldn't scrape Subreddit.", e)
        logging.error(f"Exception occured when scraping {subreddit_name}")


run_file = Path(os.path.join(PROJECT_DIR, ".last-run"))

if run_file.exists():
    with open(run_file, "r") as f:
        last_run_time = f.readline()

    if last_run_time:
        try:
            last_run_time = datetime.fromisoformat(last_run_time)

            today = datetime.today()
            start_of_week = today - timedelta(
                days=today.weekday(),
                seconds=today.second,
                minutes=today.minute,
                hours=today.hour,
                microseconds=today.microsecond,
            )

            if last_run_time > start_of_week:
                logging.info("Has already been once this week. Exiting.")
                exit()

        except ValueError:
            logging.info("Unable to read last date of run - running anyway.")

for subreddit in SUBREDDITS:
    scrape_subreddit_data(subreddit, limit=50)

with open(run_file, "w") as f:
    f.write(str(datetime.now()))
