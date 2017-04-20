from api.models import GameRoom, Player, Question, Answer
from api.serializers import GameRoomSerializer, PlayerSerializer, QuestionSerializer, AnswerSerializer
from rest_framework import generics


class GameRoomCreateView(generics.CreateAPIView):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomSerializer


class PlayerCreateView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


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
    queryset = Answer.objects.all() # TODO we need to filter the answers based on GameRoom
    serializer_class = AnswerSerializer


class PlayerDestroyView(generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer