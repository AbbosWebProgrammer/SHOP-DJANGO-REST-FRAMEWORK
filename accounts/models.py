from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError('Users must have a phone')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password):
        """
        Creates and saves a staff user with the given phone and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.staff = True
        user.save(using=self._db) 
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
def user_path(instance, filename):
    print(str(filename))
    return 'User/{0}/{1}'.format(instance.phone,filename)

class User(AbstractBaseUser):
    phone = PhoneNumberField(_('phone'), unique=True)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False) 
    staff = models.BooleanField(default=False) 
    username = models.CharField(max_length=100,unique=True,null=True,blank=True)
    firstname = models.CharField(max_length=100,null=True,blank=True)
    lastname = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    birthday=models.DateField(null=True)
    image = models.ImageField(null=True,upload_to=user_path)
    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    class Meta:
        ordering = ['id']
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
 

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    objects = UserManager()
    def __str__(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

