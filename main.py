"""Run this file to start the program"""
import PySimpleGUI as sg
import sys


def start_setup_window():
    setup_window_layout = [[sg.Text('Enter Number of Players'), sg.InputText()],
                           [sg.Button('Ok', bind_return_key=True), sg.Button('Cancel')]]
    setup_window = sg.Window('Jeopardy Scorer Setup', setup_window_layout)
    while True:
        event, values = setup_window.read()
        if event == 'Cancel' or event is None:  # if user closes window or clicks cancel
            setup_window.close()
            return "Cancelled"
        elif values[0].isnumeric() and int(values[0]) > 0:
            setup_window.close()
            return int(values[0])
        elif values[0] == "0":
            sg.popup_error("There must be at least one player!")


def start_enter_names_window(player_count):
    enter_names_window_layout = [[sg.Text('Enter the names of each player in the fields below')]]
    for i in range(player_count):
        enter_names_window_layout.append([sg.Text("Player {}".format(i + 1)), sg.InputText()])
    enter_names_window_layout.append([sg.Button("Confirm", bind_return_key=True), sg.Button("Cancel")])
    enter_names_window = sg.Window('Enter Names of Players', enter_names_window_layout)
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
    client_layout = [[sg.Table(table_data, headings=["Players", "Scores", "Previous Scores"], key="score_table",
                               hide_vertical_scroll=True,
                               num_rows=len(scores["players"]))]]
    return sg.Window("Jeopardy Score Client", client_layout, finalize=True, keep_on_top=keep_on_top)


def start_scorer_windows(players):
    scorer_layout = []
    for i in range(len(players)):
        scorer_layout.append([sg.Text(players[i] + ":"), sg.Input(key="player_{}".format(i + 1))])
    scorer_layout.extend(
        [[sg.Check("Keep client window on top", key="keep_on_top")],[sg.Button("Update", key="update", bind_return_key=True), sg.Button("Start Client", key="client_start")]])
    scorer_window = sg.Window("Jeopardy Score Host", scorer_layout, resizable=True, finalize=True)
    client_window, client_event, client_values = None, None, None
    scores = {"players": players, "scores": ["0" for _ in range(len(players))],
              "previous_scores": ["0" for _ in range(len(players))]}
    while True:
        scorer_event, scorer_values = scorer_window.read()
        if scorer_event is None:
            return
        elif scorer_event == "client_start" and not client_window:
            scorer_window["client_start"].update(disabled=True)
            scorer_window["keep_on_top"].update(disabled=True)
            client_window = make_client_window(scores, scorer_values["keep_on_top"])
        elif scorer_event == "update":
            scores["previous_scores"] = scores["scores"][:]
            for i in range(len(scores["scores"])):
                add_to_score = scorer_values["player_" + str(i + 1)]
                if add_to_score.isnumeric() or (
                        len(add_to_score) > 1 and add_to_score[0] == "-" and add_to_score[1:].isnumeric()):
                    scores["scores"][i] = str(int(scores["scores"][i]) + int(add_to_score))
                scorer_window["player_" + str(i + 1)]("")
            if client_window is not None:
                table_data = []
                for i in range(len(players)):
                    row = [players[i], scores["scores"][i], scores["previous_scores"][i]]
                    table_data.append(row)
                client_window["score_table"].update(values=table_data)


if __name__ == "__main__":
    player_count = start_setup_window()
    if player_count == "Cancelled":
        sys.exit()
    players = start_enter_names_window(player_count)
    if players == "Cancelled":
        sys.exit()
    start_scorer_windows(players)
