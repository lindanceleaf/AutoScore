from typing import List
from models.types import Student, Sheet_Contest
from config import service, GOOGLE_SHEET_ID

def get_student_list(table_name: str) -> List[Student]:
    """
    從 Google Sheets 獲取學生列表。
    :param table_name: Google Sheet 的表格名稱
    :return: 包含學生資料的列表，符合 Student 結構
    """
    read_range = f'{table_name}!A3:B'
    result = service.spreadsheets().values().get(
        spreadsheetId=GOOGLE_SHEET_ID, range=read_range).execute()
    return [
        {
            "name": row[0].replace('\u3000', ''),  # 清除多餘空格
            "student_id": row[1],
            "team_id": None,  # 預設為 None，等待後續匹配
            "score": None     # 預設為 None，等待後續更新
        }
        for row in result.get('values', []) if len(row) >= 2
    ]

def get_sheet_contest(table_name: str) -> List[str]:
    """
    從 Google Sheets 獲取比賽名稱列表。
    :param table_name: Google Sheet 的表格名稱
    :return: 比賽名稱的列表
    """
    read_range = 'D2:2'
    result = service.spreadsheets().values().get(
        spreadsheetId=GOOGLE_SHEET_ID, range=f'{table_name}!{read_range}').execute()
    return [
        contest for contest in result.get('values', [])[0] if contest
    ]

def next_col(col: str) -> str:
    """
    計算下一個 Excel 樣式的欄位名稱。
    :param col: 當前欄位名稱（如 'D', 'Z', 'AA'）
    :return: 下一個欄位名稱（如 'E', 'AA', 'AB'）
    """
    result = list(col)
    for i in range(len(result) - 1, -1, -1):
        if result[i] == 'Z':
            result[i] = 'A'
            if i == 0:
                result.insert(0, 'A')
        else:
            result[i] = chr(ord(result[i]) + 1)
            break
    return ''.join(result)

def column_mapping(sheet_contest_list: List[str]) -> List[Sheet_Contest]:
    """
    將比賽名稱映射到對應的 Google Sheets 欄位。
    :param sheet_contest_list: 比賽名稱列表（如 ['Contest 1', 'Contest 2']）
    :return: 包含比賽名稱與欄位名稱對應關係的列表
    """
    sheet_contest = []
    current_col = 'D'  # 假設從 D 欄開始
    for contest in sheet_contest_list:
        sheet_contest.append({
            'grid_name': contest,
            'col': current_col + '2'  # 如 'D2', 'E2'
        })
        current_col = next_col(current_col)
    return sheet_contest

def write_score(table_name: str, col: str, student_data: List[Student]) -> None:
    """
    將學生的分數寫入 Google Sheets。
    :param table_name: Google Sheet 的表格名稱
    :param col: 欄位名稱（如 'E'）
    :param student_data: 包含學生分數的列表
    """
    col_name = ''.join(filter(str.isalpha, col))  # 擷取欄位名稱中的字母部分
    score_list = [
        [student['score']] if student.get('score') is not None else ['']
        for student in student_data
    ]
    write_range = f'{table_name}!{col_name}3:{col_name}{len(student_data) + 2}'
    body = {'values': score_list}
    service.spreadsheets().values().update(
        spreadsheetId=GOOGLE_SHEET_ID, range=write_range, valueInputOption='RAW', body=body
    ).execute()
    print(f"Scores written to column {col_name}")
