from django.conf.urls import url
from api.views import GameRoomCreateView, PlayerCreateView, QuestionCreateView, AnswerCreateView, AnswerUpdateView, \
    AnswerListView, PlayerDestroyView, GameRoomListView, QuestionMasterRetrieveView, AnswerDetectiveRetrieveView, QuestionRetrieveView, GameRoomCloseView, GameRoomRetrieveView, GameRoomPlayersView, QuestionUnlockRetrieveView, \
    QuestionGetView

urlpatterns = [
    url(r'^gameroom/create/$', GameRoomCreateView.as_view()),
    url(r'^player/create/$', PlayerCreateView.as_view()),
    url(r'^question/create/$', QuestionCreateView.as_view()),
    url(r'^answer/create/$', AnswerCreateView.as_view()),
    url(r'^answer/(?P<pk>[0-9]+)/update/$', AnswerUpdateView.as_view()),
    url(r'^answers/(?P<pk>[0-9]+)/$', AnswerListView.as_view()), # gets the answers from question 'pk'
    url(r'^player/(?P<pk>[0-9]+)/delete/$', PlayerDestroyView.as_view()), #used a a player leaves the room,
    url(r'^gamerooms/location/(?P<lat>[0-9]+(\.[0-9]+)?)/(?P<long>[0-9]+(\.[0-9]+)?)/$', GameRoomListView.as_view()),
    url(r'^gameroom/(?P<game_room>[0-9]+)/questionmaster/$', QuestionMasterRetrieveView.as_view()),
    url(r'^gameroom/(?P<game_room>[0-9]+)/answerdetective/$', AnswerDetectiveRetrieveView.as_view()),
    url(r'^question/(?P<game_room>[0-9]+)/$', QuestionRetrieveView.as_view()),
    url(r'^gameroom/(?P<pk>[0-9]+)/close/$', GameRoomCloseView.as_view()),
    url(r'^gameroom/(?P<pk>[0-9]+)/$', GameRoomRetrieveView.as_view()),
    url(r'^gameroom/(?P<pk>[0-9]+)/players/$', GameRoomPlayersView.as_view()),
    url(r'^question/(?P<pk>[0-9]+)/unlock/$', QuestionUnlockRetrieveView.as_view()),
    url(r'^question/(?P<pk>[0-9]+)/question/$', QuestionGetView.as_view())
]
