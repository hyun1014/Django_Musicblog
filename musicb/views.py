from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from .models import Artist, Member, Album, Track
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.utils import IntegrityError

# Create your views here.
class IndexView(TemplateView):
    template_name = 'musicb/index.html'

class SearchView(View):
    def post(self, request):
        kword = request.POST['kword']
        artist_list = Artist.objects.filter(name__icontains=kword)
        member_list = Member.objects.filter(name__icontains=kword)
        album_list = Album.objects.filter(title__icontains=kword)
        track_list = Track.objects.filter(title__icontains=kword)
        context = {'artist_list': artist_list, 'member_list': member_list, 'album_list': album_list, 'track_list': track_list}
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
            context["title_tracks"] = context['object'].track_set.filter(is_titlesong=True)
        except(Track.DoesNotExist):
            pass
        return context
    
    

class TrackLV(ListView):
    def get_queryset(self):
        return Track.objects.order_by('title')
    
    allow_empty = True

class TrackDV(DetailView):
    model = Track

class NewInfoView(TemplateView):
    template_name='musicb/newinfo.html'

class NewArtistView(TemplateView):
    template_name = 'musicb/new_artist.html'

class NewMemberView(TemplateView):
    template_name = 'musicb/new_member.html'

class NewAlbumView(TemplateView):
    template_name = 'musicb/new_album.html'

class NewTrackView(TemplateView):
    template_name = 'musicb/new_track.html'

class NotValidYear(Exception): # 데뷔 연도 유효성 검증
    pass
class AlreadyExist(Exception): # 동일 데이터 이미 존재
    pass

class NewInfoSuccessView(View):
    def post(self, request, itype):
        if itype=='artist': ### Artist 추가 ###
            name = request.POST['name']
            company = request.POST['company']
            debut = request.POST['debut']
            artistinfo = request.POST['artistinfo']
            slug = name.lower().replace(' ', '-').replace('(','').replace(')','').replace('.','')
            new_artist = Artist(name=name, slug=slug, company=company, debut=debut, artist_info=artistinfo)
            try:
                if debut=="" or int(debut)<1900 or int(debut)>2020: # 데뷔 연도 유효성 검증
                    raise NotValidYear
                if artistinfo=="":
                    new_artist.artist_info = "There is no information."
                if company=="":
                    new_artist.company = "No company"
                new_artist.save()
            except (IntegrityError): # 중복된 이름의 아티스트 배제 -> error_alexist
                return render(request, template_name='musicb/new_artist.html', context={'error_alexist': True, 'ex_com': company, 
                'ex_debut': debut, 'ex_info': artistinfo})
            except (NotValidYear):
                return render(request, template_name='musicb/new_artist.html', context={'error_notvalidyear': True, 'ex_name': name, 'ex_com': company,
                'ex_debut': debut, 'ex_info': artistinfo})
            else:
                con = {'type': 'artist'}
        elif itype=='member': ### Member 추가 ###
            name = request.POST['name']
            team = request.POST['team']
            slug = name.lower().replace(' ', '-').replace('(','').replace(')','').replace('.','')
            try:
                new_member = Member(name=name, slug=slug)
                new_member.team = Artist.objects.filter(name__icontains=team)[0] # 괄호 여부와 상관없이 일단 포함
                if Member.objects.filter(name=name).exists() and Artist.objects.filter(name=team).exists(): #UNIQUE constraint failed: musicb_member.slug 에러 발생. 차후 수정 요망.
                    raise AlreadyExist
            except (Artist.DoesNotExist):
                con = {'error_noartist':True, 'ex_name': name}
                return render(request, 'musicb/new_member.html', con)
            except (AlreadyExist):
                con = {'error_alexist':True}
                return render(request, 'musicb/new_member.html', con)
            else:
                new_member.save()
                con = {'type': 'member'}
        elif itype=='album': ### Album 추가 ###
            title = request.POST['title']
            artist = request.POST['artist']
            on_sale = request.POST['on_sale']
            slug = title.lower().replace(' ', '-').replace('(','').replace(')','').replace('.','')
            try:
                new_album = Album(title=title, slug=slug, on_sale=on_sale)
                new_album.artist = Artist.objects.filter(name__icontains=artist)[0] # 괄호 여부와 상관없이 일단 포함
            except (Artist.DoesNotExist):
                con = {'error_noartist':True, 'ex_title':title, 'ex_sale':on_sale}
                return render(request, 'musicb/new_album.html', con)
            else:
                new_album.save()
                con = {'type': 'album'}
        else: ### Track 추가 ###
            title = request.POST['title']
            artist = request.POST['artist']
            album = request.POST['album']
            is_titlesong = request.POST['is_titlesong'] # 아예 bool 값을 받아올수는 없을까 -------------------------
            youtube_id = request.POST['youtube_id']
            lyrics = request.POST['lyrics']
            slug = title.lower().replace(' ', '-').replace('(','').replace(')','').replace('.','')
            try:
                new_track = Track(title=title, slug=slug, is_titlesong=(True if is_titlesong=="True" else False), youtube_id=youtube_id, lyrics=lyrics)
                new_track.artist = Artist.objects.filter(name__icontains=artist)[0] # 괄호 여부와 상관없이 일단 포함
                if lyrics=="":
                    new_track.lyrics = "There is no lyrics yet."
                if album!="":
                    new_track.album = Album.objects.get(title=album)
                else:
                    new_track.album = Album.objects.get(title="Unknown")
            except (Artist.DoesNotExist):
                con = {'error_noartist':True, 'ex_title':title, 'ex_album':album, 'ex_istitle':is_titlesong, 'ex_you':youtube_id, 'ex_lyrics':lyrics}
                return render(request, 'musicb/new_track.html', con)
            except (Album.DoesNotExist):
                con = {'error_noalbum':True, 'ex_title':title, 'ex_artist':artist, 'ex_istitle':is_titlesong, 'ex_you':youtube_id, 'ex_lyrics':lyrics}
                return render(request, 'musicb/new_track.html', con)
            else:
                new_track.save()
                con = {'type': 'track'}

        return render(request, template_name='musicb/newinfosuccess.html', context=con)