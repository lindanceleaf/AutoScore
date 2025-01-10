import requests
from typing import List
from models.types import Team, Contest, Scoreboard, Student
from config import JUDGE_URL, AUTH

def get_team_data() -> List[Team]:
    """
    從 DOMjudge API 獲取所有隊伍數據。
    :return: 包含隊伍名稱和隊伍 ID 的列表
    """
    url = f"{JUDGE_URL}/api/teams"
    response = requests.get(url, auth=AUTH)
    response.raise_for_status()  # 確保請求成功
    teams = response.json()
    return [{'team_name': team['name'], 'team_id': team['id']} for team in teams]

def get_contest_data() -> List[Contest]:
    """
    從 DOMjudge API 獲取所有比賽數據。
    :return: 包含比賽名稱和比賽 ID 的列表
    """
    url = f"{JUDGE_URL}/api/contests"
    response = requests.get(url, auth=AUTH)
    response.raise_for_status()
    contests = response.json()
    return [{'contest_id': contest['id'], 'contest_name': contest['name']} for contest in contests]

def get_scoreboard(contest_id: str) -> List[Scoreboard]:
    """
    從 DOMjudge API 獲取指定比賽的積分榜。
    :param contest_id: 比賽 ID
    :return: 包含隊伍 ID 和分數的列表
    """
    url = f"{JUDGE_URL}/api/v4/contests/{contest_id}/scoreboard"
    response = requests.get(url, auth=AUTH)
    response.raise_for_status()
    scoreboard = response.json()
    return [
        {'team_id': row['team_id'], 'score': row['score']['num_solved']}
        for row in scoreboard['rows']
    ]

def id_mapping(student_data: List[Student], team_data: List[Team]) -> List[Student]:
    """
    將學生數據與隊伍數據匹配，更新學生的 team_id。
    :param student_data: 學生數據列表
    :param team_data: 隊伍數據列表
    :return: 更新後的學生數據列表
    """
    for student in student_data:
        for team in team_data:
            if student["name"] in team["team_name"]:
                student["team_id"] = team["team_id"]
                break
        else:
            student["team_id"] = None  # 如果找不到匹配，設為 None
    return student_data

def score_mapping(scoreboard_data: List[Scoreboard], student_data: List[Student]) -> List[Student]:
    """
    將積分榜的分數映射到學生數據中，更新學生的 score。
    :param scoreboard_data: 包含隊伍 ID 和分數的列表
    :param student_data: 學生數據列表
    :return: 更新後的學生數據列表
    """
    for student in student_data:
        student["score"] = None  # 預設為 None
        for score in scoreboard_data:
            if student["team_id"] == score["team_id"]:
                student["score"] = score["score"]
                break
    return student_data