from django.contrib import admin

# Register your models here.
from.models import user
admin.site.register(user)
from.models import login
admin.site.register(login)
from.models import caretaker
admin.site.register(caretaker)
from.models import details
admin.site.register(details)
from.models import booking
admin.site.register(booking)
from.models import feedback
admin.site.register(feedback)
from.models import p_details
admin.site.register(p_details)
from.models import adpay
admin.site.register(adpay)
from.models import PasswordReset
admin.site.register(PasswordReset)
from.models import complaint
admin.site.register(complaint)