from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('note-page/',views.notePage, name="note-page"),
    path('create-note/', views.createNote, name="create-note"),
    path('note-page/update-note/<str:pk>', views.updateNote, name="update-note"),
    path('delete-note/<str:pk>', views.deleteNote, name="delete-note"),
    path('note-page/update-note/share-note/<str:pk>', views.shareNote, name="share-note"),
    
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    path('add-member/<str:pk>', views.addMember, name="add-member"),
    path('remove-user/<str:pk>/<str:rk>', views.removeMember, name="remove-user"),
    path('leave-room/<str:pk>', views.leaveRoom, name="leave-room"),


    path('user-profile/<str:pk>', views.userProfile, name="user-profile"),
    path('update-profile/', views.updateProfile, name="update-profile"),


    path('login/',views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


]