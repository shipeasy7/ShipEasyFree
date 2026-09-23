# Salon software with WhatsApp booking

A web app for running a salon, where clients book, view and cancel appointments
by chatting on **WhatsApp**. Staff use a browser dashboard for the diary, clients,
services, stylists, opening hours and a shared WhatsApp inbox.

Built with Django 5 and the official **WhatsApp Business Cloud API** (Meta). It does
not use unofficial WhatsApp Web automation, which can get numbers banned.

## Features

**For clients, on WhatsApp**
- Say "hi" to get a menu: *Book appointment · My appointments · Services & prices · Talk to the salon*
- Booking uses WhatsApp list and button messages: service → stylist (or "no preference") → day → free time → confirm
- Only real free times are offered, based on opening hours, service length and each stylist's existing bookings
- View upcoming appointments and cancel them
- "Talk to the salon" hands the chat to a person. The bot stays quiet until staff hand it back or the client types *menu*
- Confirmation, cancellation and reminder messages

**For staff, in the browser**
- Today view: schedule, expected takings, WhatsApp bookings, clients waiting for a reply
- Appointment diary by day and stylist; create or edit bookings with a free-slot picker; mark as done, no-show or cancelled (cancelling notifies the client)
- Client list with visit history and notes
- WhatsApp inbox: every conversation, bot and staff messages, live refresh, reply box, "take over" and "hand back to bot"
- Manage services and prices, stylists and the services each offers, and opening hours
- Django admin at `/admin/`

## Quick start

```bash
cd salon
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo      # sample services, stylists, hours, and an admin/admin login
python manage.py runserver
```

Open http://localhost:8000 and log in with `admin` / `admin`. Change that password straight away.

Without WhatsApp credentials the app runs in **dry-run mode**: bot replies are saved
and shown in the inbox, but nothing is sent. You can try the bot by POSTing webhook
payloads to `/whatsapp/webhook/`; see `whatsapp/tests.py` for examples.

Run the tests with `python manage.py test`.

## Connecting WhatsApp

1. At [developers.facebook.com](https://developers.facebook.com/), create an app of type **Business** and add the **WhatsApp** product.
2. Under *WhatsApp → API Setup*, note the **Phone number ID** and create a **permanent access token** (a System User token with `whatsapp_business_messaging`).
3. Deploy the app on a public HTTPS URL.
4. Under *WhatsApp → Configuration → Webhook*, set:
   - Callback URL: `https://your-domain/whatsapp/webhook/`
   - Verify token: the same value as `WHATSAPP_VERIFY_TOKEN`
   - Subscribe to the **messages** field
5. Set the environment variables below and restart.

| Variable | Purpose |
| --- | --- |
| `WHATSAPP_TOKEN` | Cloud API access token |
| `WHATSAPP_PHONE_NUMBER_ID` | Phone number ID to send from |
| `WHATSAPP_VERIFY_TOKEN` | Any secret string, also entered in the Meta webhook settings |
| `WHATSAPP_APP_SECRET` | App secret; when set, webhook signatures are verified (recommended) |
| `WHATSAPP_PUBLIC_NUMBER` | Your WhatsApp number, digits only (e.g. `919812345678`), for the shareable `wa.me` booking link |
| `WHATSAPP_REMINDER_TEMPLATE` | Name of an approved template for reminders (see below) |
| `WHATSAPP_TEMPLATE_LANGUAGE` | Template language code, default `en` |

### Reminders and the 24-hour window

WhatsApp only delivers free-form messages within 24 hours of the client's last
message. Reminders usually fall outside that window, so create a **Utility** message
template in WhatsApp Manager with three body variables, for example:

> Hi {{1}}, this is a reminder of your {{2}} appointment on {{3}}. Reply *menu* to manage it.

Set `WHATSAPP_REMINDER_TEMPLATE` to its name, and run reminders from cron:

```cron
*/15 * * * * cd /path/to/salon && .venv/bin/python manage.py send_reminders
```

Each appointment gets one reminder when it is within `SALON_REMINDER_LEAD_HOURS` (default 24 hours).

## Other settings

| Variable | Default |
| --- | --- |
| `SALON_NAME` | `Glow Salon` |
| `SALON_ADDRESS` | *(empty)* |
| `SALON_CURRENCY` | `₹` |
| `SALON_TIME_ZONE` | `Asia/Kolkata` |
| `SALON_SLOT_INTERVAL_MINUTES` | `30` |
| `SALON_BOOKING_WINDOW_DAYS` | `14` |
| `SALON_REMINDER_LEAD_HOURS` | `24` |
| `DJANGO_SECRET_KEY` | dev key. **Set this in production** |
| `DJANGO_DEBUG` | `true`. Set to `false` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | e.g. `https://your-domain` |
| `SALON_DB_PATH` | `salon/salon.sqlite3` |

## Layout

```
salon/
  booking/     models (Service, Stylist, OpeningHours, Client, Appointment), slot availability, dashboard views
  whatsapp/    Cloud API client, webhook, booking bot, notification messages, inbox models
  templates/   dashboard HTML
  static/      stylesheet
```
