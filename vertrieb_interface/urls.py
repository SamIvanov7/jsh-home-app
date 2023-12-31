from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from vertrieb_interface import views
from vertrieb_interface.views import PDFAngebotsListView
from django.views import defaults as default_views

app_name = "vertrieb_interface"

urlpatterns = [
    path("vertrieb/home/", views.home, name="home"),
    path(
        "vertrieb/vertrieb_autofield/",
        views.VertriebAutoFieldView.as_view(),
        name="vertrieb_autofield",
    ),
    path("vertrieb/create_angebot/", views.create_angebot, name="create_angebot"),
    path("vertrieb/help/", views.help, name="help"),
    path("vertrieb/chat_bot/", views.chat_bot, name="chat_bot"),
    path(
        "vertrieb/load_user_angebots/",
        views.load_user_angebots,
        name="load_user_angebots",
    ),
    path("vertrieb/profile/", views.profile, name="profile"),
    path("vertrieb/view_orders/", views.ViewOrders.as_view(), name="view_orders"),
    path(
        "vertrieb/edit_angebot/<str:angebot_id>/",
        views.AngebotEditView.as_view(),
        name="edit_angebot",
    ),
    path(
        "vertrieb/create_angebot_pdf/<str:angebot_id>",
        views.create_angebot_pdf,
        name="create_angebot_pdf",
    ),
    path(
        "vertrieb/create_angebot_pdf_user/<str:angebot_id>",
        views.create_angebot_pdf_user,
        name="create_angebot_pdf_user",
    ),
    path(
        "vertrieb/create_ticket_pdf/<str:angebot_id>",
        views.create_ticket_pdf,
        name="create_ticket_pdf",
    ),
    path(
        "vertrieb/create_calc_pdf/<str:angebot_id>",
        views.create_calc_pdf,
        name="create_calc_pdf",
    ),
    path(
        "vertrieb/pdf_angebots_list_view/",
        views.pdf_angebots_list_view,
        name="pdf_angebots_list_view",
    ),
    path(
        "vertrieb/pdf_angebots/<str:angebot_id>/",
        PDFAngebotsListView.as_view(),
        name="pdf_angebots_list",
    ),
    path(
        "PDFCalculationsListView/<str:angebot_id>/",
        views.PDFCalculationsListView,
        name="PDFCalculationsListView",
    ),
    path(
        "PDFTicketListView/<str:angebot_id>/",
        views.PDFTicketListView,
        name="PDFTicketListView",
    ),
] + [
    re_path(
        r"^400/$",
        default_views.bad_request,
        kwargs={"exception": Exception("Bad Request!")},
    ),
    re_path(
        r"^403/$",
        default_views.permission_denied,
        kwargs={"exception": Exception("Permission Denied")},
    ),
    re_path(
        r"^404/$",
        default_views.page_not_found,
        kwargs={"exception": Exception("Page not Found")},
    ),
    re_path(r"^500/$", default_views.server_error),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
