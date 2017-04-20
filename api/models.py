from django.db import models

# Create your models here.


class GameRoom(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    password = models.CharField(max_length=50, null=True, blank=True)

    # these are used to determine games near a player
    longitude = models.DecimalField(decimal_places=7, max_digits=10)
    latitude = models.DecimalField(decimal_places=7, max_digits=10)

class Player(models.Model):
    game_room = models.ForeignKey(GameRoom)
    name = models.CharField(max_length=20, null=False, blank=False)

class Question(models.Model):
    value = models.CharField(max_length=300, null=False, blank=False)
    creator = models.ForeignKey(Player)

class Answer(models.Model):
    value = models.CharField(max_length=300, null=False, blank=True)
    creator = models.ForeignKey(Player)
    question = models.ForeignKey(Question)

