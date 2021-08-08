from functools import wraps

from django.conf import settings
from django.contrib import messages

import os
import requests

recaptcha_key = os.environ.get("GOOGLE_RECAPTCHA_SECRET_KEY")
recaptcha_site_key = os.environ.get("RECAPTCHA_SITE_KEY")


def check_recaptcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.POST:
            recaptcha_response = request.POST.get("g-recaptcha-response")
            data = {"secret": recaptcha_key, "response": recaptcha_response}
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify", data=data
            )
            result = r.json()
            if result["success"]:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
        return function(request, *args, **kwargs)

    return wrap


# def check_recaptcha(view_func):
#     @wraps(view_func)
#     def _wrapped_view(self, request, *args, **kwargs):
#         request.recaptcha_is_valid = None
#         if self.request.method == 'POST':
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             data = {
#                 'secret': recaptcha_key,
#                 'response': recaptcha_response
#             }
#             r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
#             result = r.json()
#             if result['success']:
#                 request.recaptcha_is_valid = True
#             else:
#                 request.recaptcha_is_valid = False
#                 messages.error(request, 'Invalid reCAPTCHA. Please try again.')
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view
