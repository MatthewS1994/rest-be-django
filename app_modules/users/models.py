# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from vue_js_django.mixims import AccountManager

# Create your models here.


class Account(AbstractBaseUser, PermissionsMixin):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    MR = 'Mr'
    MRS = 'Mrs'
    MISS = 'Miss'
    TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MISS, 'Miss')
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    gender = models.CharField(max_length=25, choices=GENDER, null=True)
    title = models.CharField(max_length=255, choices=TITLE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return str(self.email)

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return '{name} {surname}'.format(name=self.first_name, surname=self.last_name)

    def get_short_name(self):
        return self.first_name
