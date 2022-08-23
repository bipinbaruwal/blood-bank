from django.contrib import admin
from blood.models import Articles,BloodRequest,Stock
# Register your models here.
admin.site.register(Articles)
admin.site.register(BloodRequest)
admin.site.register(Stock)