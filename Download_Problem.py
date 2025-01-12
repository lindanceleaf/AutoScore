from utils.tkinter_ui import create_selector_window
from utils.domjudge import get_contest_data, get_contest_problems
import requests
from config import JUDGE_URL, AUTH
import os

contest_data = get_contest_data()
contest_id = create_selector_window(contest_data)
os.makedirs("problems", exist_ok=True)
for contest in contest_id:
    os.makedirs(f"problems/{contest['contest_name']}", exist_ok=True)
    problem_id = get_contest_problems(contest['contest_id'])
    for problem in problem_id:
        url = f"{JUDGE_URL}/api/contests/{contest['contest_id']}/problems/{problem['problem_id']}/statement"
        response = requests.get(url, auth=AUTH)
        response.raise_for_status()
        with open(f"problems/{contest['contest_name']}/{problem['problem_name']}.pdf", "wb") as f:
            f.write(response.content)
        print(f"Downloaded {problem}.pdf")
    