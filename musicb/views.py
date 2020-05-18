from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from .models import Artist, Member, Album, Song
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.
class IndexView(TemplateView):
    template_name = 'musicb/index.html'

class SearchView(View):
    def post(self, request):
        kword = request.POST['kword']
        artist_list = Artist.objects.filter(name__icontains=kword)
        member_list = Member.objects.filter(name__icontains=kword)
        album_list = Album.objects.filter(title__icontains=kword)
        song_list = Song.objects.filter(title__icontains=kword)
        context = {'artist_list': artist_list, 'member_list': member_list, 'album_list': album_list, 'song_list': song_list}
        return render(request, 'musicb/search_result.html', context)


# def searching(request):
#     stype = request.POST['sfor']
#     target = request.POST['kword']
#     if stype=='artist':
#         try:
#             target_artist = Artist.objects.get(name=target)
#         except(Artist.DoesNotExist):
#             return render(request, 'musicb/index.html', {'error_msg': "No result for " + target})
#         else:
#             print(target_artist.name)
#             return HttpResponseRedirect(reverse('musicblog:artistview_detail', args=(target_artist.slug,)))
#     elif stype=='member':
#         try:
#             target_member = Member.objects.get(name=target)
#         except(Member.DoesNotExist):
#             return render(request, 'musicb/index.html', {'error_msg': "No result for " + target})
#         else:
#             return HttpResponseRedirect(reverse('musicblog:memberview_detail', args=(target_member.slug,)))
#     elif stype=='album':
#         try:
#             target_album = Album.objects.get(title=target)
#         except(Album.DoesNotExist):
#             return render(request, 'musicb/index.html', {'error_msg': "No result for " + target})
#         else:
#             return HttpResponseRedirect(reverse('musicblog:albumview_detail', args=(target_album.slug,)))
#     else:
#         try:
#             target_song = Song.objects.get(title=target)
#         except(Album.DoesNotExist):
#             return render(request, 'musicb/index.html', {'error_msg': "No result for " + target})
#         else:
#             return HttpResponseRedirect(reverse('musicblog:songview_detail', args=(target_song.slug,)))


class ArtistLV(ListView):
    def get_queryset(self):
        return Artist.objects.order_by('name')
    
    allow_empty = True

class ArtistDV(DetailView):
    model = Artist

class MemberLV(ListView):
    def get_queryset(self):
        return Member.objects.order_by('name')
    
    allow_empty = True

class MemberDV(DetailView):
    model = Member

class AlbumLV(ListView):
    def get_queryset(self):
        return Album.objects.order_by('title')
    
    allow_empty = True

class AlbumDV(DetailView):
    model = Album
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["title_tracks"] = context['object'].song_set.filter(is_titlesong=True)
        except(Song.DoesNotExist):
            pass
        return context
    
    

class SongLV(ListView):
    def get_queryset(self):
        return Song.objects.order_by('title')
    
    allow_empty = True

class SongDV(DetailView):
    model = Song