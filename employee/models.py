from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

class Profile(models.Model):
    usr = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, null=False, blank=False)
    salary = models.IntegerField(null=True, blank=True)

    class Meta():
        ordering = ('-salary',)

    def __str__(self):
        return "{0} {1}".format(self.usr.first_name, self.usr.last_name)


# @receiver(pre_save, sender=User)
# def create_user(sender, instance, created, **kwargs):

#     print(created)
#     if created:
#         Profile.objects.create(usr=instance)
#     else:
#         instance.profile.save()

# @receiver(post_save, sender=User)
# def user_is_created(sender, instance, created, **kwargs):
#     print(created)
#     if created:
#         Profile.objects.create(usr=instance)
#     else:
#         instance.profile.save()



