
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # Home
    path("", views.home, name="index"),

    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "api/dashboard/",
        views.live_dashboard_api,
        name="live_dashboard_api",
    ),

    # Harvest and Irrigation
    path("harvest/", views.harvest, name="harvest"),
    path("irrigation/", views.irrigation, name="irrigation"),
    path("weather/", views.weather, name="weather"),
    path(
        "water-management/",
        views.water_management,
        name="water_management",
    ),
    path("storage/", views.storage, name="storage"),
    path("analytics/", views.analytics, name="analytics"),

    # Farmers and Buyers
    path("farmers/", views.farmers, name="farmers"),
    path("buyers/", views.buyers, name="buyers"),

    # Settings
    path("settings/", views.settings_page, name="settings"),

    # Direct Chat
    path(
        "chat/<int:user_id>/",
        views.direct_chat,
        name="direct_chat",
    ),

    # Password Reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
