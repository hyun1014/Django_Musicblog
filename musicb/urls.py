from django.urls import path
from . import views

app_name = 'musicblog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('artist/', views.ArtistLV.as_view(), name='artistview'),
    path('artist/(?P<slug>[-\w]+)/$', views.ArtistDV.as_view(), name='artistview_detail'), #이렇게 안하면 한글 slug는 인식 못함
    path('member/', views.MemberLV.as_view(), name='memberview'),
    path('member/(?P<slug>[-\w]+)/$', views.MemberDV.as_view(), name='memberview_detail'),
    path('album/', views.AlbumLV.as_view(), name='albumview'),
    path('album/(?P<slug>[-\w]+)/$', views.AlbumDV.as_view(), name='albumview_detail'),
    path('track/', views.TrackLV.as_view(), name='trackview'),
    path('track/(?P<slug>[-\w]+)/$', views.TrackDV.as_view(), name='trackview_detail'),
    path('newinfo/', views.NewInfoView.as_view(), name='newinfo'),
    path('newinfo/newartist', views.NewArtistView.as_view(), name='new_artist'),
    path('newinfo/newmember', views.NewMemberView.as_view(), name='new_member'),
    path('newinfo/newalbum', views.NewAlbumView.as_view(), name='new_album'),
    path('newinfo/newtrack', views.NewTrackView.as_view(), name='new_track'),
    path('newinfo/<str:itype>/newinfosuccess', views.NewInfoSuccessView.as_view(), name='newinfosuccess'),
    #path('newinfo/newinfofailed', views.NewInfoFailedView.as_view(), name='newinfofailed'),
]
