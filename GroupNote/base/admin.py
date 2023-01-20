from django.contrib import admin
from .models import Room, Message, Note, Tag, User

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Note)
admin.site.register(Tag)
