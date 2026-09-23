import re
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def normalize_phone(value):
    """Store phones as digits with country code, the format WhatsApp uses (e.g. 919812345678)."""
    return re.sub(r"\D", "", value or "")


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def duration(self):
        return timedelta(minutes=self.duration_minutes)


class Stylist(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    services = models.ManyToManyField(Service, related_name="stylists", blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OpeningHours(models.Model):
    WEEKDAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAYS, unique=True)
    opens = models.TimeField(null=True, blank=True)
    closes = models.TimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ["weekday"]
        verbose_name_plural = "opening hours"

    def __str__(self):
        if self.closed or not (self.opens and self.closes):
            return f"{self.get_weekday_display()}: closed"
        return f"{self.get_weekday_display()}: {self.opens:%H:%M}–{self.closes:%H:%M}"

    def clean(self):
        if not self.closed and (not self.opens or not self.closes or self.opens >= self.closes):
            raise ValidationError("Set an opening time before the closing time, or mark the day closed.")


class Client(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, unique=True, help_text="With country code, e.g. 919812345678")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "phone"]

    def __str__(self):
        return self.name or f"+{self.phone}"

    def save(self, *args, **kwargs):
        self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)

    def upcoming_appointments(self):
        return self.appointments.filter(
            start__gte=timezone.now(), status__in=Appointment.ACTIVE_STATUSES
        ).select_related("service", "stylist")


class Appointment(models.Model):
    BOOKED = "booked"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    STATUSES = [
        (BOOKED, "Booked"),
        (CONFIRMED, "Confirmed"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (NO_SHOW, "No-show"),
    ]
    ACTIVE_STATUSES = [BOOKED, CONFIRMED]

    SOURCE_WEB = "web"
    SOURCE_WHATSAPP = "whatsapp"
    SOURCES = [(SOURCE_WEB, "Front desk"), (SOURCE_WHATSAPP, "WhatsApp")]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
    stylist = models.ForeignKey(
        Stylist, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments"
    )
    start = models.DateTimeField()
    end = models.DateTimeField(editable=False)
    status = models.CharField(max_length=20, choices=STATUSES, default=BOOKED)
    source = models.CharField(max_length=20, choices=SOURCES, default=SOURCE_WEB)
    notes = models.CharField(max_length=255, blank=True)
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start"]

    def __str__(self):
        return f"{self.client} – {self.service} @ {timezone.localtime(self.start):%d %b %H:%M}"

    @property
    def is_active(self):
        return self.status in self.ACTIVE_STATUSES

    def save(self, *args, **kwargs):
        self.end = self.start + self.service.duration
        super().save(*args, **kwargs)

    def clean(self):
        if not (self.start and self.service_id):
            return
        end = self.start + self.service.duration
        if self.stylist_id and self.is_active:
            clash = Appointment.objects.filter(
                stylist_id=self.stylist_id,
                status__in=self.ACTIVE_STATUSES,
                start__lt=end,
                end__gt=self.start,
            ).exclude(pk=self.pk)
            if clash.exists():
                raise ValidationError(f"{self.stylist} already has an appointment at that time.")
