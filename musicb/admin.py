from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
