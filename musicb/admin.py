from django.contrib import admin
from .models import *

# Register your models here.
class MemberInline(admin.StackedInline):
    model = Member
    extra = 4

class AlbumInline(admin.StackedInline):
    model = Album
    extra = 2

class TrackInline(admin.StackedInline):
    model = Track
    extra = 3

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MemberInline, AlbumInline, TrackInline]
    

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
