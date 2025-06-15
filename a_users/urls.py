from django.urls import path
from .views import profile_view, profile_edit, users, verify, send_email


urlpatterns = [
    path("", users, name="users"),
    path("<username>/", profile_view, name="profile"),
    path("<username>/edit/", profile_edit, name="profile_edit"),
    path("send_mail/<uuid:profile_uuid>/", send_email, name="send_mail"),
    path("verify/<uuid:profile_uuid>/", verify, name="verify"),
]
