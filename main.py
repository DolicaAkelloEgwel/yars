import json
import os
import sys
import time

from src.yars.utils import display_results, download_image
from src.yars.yars import YARS
from trello.board import Board

# Initialize the YARS Reddit miner
miner = YARS()
filename = "failure-log.json"

WEEKLY_TASKS_BOARD_ID = "646dd9fdff15415ec19515aa"
RESEARCH_BOARD_ID = "662bb890493f5d3919f029ba"

weekly = Board(WEEKLY_TASKS_BOARD_ID)
research_day = Board(RESEARCH_BOARD_ID)

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
]


# Function to scrape subreddit post details and comments and save to JSON
def scrape_subreddit_data(subreddit_name, limit=5, filename=filename):
    try:
        subreddit_posts = miner.fetch_subreddit_posts(
            subreddit_name, limit=limit, category="top", time_filter="week"
        )

        # Load existing data from the JSON file, if available
        try:
            with open(filename, "r") as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # Scrape details and comments for each post
        for i, post in enumerate(subreddit_posts, 1):
            permalink = post["permalink"]
            post_details = miner.scrape_post_details(permalink)
            print(f"Processing post {i}")

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
                    existing_data.append(post_data)

                    link = "https://www.reddit.com" + post_data["permalink"]

                    if research_day.not_already_in_list(reddit_list, link):

                        # Add a link to the trello board
                        code = research_day.add_card_to_list(
                            reddit_list,
                            link,
                            "",
                            "link",
                        )
                        # Save the data incrementally to the JSON file
                        if code != 200:
                            save_to_json(existing_data, filename)
            else:
                print(f"Failed to scrape details for post: {post['title']}")

    except Exception as e:
        print(f"Error occurred while scraping subreddit: {e}")
    time.sleep(5)


# Function to save post data to a JSON file
def save_to_json(data, filename=filename):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")


for subreddit in SUBREDDITS:
    scrape_subreddit_data(subreddit, limit=50)
