from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.urls import reverse
from django.db.models import Avg,Count
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import Permission,Group
from decimal import Decimal

from main.validators import validate_email
# Create your models here.

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100,null=False,unique=True)
    phone = PhoneNumberField(null=False,blank=False)
    address = models.CharField(max_length=255,blank=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",'phone', 'address']

    # groups = models.ManyToManyField(Group, verbose_name='groups', related_name='user_group')
    # user_permissions = models.ManyToManyField(Permission, verbose_name='permissions', related_name='user_permission')

class Account(models.Model):
    account_id = models.CharField(primary_key=True,max_length=12,unique=True,editable=False,blank=True)
    user_id = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    slug = models.SlugField(unique=True,max_length=50,blank=True,editable=False)
    current_balance = models.DecimalField(max_digits=13,decimal_places=3,default=0,validators=[MinValueValidator(Decimal('0.0'))])
    open_date = models.DateField(auto_now=True)

    def save(self,*args, **kwargs):
        if not self.account_id:
           prefix = 'AA{}'.format(timezone.now().strftime('%y%m%d'))
           prev_instances = self.__class__.objects.filter(account_id__contains=prefix)
           if prev_instances.exists():
              last_instance_id = prev_instances.last().account_id[-4:]
              self.account_id = prefix+'{0:04d}'.format(int(last_instance_id)+1)
           else:
               self.account_id = prefix+'{0:04d}'.format(1)
        if not self.slug:
           self.slug = slugify(self.account_id)
        super(Account, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('account',kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return f'{self.account_id} - {self.user_id.email}'
    
class Transaction(models.Model):
    from_account = models.ForeignKey(Account,on_delete=models.SET_NULL,related_name="payer",null=True)
    to_account = models.ForeignKey(Account,on_delete=models.SET_NULL,related_name="payee",null=True)
    money_transfer = models.DecimalField(max_digits=13,decimal_places=3)
    detail = models.CharField(max_length=255,default='transfer money')
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=False,max_length=50,blank=True,editable=False)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.detail)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('transaction',kwargs={'slug': self.slug})
    
    def __str__(self) -> str:
        return f"{self.detail}"