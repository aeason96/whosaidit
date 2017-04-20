from api.models import GameRoom, Player
from rest_framework.test import APITestCase
from rest_framework import status

class TestAPIEndpoint(APITestCase):

    def test_create_game_room(self):
        url = '/api/gameroom/create/'
        data = {'name': 'test', "password": 'test', 'longitude': 1.1, 'latitude': 1.1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GameRoom.objects.count(), 1)
        self.assertEqual(GameRoom.objects.get(pk=1).name, 'test')

    def test_player_create_joins_game(self):
        GameRoom(name='test', password='test').save()
        url = '/api/player/create/'
        data = {'name': 'kevin', 'game_room': {'id': 1, 'name': 'test', 'password': 'test'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Player.objects.get(pk=1).game_room_id, 1) # assert this player belongs to game room 1

    def test_player_creation_requires_game_room_credentials(self):
        pass


    def test_question_create_view(self):
        pass

    def test_answer_create_view(self):
        pass

    def test_answer_create_no_more_than_one_per_user_per_question(self):
        pass

    def test_answer_list(self):
        pass

    def test_player_destroy(self):
        pass

    def test_game_room_destroyed_last_player_leaves(self):
        pass

    def test_get_game_rooms_from_coordinates(self):
        pass
    