from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from .decorators import check_recaptcha
from TripHelpmate.views import AirportsAutocompleteView, MainView, AddItemToTrip, TripItemsList, SignUpView, LoginView, LogoutView, \
    TripsList, TripDelete, TripUpdate, AddItem, ItemsList, ItemDelete, ItemUpdate, ItemToTripUpdate, ItemToTripDelete, \
    UserProfileView, ActivitiesList, AddActivity, ActivityUpdate, ActivityDelete, TripActivitiesList, AddActivityToTrip,\
    ActivityToTripUpdate, ActivityToTripDelete, UserProfileUpdate, DeleteUserView, UserImgGalleryView, \
    DeletePicsFromGalleryView, ContactUsView, ContactUsSuccessView


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name="password_reset"),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name="password_reset_complete"),
    path('profile/',UserProfileView.as_view(), name='profile'),
    path('update_profile/', UserProfileUpdate.as_view(), name='update-profile'),
    path('delete_account/', DeleteUserView.as_view(), name='delete-account'),
    path('airports-autocomplete/', AirportsAutocompleteView.as_view(), name='airports-autocomplete'),
    path('add_item/', AddItem.as_view(), name='add-item'),
    path('items_list/', ItemsList.as_view(), name='items-list'),
    path('item_confirm_delete/<int:pk>', ItemDelete.as_view(), name='item-delete'),
    path('item_update_form/<int:pk>', ItemUpdate.as_view(), name='item-update'),
    path('add_item_to_trip/<int:trip_id>', AddItemToTrip.as_view(), name='add-item-trip'),
    path('trip_items_list/<int:trip_id>', TripItemsList.as_view(), name='trip-items-list'),
    path('item_to_trip_update_form/<int:pk>', ItemToTripUpdate.as_view(), name='item-to-trip-update'),
    path('itemtrip_confirm_delete/<int:pk>', ItemToTripDelete.as_view(), name='itemtrip-delete'),
    path('trips_list/', TripsList.as_view(), name='trips-list'),
    path('trip_confirm_delete/<int:pk>', TripDelete.as_view(), name='trip-delete'),
    path('trip_update_form/<int:pk>', TripUpdate.as_view(), name='trip-update'),
    path('activities_list/', ActivitiesList.as_view(), name='activities-list'),
    path('add_activity/', AddActivity.as_view(), name='add-activity'),
    path('activity_update_form/<int:pk>', ActivityUpdate.as_view(), name='activity-update'),
    path('activity_confirm_delete/<int:pk>', ActivityDelete.as_view(), name='activity-delete'),
    path('add_activity_to_trip/<int:trip_id>', AddActivityToTrip.as_view(), name='add-activity-trip'),
    path('trip_activities_list/<int:trip_id>', TripActivitiesList.as_view(), name='trip-activities-list'),
    path('activities_to_trip_update_form/<int:pk>', ActivityToTripUpdate.as_view(), name='activities-to-trip-update'),
    path('plantrip_confirm_delete/<int:pk>', ActivityToTripDelete.as_view(), name='activitytrip-delete'),
    path('img_gallery/', UserImgGalleryView.as_view(), name='img-gallery'),
    path('image_delete_confirm/<int:pk>', DeletePicsFromGalleryView.as_view(), name='delete_image'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us'),
    path('contact_us_success/', ContactUsSuccessView.as_view(), name='contact-us-success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
