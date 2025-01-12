from utils.domjudge import get_team_data, get_contest_data, get_scoreboard, id_mapping, score_mapping
from utils.google_sheet import get_student_list, get_sheet_contest, write_score, column_mapping
from utils.tkinter_ui import create_mapping_window

def main():
    table_list = ['程式設計總成績']
    team_data = get_team_data()
    contest_data = get_contest_data()

    for table_name in table_list:
        print('Start to process', table_name)

        student_data = get_student_list(table_name)
        student_data = id_mapping(student_data, team_data)

        sheet_contest_list = get_sheet_contest(table_name)
        sheet_contest = column_mapping(sheet_contest_list)

        selected_mapping = create_mapping_window(contest_data, sheet_contest)

        for mapping in selected_mapping:
            student_data.sort(key=lambda x: x['team_id'])
            if not selected_mapping[mapping]:
                continue
            scoreboard_data = []
            for contest_id in selected_mapping[mapping]:
                scoreboard_data.extend(get_scoreboard(contest_id))
            scoreboard_data.sort(key=lambda x: x['team_id'])

            student_data = score_mapping(scoreboard_data, student_data)
            student_data.sort(key=lambda x: x['student_id'])

            write_score(table_name, mapping, student_data)

if __name__ == "__main__":
    main()        