import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from dal import autocomplete


from .models import *


# class AirportChoiceField(forms.ModelChoiceField):
#
#     def label_from_instance(self, obj):
#         return "%s | %s | %s, %s" % (obj.city, obj.country, obj.iata_code, obj.name)


class RouteSearchForm(forms.ModelForm):
    departure = forms.ModelChoiceField(queryset=Airports.objects.all().order_by('country', 'city'),
                                       widget=autocomplete.ModelSelect2(url='airports-autocomplete',
                                                                                           forward=['city', 'country']))
    arrival = forms.ModelChoiceField(queryset=Airports.objects.all().order_by('country', 'city'),
                                     widget=autocomplete.ModelSelect2(url='airports-autocomplete',
                                                                                       forward=['city', 'country']))

    class Meta:
        model = Airports
        fields = ['departure', 'arrival']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, required=False, help_text='Not required')
    last_name = forms.CharField(max_length=32, required=False, help_text='Not required')
    email = forms.EmailField(max_length=256, required=True, help_text='Required. Enter a valid e-mail address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, label='username')
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label='password')


class AddItemToTripForm(forms.ModelForm):

    class Meta:
        model = ItemTrip
        fields = ['item', 'quantity', 'packed']


class AddActivityToTripForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.date.today())
    time = forms.TimeField(initial='00:00:00')

    class Meta:
        model = PlanTrip
        fields = ['activity', 'date', 'time', 'done']

    def __init__(self, user, *args, **kwargs):
        super(AddActivityToTripForm, self).__init__(*args, **kwargs)
        self.fields['activity'].queryset = ToDoList.objects.filter(user=user)


class ActivityToTripUpdateForm(forms.ModelForm):
    class Meta:
        model = PlanTrip
        fields = ['activity', 'date', 'time', 'done']

    # def __init__(self, user, *args, **kwargs):
    #     super(ActivityToTripUpdateForm, self).__init__(*args, **kwargs)
    #     self.fields['activity'].queryset = ToDoList.objects.filter(user=user)


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32, required=False, help_text='Not required')
    last_name = forms.CharField(max_length=32, required=False, help_text='Not required')
    email = forms.EmailField(max_length=256, required=True, help_text='Required. Enter a valid e-mail address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class DeleteUserForm(forms.Form):
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label='Password')


class AddPictureToGalleryForm(forms.ModelForm):
    picture = forms.ImageField(label='Select pictures to upload:',
                               widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ImgGallery
        fields = ['picture']


class ContactUsForm(forms.Form):
    from_email = forms.EmailField(label="Your e-mail:", required=True)
    subject = forms.CharField(label="Subject:", max_length=128, required=True)
    message = forms.CharField(label="Message:", required=True, widget=forms.Textarea)
