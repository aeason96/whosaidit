from api.models import GameRoom, Player, Question, Answer
from api.serializers import GameRoomSerializer, PlayerSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class GameRoomCreateView(generics.CreateAPIView):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomSerializer

    def post(self, request, *args, **kwargs):
        game_room_name = request.data['name']
        if GameRoom.objects.filter(name=game_room_name).exists():
            raise ValidationError('Your game room name must be unique')
        return super(GameRoomCreateView, self).post(request, *args, **kwargs)


class GameRoomListView(generics.ListAPIView):
    serializer_class = GameRoomSerializer

    def get(self, request, *args, **kwargs):
        latitude = float(kwargs.pop('lat'))
        longitude = float(kwargs.pop('long'))
        self.queryset = sorted(GameRoom.objects.all(), key=lambda d: d.distance_from(longitude, latitude))
        return super(GameRoomListView, self).get(request, *args, **kwargs)


class PlayerCreateView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def post(self, request, *args, **kwargs):
        try:
            GameRoom.objects.get(**request.data['game_room'])
        except:
            raise AuthenticationFailed('Your GameRoom or Password was incorrect')
        return super(PlayerCreateView, self).post(request, *args, **kwargs)


class QuestionMasterRetrieveView(generics.RetrieveAPIView):
    serializer_class = PlayerSerializer
    lookup_field = 'game_room'

    def get(self, request, *args, **kwargs):
        current_master = list(Player.objects.filter(game_room_id=kwargs['game_room'], question_master=True))
        if (len(current_master) == 1):
            current_master[0].question_master = False
            current_master[0].save()
            players = list(Player.objects.filter(game_room_id=kwargs['game_room']))
            current_id = players.index(current_master[0])
            next_master = players[(current_id + 1) % len(players)]
            next_master.question_master = True
            next_master.save()
        else: # the room has not been assigned a question aster yet, get the first person
            question_master = Player.objects.filter(game_room_id=kwargs['game_room'])[0]
            question_master.question_master = True
            question_master.save()
        self.queryset = Player.objects.filter(game_room_id=kwargs['game_room'], question_master=True)
        return super(QuestionMasterRetrieveView, self).get(request, *args, **kwargs)

class AnswerDetectiveRetrieveView(generics.RetrieveAPIView):
    serializer_class = PlayerSerializer
    lookup_field = 'game_room'

    def get(self, request, *args, **kwargs):
        current_detective = Player.objects.filter(game_room_id=kwargs['game_room'], answer_detective=True)
        if (len(current_detective) == 1):
            current_detective[0].answer_detective = False
            current_detective[0].save()
            players = list(Player.objects.filter(game_room_id=kwargs['game_room'], question_master=False))
            current_id = players.index(current_detective[0])
            next_detective = players[(current_id + 1) % len(players)]
            next_detective.answer_detective = True
            next_detective.save()
        else:
            answer_detective = Player.objects.filter(game_room_id=kwargs['game_room'], question_master=False)[0]
            answer_detective.answer_detective = True
            answer_detective.save()
        self.queryset = Player.objects.filter(game_room_id=kwargs['game_room'], answer_detective=True)
        return super(AnswerDetectiveRetrieveView, self).get(request, *args, **kwargs)

class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        previous_question = Question.objects.filter(active=True)
        if previous_question.exists():
            for question in previous_question:
                question.active = False
                question.save()
        return super().post(request, *args, **kwargs)


class QuestionRetrieveView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    lookup_field = 'game_room'
    queryset = Question.objects.filter(active=True)


class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerUpdateView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Answer.objects.filter(question_id=kwargs['pk'])
        return super(AnswerListView, self).get(request, *args, **kwargs)


class PlayerDestroyView(generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def delete(self, request, *args, **kwargs):
        player = Player.objects.get(pk=kwargs['pk'])
        game_room = GameRoom.objects.get(player=player)
        if len(Player.objects.filter(game_room=game_room)) == 1:
            game_room.delete()
        super(PlayerDestroyView, self).delete(request, *args, **kwargs)
