from django.contrib import admin
from django.contrib.auth.models import User
from . models import Profile,Tweet
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]
    
admin.site.unregister(User)
admin.site.register(Tweet)
admin.site.register(User,UserAdmin)
