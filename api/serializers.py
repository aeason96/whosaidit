from rest_framework import serializers

from api.models import GameRoom, Player, Question, Answer


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = '__all__'
        write_only_fields = ('password')
        extra_kwargs = {
            'name': {
                'validators': []
            }
        }


class PlayerSerializer(serializers.ModelSerializer):
    game_room = GameRoomSerializer()  # specify this for nested serialization

    def create(self, validated_data):
        game_room_data = validated_data.pop('game_room')
        return Player.objects.create(game_room=GameRoom.objects.get(**game_room_data), **validated_data)

    class Meta:
        model = Player
        exclude = ('question_master', 'answer_detective')
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = '__all__'

class AnswerSerializerDepth(serializers.ModelSerializer):
    creator = PlayerSerializer()
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = '__all__'
        depth = 1