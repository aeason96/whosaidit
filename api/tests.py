from api.models import GameRoom, Player, Question, Answer
from rest_framework.test import APITestCase
from rest_framework import status

class TestAPIEndpoint(APITestCase):

    def test_create_game_room(self):
        """
        tests that we can create a new game room with a post to the endpoint that has a name, password
        and coordinates.
        """
        url = '/api/gameroom/create/'
        data = {'name': 'test', "password": 'test', 'longitude': 1.1, 'latitude': 1.1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GameRoom.objects.count(), 1)
        self.assertEqual(GameRoom.objects.get(pk=1).name, 'test')

    def test_player_create_joins_game(self):
        """
        tests that a player can join the game with the write game room credentials.
        """
        GameRoom(name='test', password='test').save()
        url = '/api/player/create/'
        data = {'name': 'kevin', 'game_room': {'id': 1, 'name': 'test', 'password': 'test'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Player.objects.get(pk=1).game_room_id, 1) # assert this player belongs to game room 1

    def test_player_creation_requires_game_room_credentials(self):
        """
        tests a failed creation of a player because of wrong game room credentials.
        """
        GameRoom(name='test', password='test').save()
        url = '/api/player/create/'
        data = {'name': 'kevin', 'game_room': {'id': 1, 'name': 'test', 'password': ''}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_create_view(self):
        """
        tests that a player can create a new question to be used within the game room
        """
        GameRoom(name='test', password='test').save()
        Player(game_room_id=1, name='test').save()
        url = '/api/question/create/'
        data = {'value': 'Is this a test?', 'creator': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.get(pk=1).value, 'Is this a test?')

    def test_answer_create_view(self):
        """
        tests that an answer can be created in relation to a question. One answer per question
        """
        GameRoom(name='test', password='test').save()
        Player(game_room_id=1, name='test').save()
        Question(value='question', creator_id=1).save()
        url = '/api/answer/create/'
        data = {'value': 'answer to a question', 'creator': 1, 'question': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.get(pk=1).value, 'answer to a question')


    def test_answer_create_no_more_than_one_per_user_per_question(self):
        """
        tests that an answer can be created in relation to a question. One answer per question
        """
        GameRoom(name='test', password='test').save()
        Player(game_room_id=1, name='test').save()
        Question(value='question', creator_id=1).save()
        url = '/api/answer/create/'
        data = {'value': 'answer to a question', 'creator': 1, 'question': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        r = self.client.post(url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_update_success(self):
        """
        tests that a answer to a question can be updated. This should only happen if
        everyone in the game room has NOT finished answering the current question yet.
        """
        url = '/api/answer/1/update/'
        GameRoom(name='test', password='test').save()
        Player(game_room_id=1, name='test').save()
        Question(value='question', creator_id=1).save()
        Answer(value='test', creator_id=1, question_id=1).save()
        data = {'value': 'updated', 'creator': 1, 'question': 1}
        self.client.patch(url, data, format='json')
        self.assertEqual(Answer.objects.get(pk=1).value, 'updated')

    def test_answer_list(self):
        """
        tests that an answer list received from the endpoint only contains answers
        related to the question in the url query
        """
        url = '/api/answers/1/' # get the answers from question with pk 1
        GameRoom(name='test', password='test').save()
        Player(game_room_id=1, name='test').save()
        Player(game_room_id=1, name='test2').save()
        Question(value='question', creator_id=1).save()
        Question(value='question2', creator_id=1).save()
        Answer(value='test', creator_id=1, question_id=1).save()
        Answer(value='test', creator_id=2, question_id=1).save()
        Answer(value='test2', creator_id=1, question_id=2).save()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_player_destroy(self):
        """
        test that making a call to this endpoint destorys the database reference to this player
        """
        pass

    def test_game_room_destroyed_last_player_leaves(self):
        """
        tests that a game room is destroyed when its last player leaves
        """
        pass

    def test_distance_from_gameroom(self):
        g = GameRoom(longitude=100.00, latitude=200.00)
        self.assertAlmostEqual(g.distance_from(300, 100), 223.6068, places=4)

    def test_get_game_rooms_from_coordinates(self):
        """
        tests querying the db for game rooms within a certain radius distance of the corrdinated posted
        """
        pass



class TestGameLogic(APITestCase):

    def test_choosing_new_question_master(self):
        """
        tests choosing a new question master form the queue
        """
        pass

    def test_choosing_new_answer_detective(self):
        """
        tests choosing a new answer detective form the queue
        """
        pass

    def test_queue_question_master_wraps_around(self):
        """
        tests choosing a question master form the queue. Upon completion,
        this user should be appended to the end of the queue and the next user should be selected from the queue
        """
        pass

    def test_queue_answer_detective_wraps_around(self):
        """
        tests choosing a new answer detective form the queue. Upon completion,
        this user should be appended to the end of the queue and the next user should be selected from the queue
        """
        pass