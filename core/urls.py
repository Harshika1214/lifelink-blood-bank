from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Authentication
    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # User dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # Donor profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # Blood donation
    path(
        "donate/",
        views.donate_blood,
        name="donate"
    ),

    # Blood request
    path(
        "request-blood/",
        views.request_blood,
        name="request_blood"
    ),

    # Request history
    path(
        "my-requests/",
        views.my_requests,
        name="my_requests"
    ),

    # Blood inventory
    path(
        "inventory/",
        views.blood_inventory,
        name="inventory"
    ),

    # Cancel request
    path(
        "requests/<int:request_id>/cancel/",
        views.cancel_request,
        name="cancel_request"
    ),

    # Change password
    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),
]