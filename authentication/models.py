from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
# on import le models User de django de facon professionnel
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
# want to research (envie de recherche)
class Want_To_Research(models.Model):

    KIND=(
        ('MASCULIN', 'masculin'),
        ('FEMININ', 'féminin'),
        ('AUTRES', 'autres'),
    )

    user=models.ForeignKey(User, on_delete=models.PROTECT)
    kind=models.CharField(max_length=25, choices=KIND)
    adress=models.CharField(max_length=255, null=True, blank=True)
    picture=models.ImageField(upload_to='Images/Datasource', max_length=255, null=True, blank=True)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile {self.user.names}"