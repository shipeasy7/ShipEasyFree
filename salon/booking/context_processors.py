from django.conf import settings


def salon(request):
    number = settings.WHATSAPP_PUBLIC_NUMBER
    return {
        "SALON_NAME": settings.SALON_NAME,
        "SALON_CURRENCY": settings.SALON_CURRENCY,
        "WHATSAPP_LINK": f"https://wa.me/{number}?text=Hi" if number else "",
        "WHATSAPP_LIVE": bool(settings.WHATSAPP_TOKEN and settings.WHATSAPP_PHONE_NUMBER_ID),
    }


def inbox(request):
    if not request.user.is_authenticated:
        return {}
    from whatsapp.models import Conversation, Message

    unread = Message.objects.filter(direction=Message.INBOUND, read_by_staff=False).values_list("client", flat=True)
    waiting = Conversation.objects.filter(needs_staff=True).values_list("client", flat=True)
    # Number of chats that need a look from staff.
    return {"INBOX_ATTENTION": len(set(unread) | set(waiting))}
