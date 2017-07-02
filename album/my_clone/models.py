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
        return "{} {} {}".format(self.my_user.first_name,
                                 self.my_user.last_name,
                                 self.creation_date)
    def __str__(self):
        return self.photo_info







