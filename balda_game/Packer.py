import json
from balda_game.GameManagerProcessor import GameProcessor

__author__ = 'akhtyamovpavel'


def pack_game_message_with_action(game_id, user, action='none'):
    game_id = int(game_id)
    field_pack = GameProcessor.get_field(game_id)
    current_player = GameProcessor.get_current_player(game_id)

    first_player, second_player = GameProcessor.get_players(game_id)

    user_player = 1
    if user == first_player:
        user_player = 0

    if GameProcessor.is_game_ended(game_id):
        action='end'
        GameProcessor.end_game(game_id)

    score1, score2 = GameProcessor.get_scores(game_id)
    player1, player2 = GameProcessor.get_players(game_id)
    is_your_move = user_player == current_player
    json_result = {"action": action,
                   "field": field_pack,
                   "current_player": current_player,
                   "is_your_move": is_your_move,
                   "score1": score1,
                   "score2": score2,
                   "player1": player1.username,
                   "player2": player2.username
                   }

    print(json_result)
    return json.dumps(json_result)


def deserialize_int(value):
    return int(value)

def deserialize_list(list_value):
    return [int(value) for value in list_value]

