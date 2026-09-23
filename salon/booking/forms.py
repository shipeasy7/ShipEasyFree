from datetime import datetime

from django import forms
from django.forms import modelformset_factory
from django.utils import timezone

from .availability import is_slot_free
from .models import Appointment, Client, OpeningHours, Service, Stylist, normalize_phone


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class AppointmentForm(forms.ModelForm):
    client_phone = forms.CharField(label="Client WhatsApp number", help_text="With country code, e.g. 919812345678")
    client_name = forms.CharField(label="Client name", required=False)
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)
    notify = forms.BooleanField(
        label="Send WhatsApp confirmation", required=False, initial=True
    )

    class Meta:
        model = Appointment
        fields = ["service", "stylist", "notes", "status"]

    field_order = ["client_phone", "client_name", "service", "stylist", "date", "time", "notes", "status", "notify"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(active=True)
        self.fields["stylist"].queryset = Stylist.objects.filter(active=True)
        self.fields["stylist"].empty_label = "Any available stylist"
        if self.instance.pk:
            local = timezone.localtime(self.instance.start)
            self.initial.update(
                client_phone=self.instance.client.phone,
                client_name=self.instance.client.name,
                date=local.date(),
                time=local.time(),
            )
            self.fields["notify"].initial = False
            self.fields["notify"].label = "Send WhatsApp confirmation of the changes"
        else:
            del self.fields["status"]

    def clean_client_phone(self):
        phone = normalize_phone(self.cleaned_data["client_phone"])
        if len(phone) < 8:
            raise forms.ValidationError("Enter the full number including country code.")
        return phone

    def clean(self):
        data = super().clean()
        service, day, time = data.get("service"), data.get("date"), data.get("time")
        if not (service and day and time):
            return data
        start = timezone.make_aware(datetime.combine(day, time))
        self.instance.start = start
        self.instance.service = service
        if not data.get("stylist"):
            free = [
                s for s in Stylist.objects.filter(active=True, services=service)
                if is_slot_free(service, start, s, exclude_pk=self.instance.pk)
            ]
            if not free:
                raise forms.ValidationError("No stylist offering this service is free at that time.")
            data["stylist"] = free[0]
        return data

    def save(self, commit=True):
        client, _ = Client.objects.get_or_create(phone=self.cleaned_data["client_phone"])
        name = self.cleaned_data.get("client_name")
        if name and name != client.name:
            client.name = name
            client.save(update_fields=["name"])
        self.instance.client = client
        return super().save(commit)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone", "notes"]

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data["phone"])
        if Client.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A client with this number already exists.")
        return phone


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "duration_minutes", "price", "active"]


class StylistForm(forms.ModelForm):
    class Meta:
        model = Stylist
        fields = ["name", "phone", "services", "active"]
        widgets = {"services": forms.CheckboxSelectMultiple}


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["weekday", "opens", "closes", "closed"]
        widgets = {"weekday": forms.HiddenInput, "opens": TimeInput, "closes": TimeInput}


OpeningHoursFormSet = modelformset_factory(OpeningHours, form=OpeningHoursForm, extra=0)


class ReplyForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Type a WhatsApp reply…"}))
