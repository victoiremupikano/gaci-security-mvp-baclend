import os
from django.db import models
# on import le models User de django de facon professionnel
from django.contrib.auth import get_user_model

User = get_user_model()

# def pour mettre le nom de l'user sur l'image
def get_image_path_wtr(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.names + "_wtr", ext)
    return os.path.join('Images/Datasource/Wtr/', filename)

def get_image_path_cai(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.names + "_cai", ext)
    return os.path.join('Images/Datasource/Cai/', filename)


# Create your models here.
# want to research (envie de recherche)
class Want_To_Research(models.Model):

    KIND=(
        ('MASCULIN', 'masculin'),
        ('FEMININ', 'féminin'),
        ('AUTRES', 'autres'),
    )

    user=models.ForeignKey(User, on_delete=models.PROTECT)
    names=models.CharField(max_length=255, null=False, blank=False)
    kind=models.CharField(max_length=25, choices=KIND)
    is_finish=models.BooleanField(default=False)
    is_cancel=models.BooleanField(default=False)
    reason=models.CharField(max_length=255, null=True, blank=True)
    picture=models.ImageField(upload_to=get_image_path_wtr, max_length=255, null=True, blank=True)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Want_To_Research {self.reason}"

# curfew and instability(couvre-feu et instabilité)
class Curfew_And_Instability(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    reason=models.CharField(max_length=255, null=False, blank=False)
    longitude=models.CharField(max_length=255, null=False, blank=False)
    latittude=models.CharField(max_length=255, null=False, blank=False)
    is_finish=models.BooleanField(default=False)
    is_cancel=models.BooleanField(default=False)  
    picture=models.ImageField(upload_to=get_image_path_cai, max_length=255, null=True, blank=True)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Curfew_And_Instability {self.reason}"
    
# 
# population alert(alerte de la population)
class Population_Alert(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    reason_issued=models.CharField(max_length=255, null=False, blank=False)
    reason_to_certify=models.CharField(max_length=255, null=True, blank=True)
    longitude=models.CharField(max_length=255, null=False, blank=False)
    latittude=models.CharField(max_length=255, null=False, blank=False)
    is_finish=models.BooleanField(default=False)
    is_cancel=models.BooleanField(default=False)  
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Population_Alert {self.reason_issued}"
 
# le tentative de reconnaissance   
class Recognized(models.Model):
    wtr=models.ForeignKey(Want_To_Research, on_delete=models.PROTECT)
    names=models.CharField(max_length=255, null=False, blank=False)
    longitude=models.CharField(max_length=255, null=True, blank=True)
    latittude=models.CharField(max_length=255, null=True, blank=True)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recognized {self.names}"