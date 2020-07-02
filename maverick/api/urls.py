from django.urls import path
from .views import MessagesView, WebHookView

urlpatterns = [
    # path('getmessages/', GetMessages.as_view()),
    path('sendMessage', MessagesView.as_view()),
    path('webhook', WebHookView),
]