from django.conf.urls import url
from api.views import GameRoomCreateView, PlayerCreateView, QuestionCreateView, AnswerCreateView, AnswerUpdateView, \
    AnswerListView, PlayerDestroyView

urlpatterns = [
    url(r'^gameroom/create/$', GameRoomCreateView.as_view()),
    url(r'^player/create/$', PlayerCreateView.as_view()),
    url(r'^question/create/$', QuestionCreateView.as_view()),
    url(r'^answer/create/$', AnswerCreateView.as_view()),
    url(r'^answer/update/$', AnswerUpdateView.as_view()),
    url(r'^answers/$', AnswerListView.as_view()),
    url(r'^player/delete/$', PlayerDestroyView.as_view())
]
