from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Artist(models.Model):
    name = models.CharField(verbose_name="Name", null=False, blank=False, unique=True, max_length=50)
    slug = models.SlugField("Slug", unique=True, allow_unicode=True, help_text='one word for title alias.') #처음에는 default값 정해주고, admin.py 수정 후에는 지우면 됨 (왜 그럴까 시발)
    company = models.CharField(verbose_name="Company", default="No company", max_length=50, null=True, blank=True)
    debut = models.PositiveIntegerField(default=2020, validators=[MinValueValidator(1900), MaxValueValidator(2021)], null=True, blank=True)
    artist_info = models.TextField(verbose_name='ArtistInfo', default="There is no information.", null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("musicblog:artistview_detail", kwargs={"slug": self.slug})
    


class Member(models.Model):
    name = models.CharField(verbose_name="Name", null=False, blank=False, max_length=50)
    slug = models.SlugField("Slug", unique=True, allow_unicode=True, help_text='one word for title alias.')
    team = models.ForeignKey('Artist', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("musicblog:memberview_detail", kwargs={"slug": self.slug})


class Album(models.Model):
    title = models.CharField(verbose_name='title', null=False, blank=False, max_length=100)
    slug = models.SlugField("Slug", unique=True, allow_unicode=True, help_text='one word for title alias.')
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    on_sale = models.DateField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("musicblog:albumview_detail", kwargs={"slug": self.slug})


class Track(models.Model):
    title = models.CharField(verbose_name='title', null=False, blank=False, max_length=100) # 이 null=True는 필수로 한다는 말이 아닌건가? 모르겠다 시발.
    slug = models.SlugField("Slug", unique=True, allow_unicode=True, help_text='one word for title alias.')
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, default=12) # 얘를 굳이 id값으로 지정해줘야하나?
    album = models.ForeignKey('Album', on_delete=models.CASCADE, default=4)
    is_titlesong = models.BooleanField(default=False)
    youtube_id = models.CharField(max_length=100, null=True, blank=True)
    lyrics = models.TextField(verbose_name='lyrics', null=True, blank=True, default="There is no lyrics yet.")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("musicblog:trackview_detail", kwargs={"slug": self.slug})