from app.mock.mock_player import create_player

player_list = [create_player() for _ in range(5)]
player_list.append(create_player("user1"))