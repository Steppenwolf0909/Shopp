from django.db import models


# Create your models here.

class Mail_verification(models.Model):
    mail = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=4, null=True)

    class Meta:
        verbose_name = 'Подтверждение почты'
        verbose_name_plural = 'Подтверждение почты'
