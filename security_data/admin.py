from django.contrib import admin
from . models import Want_To_Research, Curfew_And_Instability, Population_Alert, Recognized

# Register your models here.
admin.site.register(Want_To_Research)
admin.site.register(Population_Alert)
admin.site.register(Curfew_And_Instability)
admin.site.register(Recognized)

