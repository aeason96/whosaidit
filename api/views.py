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


class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


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
