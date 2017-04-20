from django.conf.urls import url
from api.views import GameRoomCreateView, PlayerCreateView, QuestionCreateView, AnswerCreateView, AnswerUpdateView, \
    AnswerListView, PlayerDestroyView

urlpatterns = [
    url(r'^gameroom/create/$', GameRoomCreateView.as_view()),
    url(r'^player/create/$', PlayerCreateView.as_view()),
    url(r'^question/create/$', QuestionCreateView.as_view()),
    url(r'^answer/create/$', AnswerCreateView.as_view()),
    url(r'^answer/(?P<pk>[0-9]+)/update/$', AnswerUpdateView.as_view()),
    url(r'^answers/(?P<pk>[0-9]+)$', AnswerListView.as_view()), # gets the answers from question 'pk'
    url(r'^player/(?P<pk>[0-9]+)/delete/$', PlayerDestroyView.as_view()) #used a a player leaves the room
]
