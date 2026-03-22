from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hobbies",views.hobbies,name="hobbies"),
    path("hobbies/<int:hobby_id>/", views.hobby, name="hobby"),
    path("user/<int:user_id>/", views.user, name="user"),
    path("vote/<int:hobby_id>", views.vote, name="vote"),
    path("add_offering/", views.add_offering, name="add_offering"),
    path("add_hobby/", views.add_hobby, name="add_hobby"),
    path("offering/<int:offering_id>/", views.offering_detail, name="offering_detail"),
    path("gangs", views.gangs, name="gangs"),
     path("gangs/<int:gang_id>/leave/", views.leave_gang, name="leave_gang"),
    path("gangs/create/", views.create_gang, name="create_gang"),
]
