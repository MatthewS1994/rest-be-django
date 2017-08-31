from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.query import QuerySet

from rest_framework.authtoken.models import Token

from fabric.colors import *


class QuerySetManager(models.Manager):
    """
    Makes it possible to chain filters (named scopes)
    """

    def __init__(self, queryset_class=QuerySet):
        super(QuerySetManager, self).__init__()
        self._queryset_class = queryset_class

    def get_query_set(self):
        return self._queryset_class(self.model)


class Timestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
        account.set_password(password)
        account.save()
        Token.objects.create(user=account)
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_superuser = True
        account.is_staff = True
        account.is_admin = True
        account.is_active = True
        account.save()

        print blue('    ---*------------------------------------------------------------------------------------------------------')
        print blue('')
        print blue('	| | | | /  ___/ | ____| |  _  \       /  ___| |  _  \  | ____|     /   | |_   _| | ____| |  _  \ ')
        print blue('	| | | | | |___  | |__   | |_| |       | |     | |_| |  | |__      / /| |   | |   | |__   | | | | ')
        print blue('	| | | | \___  \ |  __|  |  _  /       | |     |  _  /  |  __|    / / | |   | |   |  __|  | | | | ')
        print blue('	| |_| |  ___| | | |___  | | \ \       | |___  | | \ \  | |___   / /  | |   | |   | |___  | |_| | ')
        print blue('	\_____/ /_____/ |_____| |_|  \_\      \_____| |_|  \_\ |_____| /_/   |_|   |_|   |_____| |_____/ ')
        print blue('')
        print blue('    ------------------------------------------------------------------------------------------------------*---')
        print yellow('   ________________________________________________________________________________')
        print green('     Username:          ') + yellow('|  ') + green(str(account.username))
        print yellow('   ________________________________________________________________________________')
        print green('     Email:             ') + yellow('|  ') + green(str(email))
        print yellow('   ________________________________________________________________________________')
        print green('     Password:          ') + yellow('|  ') + green(str(password))
        print yellow('   ________________________________________________________________________________')
        print green('     User Permissions:  ') + yellow('|  ') + green(' Superuser:  ' + str(account.is_superuser))
        print green('                        ') + yellow('|  ') + green(' Admin User:  ' + str(account.is_staff))
        print green('                        ') + yellow('|  ') + green(' Staff Member:  ' + str(account.is_admin))
        print yellow('   ________________________________________________________________________________')