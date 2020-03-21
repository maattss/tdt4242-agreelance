from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.TextField(max_length=50, blank=True)
    phone_number = models.TextField(max_length=50, blank=True)
    country = models.TextField(max_length=50, blank=True)
    state = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    postal_code = models.TextField(max_length=50, blank=True)
    street_address = models.TextField(max_length=50, blank=True)
    categories = models.ManyToManyField('projects.ProjectCategory', related_name='competance_categories')

    def __str__(self):
        return self.user.username
    

class Review(models.Model):
    CHOICES=[
        (1, '1 - Very bad'),
        (2, '2 - Bad'),
        (3, '3 - Okay'),
        (4, '4 - Good'),
        (5, '5 - Very Good')
        ]
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_reviewer', default=1)
    rating = models.IntegerField(choices=CHOICES, default=3)
    comment = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return  str(self.rating) + "-" + self.comment


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save() # Saves the user profile
