from django.db import models
from django.contrib.auth.models import User

# class User -> he's always watching :)
# https://docs.djangoproject.com/en/1.11/ref/contrib/auth/
# his fields:
# username, first_name, last_name, email, password, groups
# user_permissions, is_staff, is_active, is_superuser,
# last_login, date_joined


class Photo(models.Model):

    path = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now=True)
    my_user = models.ForeignKey(User)

    @property
    def photo_info(self):
        return "Added: {} by {}".format(self.creation_date
                                            .strftime("%Y-%m-%d, %H:%M:%S"),
                                        self.my_user.username)

    def __str__(self):
        return "ID:" + str(self.id) + " " + self.photo_info


class Like(models.Model):
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    created = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    created = models.DateTimeField(auto_now=True)

    @property
    def comment_info(self):
        return "{}, {}".format(self.user.username,
                                 self.created.strftime("%Y-%m-%d, %H:%M:%S"))

    def __str__(self):
        return "ID:" + str(self.id) + " " + self.comment_info



