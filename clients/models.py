# Create your models here.


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    avatar = models.ImageField(upload_to=f'files/avatars/', verbose_name='Аватар', null=True, blank=True)
    call_sign = models.CharField(max_length=200, verbose_name='Позывной', null=True, blank=True)
    rep = models.DecimalField(default=0, max_digits=2, decimal_places=1, null=True, blank=True,
                              verbose_name='Репутация')
    tg = models.CharField(max_length=200, verbose_name='Телеграмм', null=True, blank=True)
    vk = models.CharField(max_length=200, verbose_name='ВКонтакте', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def __str__(self):
        return self.email



class Review(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='review')
    estimate = models.IntegerField(verbose_name='Оценка', null=True, blank=False)
    text = models.CharField(max_length=2000, verbose_name='Отзыв', null=True, blank=True)
    created = models.DateTimeField(auto_now=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user.email} {self.created}'

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
