from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.index, name="index"),
    path("htmx-term-res/", views.htmx_term_res, name="htmx_term_res"),
    path("api/execute_command/", views.execute_command, name="execute_command"),
]
