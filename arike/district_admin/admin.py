from django.contrib import admin
from .models import State, District, LocalBody, Ward, Facility


admin.site.register(State)
admin.site.register(District)
admin.site.register(LocalBody)
admin.site.register(Ward)
admin.site.register(Facility)
