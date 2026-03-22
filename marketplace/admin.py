from django.contrib import admin

from .models import User, Hobby, UserHasHobby, Offering, Trade, Gang

admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(UserHasHobby)
admin.site.register(Offering)
admin.site.register(Trade)
admin.site.register(Gang)
