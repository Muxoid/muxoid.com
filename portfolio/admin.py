from django.contrib import admin
from .models import Command, Note, BlogPost, Directory, File
# Register your models here.


admin.site.register(Command)

admin.site.register(Note)
admin.site.register(BlogPost)
admin.site.register(Directory)
admin.site.register(File)
