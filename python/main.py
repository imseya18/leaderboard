import requests

def fetch_data(url):
    response = requests.get(url)
    return response.json()


def GetAllUniqueIds(uniqueId):
    datas = fetch_data(f"http://localhost:8020/player/get/{uniqueId}")
    result = []
    seen = set()

    for data in datas:
        for player_id in (data["player1_id"], data["player2_id"]):
            if player_id not in seen:
                result.append(player_id)
                seen.add(player_id)

    ids_string = ",".join(map(str, result))
    return datas, ids_string


def updatePlayerData(data, player_key, unique_ids_data):
    player_id = str(data[f"{player_key}_id"])
    if player_id in unique_ids_data:
        if data[f"{player_key}_id"] == data["winner_id"]:
            data["winner_id"] = unique_ids_data[player_id]['username']
        data[f"{player_key}_img"] = unique_ids_data[player_id]["profile_picture"]
        data[f"{player_key}_id"] = unique_ids_data[player_id]['username']
    else:
        data[f"{player_key}_img"] = None


def AddNameAndImgToDict(final_dict, unique_ids):
    unique_ids_data = fetch_data(f"http://localhost:8050/auth/user_info/{unique_ids}/")
    for data in final_dict:
        updatePlayerData(data, "player1", unique_ids_data)
        updatePlayerData(data, "player2", unique_ids_data)
    return final_dict


def GetMatchHistory(uniqueId):
    try:
        final_dict, unique_ids = GetAllUniqueIds(uniqueId)
        final_dict = AddNameAndImgToDict(final_dict, unique_ids)
        print(final_dict)
    except requests as e:
        return None

GetMatchHistory(13)
