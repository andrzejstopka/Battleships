import socket
import json


message_by_status = {0: None, 1: "Server is playing the other game.", 2: "The shot is not within the boundaries of the board.",
                     3: "Internal server error, game is aborted.", 4: "The server cannot recognize the request"}


def server_game_invitation(playing):
    try:
        if playing is False:
            status = 0
        elif playing is True:
            status = 1
        else:
            status = 4
    except socket.error:
        status = 3
    return {"type": "GAME_INVITATION", "status": status, "message": message_by_status[status], "body": None}

def board_arrangement(arrangement):
    return {"type": "BOARD_ARRANGEMENT", "body": arrangement}

def cord_request(ship_name, ship_spaces):
    if ship_name != "Destroyer":
        return {"type": "CORD_REQUEST",
                "message": f"Enter a start coordinates and horizon(h/v) for {ship_name}({ship_spaces} spaces) (e.g. A1v): "}
    else:
        return {"type": "CORD_REQUEST", "message": f"Enter a coordinates for {ship_name}(e.g. A1): "}


def cord_answer(answer):
    try:
        if answer == "Placed":
            status = 0
            message = "Placed"
        else:
            status = 2
            message = answer
    except socket.error:
        status = 3
        message = message_by_status[status]

    return {"type": "CORD_ACCEPTANCE", "status": status, "message": message, "body": None}


# def locating_done():
#     return {"type": "CORD_ACCEPTANCE", "message": "Done"}


def ships_cords(row, column, horizon):
    return {"type": "LOCATE_SHIP", "body": {"row": row, "column": column, "horizon": horizon}}


def shot(row, column):
    return {"type": "SHOT", "body": {"row": row, "column": column}}


def shot_answer(body):
    try:
        if body == "Out of board":
            status = 2
            body = None
        else:
            status = 0
    except socket.error:
        status = 3

    return {"type": "SHOT", "status": message_by_status[status], "message": None, "body": body}


def shot_request():
    return {"type": "SHOT_REQUEST", "body": None}


def server_shot(row, column):
    try:
        status = 0
    except socket.error:
        status = 3
    return {"type": "SHOT_REQUEST", "status": status, "message": message_by_status[status],
            "body": {"row": row, "column": column}}


def result_response():
    try:
        status = 0
    except socket.error:
        status = 3
    return {"type": "RESULT", "status": status, "message": message_by_status[status], "body": None}

# DO ZROBIENIA PRZESŁANIE UKŁADU STATKÓW PO SKOŃCZONEJ GRZE


game_invitation = json.dumps({"type": "GAME_INVITATION", "body": None})
