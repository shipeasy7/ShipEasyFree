from datetime import date, datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from whatsapp import client as wa
from whatsapp import notifications
from whatsapp.models import Conversation, Message

from .availability import available_slots
from .forms import (
    AppointmentForm,
    ClientForm,
    OpeningHoursFormSet,
    ReplyForm,
    ServiceForm,
    StylistForm,
)
from .models import Appointment, Client, OpeningHours, Service, Stylist


def _day_bounds(day):
    tz = timezone.get_current_timezone()
    start = timezone.make_aware(datetime.combine(day, time.min), tz)
    return start, start + timedelta(days=1)


@login_required
def dashboard(request):
    today = timezone.localdate()
    start, end = _day_bounds(today)
    todays = Appointment.objects.filter(start__gte=start, start__lt=end).select_related(
        "client", "service", "stylist"
    )
    active_today = [a for a in todays if a.status != Appointment.CANCELLED]
    week_end = start + timedelta(days=7)
    context = {
        "today": today,
        "appointments": todays,
        "stats": {
            "today": len(active_today),
            "revenue": sum(a.service.price for a in active_today),
            "week": Appointment.objects.filter(
                start__gte=start, start__lt=week_end, status__in=Appointment.ACTIVE_STATUSES
            ).count(),
            "whatsapp_week": Appointment.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7), source=Appointment.SOURCE_WHATSAPP
            ).count(),
        },
        "waiting": Conversation.objects.filter(needs_staff=True).select_related("client"),
    }
    return render(request, "booking/dashboard.html", context)


# --- Appointments ----------------------------------------------------------------

@login_required
def appointment_list(request):
    try:
        day = date.fromisoformat(request.GET.get("date", ""))
    except ValueError:
        day = timezone.localdate()
    start, end = _day_bounds(day)
    appointments = Appointment.objects.filter(start__gte=start, start__lt=end).select_related(
        "client", "service", "stylist"
    )
    stylist_id = request.GET.get("stylist")
    if stylist_id:
        appointments = appointments.filter(stylist_id=stylist_id)
    return render(
        request,
        "booking/appointment_list.html",
        {
            "day": day,
            "prev_day": day - timedelta(days=1),
            "next_day": day + timedelta(days=1),
            "appointments": appointments,
            "stylists": Stylist.objects.filter(active=True),
            "stylist_id": stylist_id,
        },
    )


@login_required
def appointment_form(request, pk=None):
    appt = get_object_or_404(Appointment, pk=pk) if pk else None
    initial = {}
    if appt is None:
        initial = {k: request.GET[k] for k in ("client_phone", "client_name", "date") if k in request.GET}
    form = AppointmentForm(request.POST or None, instance=appt, initial=initial)
    if request.method == "POST" and form.is_valid():
        appt = form.save()
        if form.cleaned_data.get("notify"):
            if appt.status == Appointment.CANCELLED:
                notifications.send_cancellation(appt)
            else:
                notifications.send_confirmation(appt)
        messages.success(request, f"Saved appointment for {appt.client}.")
        return redirect(f"{reverse('appointment_list')}?date={timezone.localtime(appt.start).date().isoformat()}")
    return render(request, "booking/appointment_form.html", {"form": form, "appointment": appt})


@login_required
@require_POST
def appointment_status(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    status = request.POST.get("status")
    if status in dict(Appointment.STATUSES):
        appt.status = status
        appt.save(update_fields=["status"])
        if status == Appointment.CANCELLED and request.POST.get("notify"):
            notifications.send_cancellation(appt)
        messages.success(request, f"Marked {appt.client} as {appt.get_status_display().lower()}.")
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("appointment_list")


@login_required
def slots_api(request):
    service = get_object_or_404(Service, pk=request.GET.get("service"))
    stylist = Stylist.objects.filter(pk=request.GET.get("stylist") or None).first()
    try:
        day = date.fromisoformat(request.GET.get("date", ""))
    except ValueError:
        return JsonResponse({"slots": []})
    slots = [
        {"time": timezone.localtime(start).strftime("%H:%M"), "stylist": s.name, "stylist_id": s.pk}
        for start, s in available_slots(service, day, stylist)
    ]
    return JsonResponse({"slots": slots})


# --- Clients -----------------------------------------------------------------------

@login_required
def client_list(request):
    q = request.GET.get("q", "").strip()
    clients = Client.objects.annotate(visits=Count("appointments"), last_visit=Max("appointments__start"))
    if q:
        clients = clients.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    return render(request, "booking/client_list.html", {"clients": clients, "q": q})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(
        request,
        "booking/client_detail.html",
        {
            "client": client,
            "appointments": client.appointments.select_related("service", "stylist").order_by("-start"),
        },
    )


@login_required
def client_form(request, pk=None):
    client = get_object_or_404(Client, pk=pk) if pk else None
    form = ClientForm(request.POST or None, instance=client)
    if request.method == "POST" and form.is_valid():
        client = form.save()
        messages.success(request, f"Saved {client}.")
        return redirect("client_detail", pk=client.pk)
    return render(request, "booking/simple_form.html", {"form": form, "title": "Client"})


# --- Catalogue ------------------------------------------------------------------------

@login_required
def service_list(request):
    return render(request, "booking/service_list.html", {"services": Service.objects.prefetch_related("stylists")})


@login_required
def service_form(request, pk=None):
    service = get_object_or_404(Service, pk=pk) if pk else None
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Service saved.")
        return redirect("service_list")
    return render(request, "booking/simple_form.html", {"form": form, "title": "Service"})


@login_required
def stylist_list(request):
    return render(request, "booking/stylist_list.html", {"stylists": Stylist.objects.prefetch_related("services")})


@login_required
def stylist_form(request, pk=None):
    stylist = get_object_or_404(Stylist, pk=pk) if pk else None
    form = StylistForm(request.POST or None, instance=stylist)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Stylist saved.")
        return redirect("stylist_list")
    return render(request, "booking/simple_form.html", {"form": form, "title": "Stylist"})


@login_required
def opening_hours(request):
    for weekday, _ in OpeningHours.WEEKDAYS:
        OpeningHours.objects.get_or_create(weekday=weekday, defaults={"closed": True})
    formset = OpeningHoursFormSet(request.POST or None, queryset=OpeningHours.objects.all())
    if request.method == "POST" and formset.is_valid():
        formset.save()
        messages.success(request, "Opening hours saved.")
        return redirect("opening_hours")
    return render(request, "booking/opening_hours.html", {"formset": formset})


# --- WhatsApp inbox ---------------------------------------------------------------

@login_required
def inbox(request):
    clients = (
        Client.objects.filter(messages__isnull=False)
        .annotate(
            last_message_at=Max("messages__created_at"),
            unread=Count(
                "messages",
                filter=Q(messages__direction=Message.INBOUND, messages__read_by_staff=False),
            ),
        )
        .select_related("conversation")
        .order_by("-last_message_at")
    )
    return render(request, "booking/inbox.html", {"clients": clients})


@login_required
def chat(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ReplyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        msg = wa.send_text(client, form.cleaned_data["body"], sent_by_staff=True)
        if msg.status == "failed":
            messages.error(request, "WhatsApp rejected the message. Check the API settings or the 24h window.")
        return redirect("chat", pk=client.pk)
    client.messages.filter(direction=Message.INBOUND, read_by_staff=False).update(read_by_staff=True)
    conversation, _ = Conversation.objects.get_or_create(client=client)
    return render(
        request,
        "booking/chat.html",
        {
            "client": client,
            "chat_messages": client.messages.all(),
            "conversation": conversation,
            "form": form,
            "window_open": conversation.last_inbound_at
            and timezone.now() - conversation.last_inbound_at < timedelta(hours=24),
        },
    )


@login_required
def chat_messages(request, pk):
    """Message list fragment, polled by the chat page for new messages."""
    client = get_object_or_404(Client, pk=pk)
    client.messages.filter(direction=Message.INBOUND, read_by_staff=False).update(read_by_staff=True)
    return render(request, "booking/_messages.html", {"chat_messages": client.messages.all()})


@login_required
@require_POST
def chat_handover(request, pk):
    conversation, _ = Conversation.objects.get_or_create(client_id=pk)
    conversation.needs_staff = request.POST.get("needs_staff") == "1"
    conversation.reset()
    conversation.save()
    return redirect("chat", pk=pk)
