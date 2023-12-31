import os
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from shared.chat_bot import handle_message
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import IntegerField, Q
from vertrieb_interface.get_user_angebots import (
    fetch_all_user_angebots,
    fetch_current_user_angebot,
)
from django.contrib.auth.decorators import login_required
from vertrieb_interface.pdf_services import (
    angebot_pdf_creator,
    angebot_pdf_creator_user,
    calc_pdf_creator,
    ticket_pdf_creator,
)
from vertrieb_interface.utils import load_vertrieb_angebot
from vertrieb_interface.models import VertriebAngebot
from vertrieb_interface.forms import VertriebAngebotForm
from config import settings
import datetime
from dotenv import load_dotenv
import json
from django.utils import timezone
from config.settings import ENV_FILE
from django.views.defaults import page_not_found
from django.core.exceptions import PermissionDenied

NAMES_CHOICES = ""


load_dotenv(ENV_FILE)
User = get_user_model()


def handler404(request, exception):
    return render(request, "404.html", status=404)


def vertrieb_check(user):
    return User.objects.filter(id=user.id, beruf="Vertrieb").exists()


class VertriebCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return vertrieb_check(self.request.user)


@user_passes_test(vertrieb_check)
def home(request):
    return render(request, "vertrieb/home.html")


@user_passes_test(vertrieb_check)
def profile(request, *args, **kwargs):
    user = request.user
    context = {"user": user}
    return render(request, "vertrieb/profile.html", context)


@user_passes_test(vertrieb_check)
def help(request):
    return render(request, "vertrieb/help.html")


@user_passes_test(vertrieb_check)
@csrf_exempt
def chat_bot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")
        response = handle_message(question)
        return JsonResponse({"response": response})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@user_passes_test(vertrieb_check)
def create_angebot(request):
    form_angebot = VertriebAngebotForm(request.POST or None, user=request.user)
    print(form_angebot.errors)
    if form_angebot.is_valid():
        vertrieb_angebot = form_angebot.save(commit=False)
        vertrieb_angebot.user = request.user
        vertrieb_angebot.save()

        return redirect("vertrieb_interface:edit_angebot", vertrieb_angebot.angebot_id)

    if request.POST and "create_blank_angebot" in request.POST:
        blank_angebot = VertriebAngebot(user=request.user)
        blank_angebot.created_at = timezone.now()
        blank_angebot.current_date = datetime.datetime.now()
        blank_angebot.save()
        return HttpResponseRedirect(
            reverse("vertrieb_interface:edit_angebot", args=[blank_angebot.angebot_id])
        )

    if not form_angebot.is_valid():
        print(form_angebot.errors)
        return page_not_found(request, Exception())

    return render(request, "vertrieb/edit_angebot.html", {"form_angebot": form_angebot})


class VertriebAutoFieldView(View, VertriebCheckMixin):
    data = []

    def get(self, request, *args, **kwargs):
        name = request.GET.get("name", None)
        self.data = fetch_all_user_angebots(request)
        data = next((item for item in self.data if item["name"] == name), None)

        if data is None:
            data = {}
            print(data)

        return JsonResponse(data)


class AngebotEditView(LoginRequiredMixin, VertriebCheckMixin, FormMixin, View):
    model = VertriebAngebot
    form_class = VertriebAngebotForm
    template_name = "vertrieb/edit_angebot.html"
    context_object_name = "vertrieb_angebot"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()  # This will use your custom 403.html template
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, angebot_id=self.kwargs.get("angebot_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vertrieb_angebot = self.get_object()
        context["form"] = self.form_class(
            instance=vertrieb_angebot, user=self.request.user
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get(self, request, angebot_id, *args, **kwargs):
        vertrieb_angebot = VertriebAngebot.objects.get(
            angebot_id=angebot_id, user=request.user
        )
        zoho_id = vertrieb_angebot.zoho_id

        data = fetch_current_user_angebot(request, zoho_id)
        for item in data:
            vertrieb_angebot.status = item["status"] if item["status"] else ""
            if (
                vertrieb_angebot.status == "bekommen"
                and not vertrieb_angebot.status_change_date
            ):
                current_datetime = datetime.datetime.now()
                vertrieb_angebot.status_change_date = (
                    f"{current_datetime.strftime('%d.%m.%Y')}"
                )
            vertrieb_angebot.anfrage_ber = item["anfrage_berr"]

            vertrieb_angebot.angebot_bekommen_am = (
                item["angebot_bekommen_am"] if item["angebot_bekommen_am"] else ""
            )
            vertrieb_angebot.ausrichtung = item["ausrichtung"]
            vertrieb_angebot.verbrauch = item["verbrauch"]
            vertrieb_angebot.leadstatus = (
                item["leadstatus"] if item["leadstatus"] else ""
            )
            vertrieb_angebot.notizen = item["notizen"]
            vertrieb_angebot.empfohlen_von = item["empfohlen_von"]
            vertrieb_angebot.termine_text = item["termine_text"]
            vertrieb_angebot.termine_id = item["termine_id"]
            print("SUCCESS!!!")
        form = self.form_class(instance=vertrieb_angebot, user=request.user)
        context = self.get_context_data()
        context["vertrieb_angebot"] = vertrieb_angebot
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        vertrieb_angebot = self.get_object()
        form = self.form_class(
            request.POST, instance=vertrieb_angebot, user=request.user
        )

        if form.is_valid():
            vertrieb_angebot.is_locked = True
            form.save()
            return redirect(
                "vertrieb_interface:edit_angebot", vertrieb_angebot.angebot_id
            )

        return self.form_invalid(form, vertrieb_angebot)

    def form_invalid(self, form, vertrieb_angebot):
        context = self.get_context_data()
        context["vertrieb_angebot"] = vertrieb_angebot
        context["form"] = form
        print(form.errors)
        return render(self.request, self.template_name, context)

    def load_data_from_zoho_to_angebot_id(self, request):
        pass


class ViewOrders(LoginRequiredMixin, VertriebCheckMixin, ListView):
    model = VertriebAngebot
    template_name = "vertrieb/view_orders.html"
    context_object_name = "angebots"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()  # This will use your custom 403.html template
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.filter(
            user=self.request.user, zoho_kundennumer__regex=r"^\d+$"
        )
        queryset = queryset.annotate(
            zoho_kundennumer_int=Cast("zoho_kundennumer", IntegerField())
        )
        queryset = queryset.order_by("-zoho_kundennumer_int")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(zoho_kundennumer__icontains=query)
                | Q(angebot_id__icontains=query)
                | Q(status__icontains=query)
                | Q(name__icontains=query)
                | Q(anfrage_vom__icontains=query)
            )

        return queryset


@user_passes_test(vertrieb_check)
def load_user_angebots(request):
    try:
        profile, created = User.objects.get_or_create(zoho_id=request.user.zoho_id)
        user = get_object_or_404(User, zoho_id=request.user.zoho_id)
        kurz = user.kuerzel
        all_user_angebots_list = fetch_all_user_angebots(request)

        zoho_data = json.dumps(all_user_angebots_list)
        profile.zoho_data_text = zoho_data
        profile.save()
        load_vertrieb_angebot(all_user_angebots_list, user, kurz)
        return render(request, "vertrieb/home.html")
    except Exception:
        return page_not_found(request, Exception())


def create_ticket_pdf(request, angebot_id):
    vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
    user = vertrieb_angebot.user
    if request.user != vertrieb_angebot.user and not request.user.is_staff:
        return page_not_found(request, Exception())
    data = vertrieb_angebot.data

    ticket_pdf_creator.createTicketPdf(
        data,
        vertrieb_angebot,
        user,
    )
    # Create the link to the PDF file
    pdf_link = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Tickets/Ticket_{vertrieb_angebot.angebot_id}.pdf")  # type: ignore

    # Redirect to the PDF file link
    return HttpResponseRedirect(pdf_link)


def create_calc_pdf(request, angebot_id):
    vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
    user = vertrieb_angebot.user
    if request.user != vertrieb_angebot.user and not request.user.is_staff:
        return page_not_found(request, Exception())
    data = vertrieb_angebot.data

    calc_pdf_creator.createCalcPdf(
        data,
        vertrieb_angebot,
        user,
    )
    # Create the link to the PDF file
    pdf_link = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Kalkulationen/Kalkulation_{vertrieb_angebot.angebot_id}.pdf")  # type: ignore

    # Redirect to the PDF file link
    return HttpResponseRedirect(pdf_link)


def create_angebot_pdf(request, angebot_id):
    vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
    user = vertrieb_angebot.user
    if not request.user.is_staff:
        raise PermissionDenied()
    data = vertrieb_angebot.data

    angebot_pdf_creator.createOfferPdf(
        data,
        vertrieb_angebot,
        user,
    )
    # Create the link to the PDF file
    pdf_link = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Angebot_{vertrieb_angebot.angebot_id}.pdf")  # type: ignore

    # Redirect to the PDF file link
    return HttpResponseRedirect(pdf_link)


@user_passes_test(vertrieb_check)
def create_angebot_pdf_user(request, angebot_id):
    vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
    user = vertrieb_angebot.user
    if request.user != vertrieb_angebot.user and not request.user.is_staff:
        raise PermissionDenied()
    data = vertrieb_angebot.data

    angebot_pdf_creator_user.createOfferPdf(
        data,
        vertrieb_angebot,
        user,
    )
    # Create the link to the PDF file
    pdf_link = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Angebot_{vertrieb_angebot.angebot_id}.pdf")  # type: ignore

    # Redirect to the PDF file link
    return HttpResponseRedirect(pdf_link)


@login_required
@user_passes_test(vertrieb_check)
def pdf_angebots_list_view(request):
    user_angebots = VertriebAngebot.objects.all()

    query = request.GET.get("q")
    if query:
        user_angebots = user_angebots.filter(
            Q(zoho_kundennumer__icontains=query)
            | Q(angebot_id__icontains=query)
            | Q(status__icontains=query)
            | Q(name__icontains=query)
            | Q(anfrage_vom__icontains=query)
        )

    angebots_and_files = []

    for angebot in user_angebots:
        user = angebot.user
        angebot_path = os.path.join(
            settings.MEDIA_URL,
            f"pdf/usersangebots/{user.username}/",
            f"Angebot_{angebot.angebot_id}.pdf",
        )
        angebots_and_files.append((angebot, angebot_path))

    context = {
        "zipped_angebots": angebots_and_files,
        "angebots": user_angebots,
    }

    return render(request, "vertrieb/pdf_angebot_created.html", context)


class PDFAngebotsListView(LoginRequiredMixin, VertriebCheckMixin, ListView):
    model = VertriebAngebot
    template_name = "vertrieb/pdf_angebot_created.html"
    context_object_name = "angebots"

    def dispatch(self, request, *args, **kwargs):
        angebot_id = self.kwargs.get("angebot_id")
        vertrieb_angebot = get_object_or_404(self.model, angebot_id=angebot_id)
        user = vertrieb_angebot.user
        if not request.user.is_authenticated and self.request.user != user:
            raise PermissionDenied()  # This will use your custom 403.html template
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        angebot_id = self.kwargs.get("angebot_id")
        vertrieb_angebot = get_object_or_404(self.model, angebot_id=angebot_id)
        user = vertrieb_angebot.user

        if self.request.user != user and not self.request.user.is_staff:
            raise Http404()

        user_angebots = self.model.objects.filter(user=user)

        query = self.request.GET.get("q")
        if query:
            user_angebots = user_angebots.filter(
                Q(zoho_kundennumer__icontains=query)
                | Q(angebot_id__icontains=query)
                | Q(status__icontains=query)
                | Q(name__icontains=query)
                | Q(anfrage_vom__icontains=query)
            )

        angebot_path = os.path.join(
            settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/"
        )

        angebot_files = [
            os.path.join(angebot_path, f"Angebot_{angebot.angebot_id}.pdf")
            for angebot in user_angebots
        ]

        self.extra_context = {
            "user": user,
            "zipped_angebots": zip(user_angebots, angebot_files),
        }

        return user_angebots


# @user_passes_test(vertrieb_check)
# def PDFAngebotsListView(request, angebot_id):
#     vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
#     user = vertrieb_angebot.user
#     if request.user != vertrieb_angebot.user and not request.user.is_staff:
#         return page_not_found(request, Exception())
#     user_angebots = VertriebAngebot.objects.filter(user=user)

#     # Create a list of invoice file paths
#     angebot_path = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/")  # type: ignore

#     angebot_files = [
#         os.path.join(angebot_path, f"Angebot_{vertrieb_angebot.angebot_id}.pdf")
#         for angebot in user_angebots
#     ]

#     # Zip the two lists together
#     zipped_angebots = zip(user_angebots, angebot_files)

#     return render(
#         request,
#         "vertrieb/pdf_angebot_created.html",
#         {
#             "user": user,
#             "zipped_angebots": zipped_angebots,
#         },
#     )


@user_passes_test(vertrieb_check)
def PDFCalculationsListView(request, angebot_id):
    vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
    user = vertrieb_angebot.user
    if request.user != vertrieb_angebot.user and not request.user.is_staff:
        return page_not_found(request, Exception())
    user_angebots = VertriebAngebot.objects.filter(user=user)

    # Create a list of calculation file paths
    calc_path = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Kalkulationen/")  # type: ignore

    calc_files = [
        os.path.join(calc_path, f"Kalkulation_{vertrieb_angebot.angebot_id}.pdf")
        for angebot in user_angebots
    ]

    # Zip the two lists together
    zipped_calculations = zip(user_angebots, calc_files)

    return render(
        request,
        "vertrieb/pdf_calculations_created.html",
        {
            "user": user,
            "zipped_calculations": zipped_calculations,
        },
    )


@user_passes_test(vertrieb_check)
def PDFTicketListView(request, angebot_id):
    vertrieb_angebot = get_object_or_404(VertriebAngebot, angebot_id=angebot_id)
    user = vertrieb_angebot.user
    if request.user != vertrieb_angebot.user and not request.user.is_staff:
        return page_not_found(request, Exception())
    user_angebots = VertriebAngebot.objects.filter(user=user)

    # Create a list of ticket file paths
    ticket_path = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Tickets/")  # type: ignore

    ticket_files = [
        os.path.join(ticket_path, f"Ticket_{vertrieb_angebot.angebot_id}.pdf")
        for angebot in user_angebots
    ]

    # Zip the two lists together
    zipped_tickets = zip(user_angebots, ticket_files)

    return render(
        request,
        "vertrieb/pdf_ticket_created.html",
        {
            "user": user,
            "zipped_tickets": zipped_tickets,
        },
    )


# def get_names(data):
#     env_file = find_dotenv()
#     names = tuple((item['name'], item['name']) for item in data)

#     set_key(env_file, "NAMES_CHOICES", str(names))
#     return
