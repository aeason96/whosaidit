from math import sqrt
from decimal import Decimal
from django.db import models

# Create your models here.


class GameRoom(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=50, null=False, blank=False)

    # these are used to determine games near a player
    longitude = models.DecimalField(decimal_places=7, max_digits=10, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=7, max_digits=10, null=True, blank=True)
    accepting_players = models.BooleanField(default=True)

    def distance_from(self, longitude, latitude):
        return sqrt((Decimal(self.longitude) - Decimal(longitude)) ** 2 + (Decimal(self.latitude) - Decimal(latitude)) ** 2)

class Player(models.Model):
    game_room = models.ForeignKey(GameRoom)
    name = models.CharField(max_length=20, null=False, blank=False)
    question_master = models.BooleanField(default=False)
    answer_detective = models.BooleanField(default=False)

    class Meta:
        unique_together = ('game_room', 'name')

class Question(models.Model):
    value = models.CharField(max_length=300, null=False, blank=False)
    creator = models.ForeignKey(Player)
    game_room = models.ForeignKey(GameRoom)
    active = models.BooleanField(default=True)
    unlocked = models.BooleanField(default=False)

class Answer(models.Model):
    value = models.CharField(max_length=300, null=False, blank=True)
    creator = models.ForeignKey(Player)
    question = models.ForeignKey(Question)
    winner = models.BooleanField(default=False)

    class Meta:
        unique_together = ('creator', 'question')