from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    def average_rating(self):
        from django.db.models import Avg
        reviews = Review.objects.filter(movie=self)
        if reviews.exists():
            return round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        return 0.0
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class MovieRequest(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - requested by {self.requested_by.username}"