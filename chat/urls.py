from django.urls import path
# from .views import HomeView
from .views import Signup, Login, HomeView, UsersList, ChatData


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('list-users/', UsersList.as_view(), name='list-users'),
    path('history/<int:id>/', ChatData.as_view(), name='chat-history'),
    

]
