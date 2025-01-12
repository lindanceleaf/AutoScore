from typing import TypedDict, Optional, List

class Team(TypedDict):
    team_name: str
    team_id: str

class Student(TypedDict):
    name: str
    team_id: Optional[str]
    student_id: Optional[str]
    score: Optional[int]

class Contest(TypedDict):
    contest_id: str
    contest_name: str

class Scoreboard(TypedDict):
    team_id: str
    score: int

class Sheet_Contest(TypedDict):
    grid_name: str
    col: str

class Selected_Mapping(TypedDict):
    col: List[str]

class Problem(TypedDict):
    problem_id: str
    problem_name: str