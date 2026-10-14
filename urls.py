from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.PhoneLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("courses/", views.course_list, name="courses"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("code-library/", views.snippets, name="snippets"),
    path("resources/", views.resources, name="resources"),
    path("cv/", views.cv, name="cv"),
    path("staff/", views.staff_panel, name="staff"),
    path("staff/approve/<int:user_id>/", views.approve_user, name="approve_user"),
    path("staff/role/<int:user_id>/", views.change_role, name="change_role"),
    path("staff/delete/<int:user_id>/", views.delete_user, name="delete_user"),
]
