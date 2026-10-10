
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q

from .models import Harvest, ChatMessage, Farmer, Buyer

User = get_user_model()


# HOME
def home(request):
    return render(request, "index.html")


# REGISTER
def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([full_name, username, email, password, confirm_password]):
            messages.error(request, "Please fill in all fields.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return render(request, "register.html")

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
            )
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Smart Harvest.")
            return redirect("dashboard")
        except Exception:
            messages.error(request, "Registration failed. Please try again.")
            return render(request, "register.html")

    return render(request, "register.html")


# LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please enter your username and password.")
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.POST.get("next") or request.GET.get("next")

                if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)

                messages.success(request, "Login successful!")
                return redirect("dashboard")

            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# LOGOUT
@login_required(login_url="login")
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("index")


# DASHBOARD
@login_required(login_url="login")
def dashboard(request):
    user_harvests = Harvest.objects.filter(farmer=request.user)

    context = {
        "recent_harvests": user_harvests[:5],
        "total_harvest": user_harvests.count(),
        "total_farmers": Farmer.objects.count(),
        "total_buyers": Buyer.objects.count(),
    }
    return render(request, "dashboard.html", context)


# HARVEST
@login_required(login_url="login")
def harvest(request):
    harvest_list = Harvest.objects.filter(farmer=request.user)
    return render(request, "harvest.html", {"harvests": harvest_list})


# IRRIGATION
@login_required(login_url="login")
def irrigation(request):
    return render(request, "irrigation.html")


# WEATHER
@login_required(login_url="login")
def weather(request):
    return render(request, "weather.html")


# WATER MANAGEMENT
@login_required(login_url="login")
def water_management(request):
    return render(request, "water_management.html")


# STORAGE
@login_required(login_url="login")
def storage(request):
    return render(request, "storage.html")


# ANALYTICS
@login_required(login_url="login")
def analytics(request):
    return render(request, "analytics.html")


# FARMERS
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def farmers(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        location = request.POST.get("location", "").strip()
        main_crop = request.POST.get("main_crop", "").strip()

        if not name or not phone or not location:
            messages.error(
                request,
                "Please fill in Full Name, Phone Number and Farm Location."
            )
            return redirect("farmers")

        if email and Farmer.objects.filter(email__iexact=email).exists():
            messages.error(request, "A farmer with this email already exists.")
            return redirect("farmers")

        # Do not automatically link an account based only on email.
        Farmer.objects.create(
            name=name,
            email=email,
            phone=phone,
            location=location,
            main_crop=main_crop,
            created_by=request.user,
        )

        messages.success(request, "Farmer registered successfully!")
        return redirect("farmers")

    farmer_list = Farmer.objects.select_related("user", "created_by").all()

    # All active registered users except the currently logged-in user.
    chat_users = User.objects.filter(is_active=True).exclude(
        pk=request.user.pk
    ).order_by("username")

    return render(
        request,
        "farmers.html",
        {
            "farmers": farmer_list,
            "chat_users": chat_users,
        },
    )


# BUYERS
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def buyers(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        location = request.POST.get("location", "").strip()
        interested_product = request.POST.get("interested_product", "").strip().lower()
        notes = request.POST.get("notes", "").strip()

        allowed_products = {
            "rice", "vegetables", "fruits", "potatoes", "other", ""
        }

        if not name or not phone:
            messages.error(request, "Please enter Buyer Name and Phone Number.")
            return redirect("buyers")

        if interested_product not in allowed_products:
            messages.error(request, "Please select a valid interested product.")
            return redirect("buyers")

        Buyer.objects.create(
            name=name,
            email=email,
            phone=phone,
            location=location,
            interested_product=interested_product,
            notes=notes,
            created_by=request.user,
        )

        messages.success(request, "Buyer registered successfully!")
        return redirect("buyers")

    return render(request, "buyers.html", {"buyers": Buyer.objects.all()})


# SETTINGS
@login_required(login_url="login")
def settings_page(request):
    return render(request, "settings.html")


# DASHBOARD API
@login_required(login_url="login")
@require_GET
def live_dashboard_api(request):
    return JsonResponse({
        "total_harvest": 1250,
        "water_used": 3450,
        "active_crops": 8,
        "storage_kg": 680,
        "temperature": 29,
        "humidity": 68,
        "wind": 12,
        "soil_moisture": 64,
    })


# DIRECT CHAT
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def direct_chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id, is_active=True)

    if other_user.pk == request.user.pk:
        messages.error(request, "You cannot chat with yourself.")
        return redirect("farmers")

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()

        if not message_text:
            messages.error(request, "Please enter a message.")
        elif len(message_text) > 5000:
            messages.error(request, "Message cannot exceed 5000 characters.")
        else:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message_text,
            )

        return redirect("direct_chat", user_id=other_user.pk)

    chat_messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user)
        | Q(sender=other_user, receiver=request.user)
    ).select_related("sender", "receiver").order_by("created_at")

    ChatMessage.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False,
    ).update(is_read=True)

    return render(
        request,
        "chat.html",
        {
            "other_user": other_user,
            "chat_messages": chat_messages,
        },
    )
@login_required
def direct_chat(request, user_id):
    other_user = get_object_or_404(
        User,
        pk=user_id,
        is_active=True
    )

    if other_user.pk == request.user.pk:
        messages.error(request, "You cannot chat with yourself.")
        return redirect("farmers")

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()

        if message_text and len(message_text) <= 5000:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message_text
            )
        elif not message_text:
            messages.error(request, "Please enter a message.")
        else:
            messages.error(request, "Message must be under 5000 characters.")

        return redirect("direct_chat", user_id=other_user.pk)

    chat_messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user)
        | Q(sender=other_user, receiver=request.user)
    ).select_related("sender", "receiver").order_by("created_at")

    ChatMessage.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, "chat.html", {
        "other_user": other_user,
        "chat_messages": chat_messages,
    })