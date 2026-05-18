import datetime
from trello.board import Board

WEEKLY_TASKS_BOARD_ID = "646dd9fdff15415ec19515aa"
RESEARCH_BOARD_ID = "662bb890493f5d3919f029ba"

weekly = Board(WEEKLY_TASKS_BOARD_ID)
research_day = Board(RESEARCH_BOARD_ID)

day = datetime.datetime.now().strftime("%A")

print(weekly.get_list_id_by_name("Monday"))
print(research_day.get_list_id_by_name("/r/StableDiffusion"))