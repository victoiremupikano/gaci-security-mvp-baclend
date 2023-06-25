from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, names, phone_number, staff, password=None, password2=None):
        """
        Creates and saves a User with the given email, names, phone_number, and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            names=names,
            phone_number=phone_number,
            staff=staff
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, names, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, names, phone_number and password.
        """
        user = self.create_user(
            email,
            password=password,
            names=names,
            phone_number=phone_number,
            staff=True
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#  Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    names=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    staff=models.BooleanField(null=False)
    phone_number=PhoneNumberField(unique=True,null=False,blank=False)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['names', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission ?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True

    def __str__(self):
        return f"User {self.email}"

# Agent Model
class Agent(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    names=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    phone_number=PhoneNumberField(unique=True,null=False,blank=False)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agent {self.names}"

# Profile User Model
class Profile(models.Model):

    KIND=(
        ('MASCULIN', 'masculin'),
        ('FEMININ', 'féminin'),
        ('AUTRES', 'autres'),
    )

    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    agent=models.ForeignKey(Agent, on_delete=models.PROTECT)
    kind=models.CharField(max_length=25, choices=KIND)
    adress=models.CharField(max_length=255, null=True, blank=True)
    picture=models.ImageField(upload_to='Images/Profile', max_length=255, null=True, blank=True)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile {self.agent.names}"

# Function User Model
class Function(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    wording=models.CharField(max_length=255, unique=True, null=False, blank=False)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Function {self.wording}"

# Assignment User Model
class Assignment(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    agent=models.ForeignKey(Agent, on_delete=models.PROTECT)
    function=models.ForeignKey(Function, on_delete=models.PROTECT)
    date_start=models.DateTimeField()
    date_end=models.DateTimeField()
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Assignment {self.agent.names}"

# Rate Model, taux des lotisseurs
class Rate(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    value=models.DecimalField(max_digits=13, decimal_places=4, null=False)
    date_start=models.DateTimeField()
    date_end=models.DateTimeField()
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rate {self.value}"

# Station Model
class Station(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    wording=models.CharField(max_length=255, unique=True, null=False, blank=False)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Station {self.wording}"

# Usage Model
class Usage(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    wording=models.CharField(max_length=255, unique=True, null=False, blank=False)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Usage {self.wording}"

# Buy_Mode Model
class Buy_Mode(models.Model):
    user=models.ForeignKey(User, on_delete=models.PROTECT) # utilisateur qui fait l'operation
    wording=models.CharField(max_length=255, unique=True, null=False, blank=False)
    date_add=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Buy_Mode {self.wording}"

