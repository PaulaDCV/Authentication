from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyAccountManager(BaseUserManager):
    def create_user(self,customer_email, username,date_birth,address, password=None):
        if not customer_email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not date_birth:
            raise ValueError("Date of birth is required")
        if not address:
            raise ValueError("address is required")
        user = self.model(
            customer_email= self.normalize_email(customer_email),
            username= username,
            date_birth= date_birth,
            address= address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,customer_email, username,date_birth,address, password=None):
        if not customer_email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not date_birth:
            raise ValueError("Date of birth is required")
        if not address:
            raise ValueError("address is required")
        user = self.model(
            customer_email= self.normalize_email(customer_email),
            username= username,
            password =password,
            date_birth= date_birth,
            address= address
        )

        user.is_admin = True
        user.is_staff =True
        user.is_superuser =True
        user.set_password(password)
        user.save(using=self._db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    customer_email = models.EmailField(verbose_name="email", max_length=60, unique= True)
    username = models.CharField(verbose_name= "customer name",max_length=30, unique=True)
    date_birth = models.DateField()
    address = models.CharField(max_length =100)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "customer_email"
    REQUIRED_FIELDS = ["username","date_birth","address"]

    objects = MyAccountManager()
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
