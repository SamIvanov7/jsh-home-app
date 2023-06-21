from django.urls import path, include
from django.urls import path
from authentication.api import LoginView, LogoutView
# from invoices.views import home
from authentication.views import (
    update_vertrieblers,
    update_elektrikers,
    protected_schema_view,
)

app_name = "authentication"

urlpatterns = [
    path("admin/update_vertrieblers/", update_vertrieblers, name="update_vertrieblers"),
    path("admin/update_elektrikers/", update_elektrikers, name="update_elektrikers"),
    path("admin/schema/", protected_schema_view, name="schema_view"),
    # path("", home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
