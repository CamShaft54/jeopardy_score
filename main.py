"""Run this file to start the program"""
import PySimpleGUI as Sg
import sys
import json


def start_setup_window():
    setup_window_layout = [[Sg.Text('Enter Number of Players'), Sg.InputText()],
                           [Sg.Button('Ok', bind_return_key=True), Sg.Button('Cancel')]]
    setup_window = Sg.Window('Jeopardy Scorer Setup', setup_window_layout)
    while True:
        event, values = setup_window.read()
        if event == 'Cancel' or event is None:  # if user closes window or clicks cancel
            setup_window.close()
            return "Cancelled"
        elif values[0].isnumeric() and int(values[0]) > 0:
            setup_window.close()
            return int(values[0])
        elif values[0] == "0":
            Sg.popup_error("There must be at least one player!")


def start_enter_names_window():
    enter_names_window_layout = [[Sg.Text('Enter the names of each player in the fields below')]]
    for i in range(player_count):
        enter_names_window_layout.append([Sg.Text("Player {}".format(i + 1)), Sg.InputText()])
    enter_names_window_layout.append([Sg.Button("Confirm", bind_return_key=True), Sg.Button("Cancel")])
    enter_names_window = Sg.Window('Enter Names of Players', enter_names_window_layout)
    while True:
        event, values = enter_names_window.read()
        if event == 'Confirm':
            enter_names_window.close()
            return list(values.values())
        if event == 'Cancel' or event is None:
            return "Cancelled"


def make_client_window(scores, keep_on_top):
    table_data = []
    for i in range(len(scores["players"])):
        row = [scores["players"][i], scores["scores"][i], scores["previous_scores"][i]]
        table_data.append(row)
    client_layout = [[Sg.Table(table_data, headings=["Players", "Scores", "Previous Scores"], key="score_table",
                               hide_vertical_scroll=True,
                               num_rows=len(scores["players"]))]]
    return Sg.Window("Jeopardy Score Client", client_layout, finalize=True, keep_on_top=keep_on_top)


def start_scorer_windows():
    scorer_layout = [[Sg.Text("Current Question:"), Sg.Text("N/A", key="current_question"), Sg.Text("Question Value:"),
                      Sg.Text("0000", key="question_value")],
                     [Sg.Text("       +       -     Other")]]
    for i in range(len(players)):
        scorer_layout.append([Sg.Text(players[i] + ":"),
                              Sg.Radio("", group_id="player_{}".format(i + 1), key="player_{}_add".format(i + 1)),
                              Sg.Radio("", group_id="player_{}".format(i + 1), key="player_{}_subtract".format(i + 1)),
                              Sg.Radio("", default=True, group_id="player_{}".format(i + 1),
                                       key="player_{}_other".format(i + 1)),
                              Sg.Input(key="player_{}_input".format(i + 1), size=(6, 1))])
    scorer_layout.extend(
        [[Sg.Text("Save to File:"), Sg.Input(key="filename", size=(18, 1)), Sg.FileSaveAs(file_types=(("Text Document","*.txt"),("all files","*.*")))],
         [Sg.Check("Keep client window on top", key="keep_on_top")],
         [Sg.Button("Update", key="update", bind_return_key=True), Sg.Button("Start Client", key="client_start"),
          Sg.Button("Save To File", key="save_to_file")]])
    scorer_window = Sg.Window("Jeopardy Score Host", scorer_layout, resizable=True, finalize=True)
    client_window, client_event, client_values = None, None, None
    scores = {"players": players, "scores": ["0" for _ in range(len(players))],
              "previous_scores": ["0" for _ in range(len(players))]}
    question_value = 0
    board = json.loads(open("board.json").read())
    while True:
        scorer_event, scorer_values = scorer_window.read(100)
        if scorer_event is None:
            return
        elif scorer_event == "client_start" and not client_window:
            scorer_window["client_start"].update(disabled=True)
            scorer_window["keep_on_top"].update(disabled=True)
            client_window = make_client_window(scores, scorer_values["keep_on_top"])
        elif scorer_event == "update":
            scores["previous_scores"] = scores["scores"][:]
            for i in range(len(scores["scores"])):
                if scorer_values["player_" + str(i + 1) + "_add"]:
                    scores["scores"][i] = str(int(scores["scores"][i]) + question_value)
                elif scorer_values["player_" + str(i + 1) + "_subtract"]:
                    scores["scores"][i] = str(int(scores["scores"][i]) - question_value)
                else:
                    add_to_score = scorer_values["player_" + str(i + 1) + "_input"]
                    if add_to_score.isnumeric() or (
                            len(add_to_score) > 1 and add_to_score[0] == "-" and add_to_score[1:].isnumeric()):
                        scores["scores"][i] = str(int(scores["scores"][i]) + int(add_to_score))
                scorer_window["player_" + str(i + 1) + "_add"](False)
                scorer_window["player_" + str(i + 1) + "_subtract"](False)
                scorer_window["player_" + str(i + 1) + "_other"](True)
                scorer_window["player_" + str(i + 1) + "_input"]("")
            if client_window is not None:
                table_data = []
                for i in range(len(players)):
                    row = [players[i], scores["scores"][i], scores["previous_scores"][i]]
                    table_data.append(row)
                client_window["score_table"].update(values=table_data)
        elif scorer_event == "save_to_file":
            if scorer_values["filename"] != "":
                open(scorer_values["filename"], "w").write(str(scores))
        current_question = open("SlideNotes.txt").read().strip("\n")
        scorer_window["current_question"](current_question)
        question_value = board[current_question]
        scorer_window["question_value"](str(question_value))
        if current_question == "DD":
            for i in range(len(scores["players"])):
                scorer_window["player_" + str(i + 1) + "_add"].update(disabled=True)
                scorer_window["player_" + str(i + 1) + "_subtract"].update(disabled=True)
        else:
            for i in range(len(scores["players"])):
                scorer_window["player_" + str(i + 1) + "_add"].update(disabled=False)
                scorer_window["player_" + str(i + 1) + "_subtract"].update(disabled=False)


if __name__ == "__main__":
    player_count = start_setup_window()
    if player_count == "Cancelled":
        sys.exit()
    players = start_enter_names_window()
    if players == "Cancelled":
        sys.exit()
    start_scorer_windows()
