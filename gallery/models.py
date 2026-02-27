from django.db import models


class Album(models.Model):
    album_name = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='gallery/covers/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.album_name


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/photos/')
    caption = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f"{self.album.album_name} - {self.caption or 'Photo'}"


class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_link = models.CharField(
        max_length=300, 
        help_text="Just copy and paste the FULL YouTube link from your browser address bar or the 'Share' button. (e.g., https://www.youtube.com/watch?v=...) Do NOT paste iframe embed code."
    )
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title

    def get_embed_url(self):
        import re
        patterns = [
            r'(?:v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_link)
            if match:
                return f"https://www.youtube.com/embed/{match.group(1)}"
        return self.youtube_link
