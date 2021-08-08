from django.views import View
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.conf import settings
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy

# from .decorators import check_recaptcha
# from .models import *
from .forms import *

# from MyProject1.local_settings import weather_api_key, google_maps_api_key
import requests

import json
import urllib

# Create your views here.

weather_api_key = os.environ.get("weather_api_key")
google_maps_api_key = os.environ.get("google_maps_api_key")
recaptcha_key = os.environ.get("GOOGLE_RECAPTCHA_SECRET_KEY")
recaptcha_site_key = os.environ.get("RECAPTCHA_SITE_KEY")


class AirportsAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Airports.objects.all().order_by("country", "city")
        if self.q:
            qs = qs.filter(city__icontains=self.q) or qs.filter(
                country__icontains=self.q
            )
        return qs


class MainView(View):
    def get(self, request):
        form = RouteSearchForm
        return render(request, "index.html", {"form": form})

    def post(self, request):
        form = RouteSearchForm(request.POST)
        if "check_trip" in request.POST and form.is_valid():
            # location data
            departure = form.cleaned_data["departure"]
            arrival = form.cleaned_data["arrival"]
            departure_result = Airports.objects.get(pk=departure.id)
            arrival_result = Airports.objects.get(pk=arrival.id)

            # current weather api implementation
            d_api_response = requests.get(
                "http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s"
                % (departure_result.city, weather_api_key)
            )
            a_api_response = requests.get(
                "http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s"
                % (arrival_result.city, weather_api_key)
            )
            d_curr_weather = d_api_response.json()
            a_curr_weather = a_api_response.json()

            # google maps embed api implementation
            a_map_api_key = google_maps_api_key

            ctx = {
                "form": form,
                "d_result": departure_result,
                "a_result": arrival_result,
                "d_weather_ico": d_curr_weather["weather"][0]["icon"],
                "d_weather": (d_curr_weather["weather"][0]["description"]).capitalize(),
                "d_weather_temp": d_curr_weather["main"]["temp"],
                "d_weather_temp_min": d_curr_weather["main"]["temp_min"],
                "d_weather_temp_max": d_curr_weather["main"]["temp_max"],
                "d_weather_wind": d_curr_weather["wind"]["speed"],
                "d_weather_clouds": d_curr_weather["clouds"]["all"],
                "d_weather_pressure": d_curr_weather["main"]["pressure"],
                "a_weather_ico": a_curr_weather["weather"][0]["icon"],
                "a_weather": (a_curr_weather["weather"][0]["description"]).capitalize(),
                "a_weather_temp": a_curr_weather["main"]["temp"],
                "a_weather_temp_min": a_curr_weather["main"]["temp_min"],
                "a_weather_temp_max": a_curr_weather["main"]["temp_max"],
                "a_weather_wind": a_curr_weather["wind"]["speed"],
                "a_weather_clouds": a_curr_weather["clouds"]["all"],
                "a_weather_pressure": a_curr_weather["main"]["pressure"],
                "a_map_api_key": a_map_api_key,
            }
            return render(request, "index.html", ctx)
        if "save_trip" in request.POST and form.is_valid():
            departure = form.cleaned_data["departure"]
            arrival = form.cleaned_data["arrival"]
            origin = Airports.objects.get(pk=departure.id)
            destination = Airports.objects.get(pk=arrival.id)
            new_trip = Trip.objects.create(
                origin=origin, destination=destination, user=request.user
            )
            new_trip.save()
            return redirect("trips-list")


class SignUpView(View):
    def get(self, request):
        form = SignUpForm
        data_site_key = recaptcha_site_key
        return render(
            request, "signup.html", {"form": form, "data_site_key": data_site_key}
        )

    def post(self, request):
        form = SignUpForm(request.POST)
        data_site_key = recaptcha_site_key
        if form.is_valid():

            """Begin reCAPTCHA validation"""
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {"secret": recaptcha_key, "response": recaptcha_response}
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ End reCAPTCHA validation """

            if result["success"]:
                form.save()
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request,
                    "Your account has been created. You are now able to log in.",
                )
                return redirect("index")
            else:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
                return render(
                    request,
                    "signup.html",
                    {"form": form, "data_site_key": data_site_key},
                )
        else:
            form = SignUpForm()
            messages.error(request, "Incomplete or invalid data provided")
        return render(request, "signup.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        data_site_key = recaptcha_site_key
        return render(
            request, "login.html", {"form": form, "data_site_key": data_site_key}
        )

    def post(self, request):
        form = LoginForm(request.POST)
        data_site_key = recaptcha_site_key
        if form.is_valid():

            """Begin reCAPTCHA validation"""
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {"secret": recaptcha_key, "response": recaptcha_response}
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ End reCAPTCHA validation """

            user = authenticate(**form.cleaned_data)
            if user is not None and user.is_active and result["success"]:
                login(request, user)
            elif not result["success"]:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
                return render(
                    request,
                    "login.html",
                    {"form": form, "data_site_key": data_site_key},
                )
        return redirect("index")


class DeleteUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = DeleteUserForm()
        return render(request, "delete_user.html", {"form": form})

    def post(self, request):
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            success = request.user.check_password(request.POST["password"])
            if success:
                User.objects.get(username=request.user.username).delete()
                messages.success(request, "Deleted.")
                return redirect("index")
            else:
                return redirect("delete-account")


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("index")


class AddItem(LoginRequiredMixin, CreateView):
    model = Item
    fields = ["name"]
    template_name = "add_item.html"
    success_url = "/items_list"
    # login_url = '/login/'
    redirect_field_name = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy("items-list")
    # login_url = '/login/'
    redirect_field_name = "login"


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("items-list")
    # login_url = '/login/'
    redirect_field_name = "login"


class ItemsList(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            items = Item.objects.filter(user=request.user)
            ctx = {
                "items": items,
            }
            return render(request, "items_list.html", ctx)
        else:
            return redirect("login")


class AddItemToTrip(LoginRequiredMixin, View):
    def get(self, request, trip_id):
        form = AddItemToTripForm
        trip = Trip.objects.get(pk=trip_id)
        ctx = {
            "form": form,
            "trip": trip,
        }
        return render(request, "add_item_to_trip.html", ctx)

    def post(self, request, trip_id):
        form = AddItemToTripForm(request.POST)
        if "pack" and form.is_valid():
            item = form.cleaned_data["item"]
            quantity = form.cleaned_data["quantity"]
            packed = form.cleaned_data["packed"]
            trip = Trip.objects.get(pk=trip_id)
            ItemTrip.objects.create(
                quantity=quantity, packed=packed, item=item, trip=trip
            )
            ctx = {
                "form": form,
                "trip": trip,
            }
            return render(request, "add_item_to_trip.html", ctx)


class TripItemsList(LoginRequiredMixin, View):
    def get(self, request, trip_id):
        if request.user.is_authenticated:
            trips = Trip.objects.get(pk=trip_id, user=request.user)
            items = ItemTrip.objects.filter(trip=trip_id)
            ctx = {
                "items": items,
                "trips": trips,
            }
            return render(request, "trip_items_list.html", ctx)
        else:
            return redirect("login")


class ItemToTripDelete(LoginRequiredMixin, DeleteView):
    model = ItemTrip
    # login_url = '/login/'
    redirect_field_name = "login"

    def get_success_url(self):
        return reverse_lazy("trip-items-list", kwargs={"trip_id": self.object.trip.pk})


class ItemToTripUpdate(LoginRequiredMixin, UpdateView):
    model = ItemTrip
    fields = ["item", "quantity", "packed"]
    template_name = "item_to_trip_update_form.html"
    # login_url = '/login/'
    redirect_field_name = "login"

    def get_success_url(self):
        return reverse_lazy("trip-items-list", kwargs={"trip_id": self.object.trip.pk})


class TripsList(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            trips = Trip.objects.filter(user=request.user)
            return render(request, "trips_list.html", {"trips": trips})
        else:
            return redirect("login")


class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    success_url = reverse_lazy("trips-list")
    # login_url = '/login/'
    redirect_field_name = "login"


class TripUpdate(LoginRequiredMixin, UpdateView):
    form_class = RouteSearchForm
    queryset = Trip.objects.all()
    template_name_suffix = "_update_form"
    success_url = "/trips_list"
    # login_url = '/login/'
    redirect_field_name = "login"


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            user_data = UserProfile.objects.get(user=request.user)
            return render(request, "profile.html", {"user_data": user_data})
        # else:
        #     return redirect('login')


class UserProfileUpdate(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            data_update = UserUpdateForm(instance=request.user)
            img_update = UserProfileUpdateForm(instance=request.user.userprofile)
            ctx = {
                "data_update": data_update,
                "img_update": img_update,
            }
            return render(request, "profile_update.html", ctx)

    def post(self, request):
        data_update = UserUpdateForm(request.POST, instance=request.user)
        img_update = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if data_update.is_valid() and img_update.is_valid():
            data_update.save()
            img_update.save()
            messages.success(request, "Your account has been updated.")
            return redirect("profile")


class ActivitiesList(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            activities = ToDoList.objects.filter(user=request.user)
            ctx = {
                "activities": activities,
            }
            return render(request, "activities_list.html", ctx)
        else:
            return redirect("login")


class AddActivity(CreateView, LoginRequiredMixin):
    model = ToDoList
    fields = ["activity"]
    template_name = "add_activity.html"
    success_url = "/activities_list"
    # login_url = '/login/'
    redirect_field_name = "login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddActivity, self).form_valid(form)


class ActivityDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    success_url = reverse_lazy("activities-list")
    # login_url = '/login/'
    redirect_field_name = "login"


class ActivityUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoList
    fields = ["activity"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("activities-list")
    # login_url = '/login/'
    redirect_field_name = "login"


class AddActivityToTrip(LoginRequiredMixin, View):
    def get(self, request, trip_id):
        form = AddActivityToTripForm(user=request.user)
        trip = Trip.objects.get(pk=trip_id)
        ctx = {
            "form": form,
            "trip": trip,
        }
        return render(request, "add_activity_trip.html", ctx)

    def post(self, request, trip_id):
        form = AddActivityToTripForm(request.user, request.POST)
        if form.is_valid():
            activity = form.cleaned_data["activity"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            done = form.cleaned_data["done"]
            trip = Trip.objects.get(pk=trip_id)
            PlanTrip.objects.create(
                activity=activity, date=date, time=time, done=done, trip=trip
            )
            ctx = {
                "form": form,
                "trip": trip,
            }
            return render(request, "add_activity_trip.html", ctx)

    def get_from_kwargs(self):
        kwargs = super(AddActivityToTrip, self).get_from_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class TripActivitiesList(LoginRequiredMixin, View):
    def get(self, request, trip_id):
        if request.user.is_authenticated:
            trips = Trip.objects.get(pk=trip_id, user=request.user)
            activities = PlanTrip.objects.filter(trip=trip_id).order_by("date", "time")
            ctx = {
                "activities": activities,
                "trips": trips,
            }
            return render(request, "trip_activities_list.html", ctx)
        else:
            return redirect("login")


class ActivityToTripDelete(LoginRequiredMixin, DeleteView):
    model = PlanTrip
    # login_url = '/login/'
    redirect_field_name = "login"

    def get_success_url(self):
        return reverse_lazy(
            "trip-activities-list", kwargs={"trip_id": self.object.trip.pk}
        )


class ActivityToTripUpdate(LoginRequiredMixin, UpdateView):
    model = PlanTrip
    form_class = ActivityToTripUpdateForm
    template_name = "activity_to_trip_update_form.html"
    # login_url = '/login/'
    redirect_field_name = "login"

    def get_success_url(self):
        return reverse_lazy(
            "trip-activities-list", kwargs={"trip_id": self.object.trip.pk}
        )


class UserImgGalleryView(LoginRequiredMixin, FormView):
    form_class = AddPictureToGalleryForm
    template_name = "user_img_gallery.html"
    success_url = "/img_gallery/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            images = ImgGallery.objects.filter(user=request.user).order_by("-pk")
            add_image = AddPictureToGalleryForm(instance=request.user)
            ctx = {
                "images": images,
                "add_image": add_image,
            }
            return render(request, "user_img_gallery.html", ctx)
        else:
            return redirect("login")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        pictures = request.FILES.getlist("picture")
        if "upload_pics" and form.is_valid():
            for pic in pictures:
                ImgGallery.objects.create(user=request.user, picture=pic)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeletePicsFromGalleryView(LoginRequiredMixin, DeleteView):
    model = ImgGallery
    template_name = "imggallery_confirm_delete.html"
    context_object_name = "picture"
    success_url = "/img_gallery/"


class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm()
        data_site_key = recaptcha_site_key
        return render(
            request, "contact_us.html", {"form": form, "data_site_key": data_site_key}
        )

    def post(self, request):
        form = ContactUsForm(request.POST)
        data_site_key = recaptcha_site_key
        if form.is_valid():
            from_email = form.cleaned_data["from_email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            """ Begin reCAPTCHA validation """
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {"secret": recaptcha_key, "response": recaptcha_response}
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ End reCAPTCHA validation """

            if result["success"]:
                try:
                    msg = EmailMessage(
                        subject,
                        "From: " + from_email + "\n\n" + message,
                        from_email,
                        [settings.EMAIL_HOST_USER],
                    )
                    msg.send()
                except BadHeaderError:
                    return HttpResponse("Error. Invalid header")
                return redirect("contact-us-success")
            else:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
                return render(
                    request,
                    "contact_us.html",
                    {"form": form, "data_site_key": data_site_key},
                )


class ContactUsSuccessView(View):
    def get(self, request):
        return render(request, "contact_us_success.html")
