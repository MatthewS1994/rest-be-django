# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField
from autoslug import AutoSlugField

from vue_js_django.mixims import QuerySetManager, Timestamps
# Create your models here.


class Location(Timestamps):
    name = models.CharField(_("Name"), max_length=225, null=False, blank=False)
    lang = models.CharField(_("Language"), max_length=225)
    popRank = models.CharField(max_length=225, null=True, blank=True)
    woeid = models.CharField('Where on Earth ID', max_length=225, null=False, blank=False)
    uri = models.CharField('URI', max_length=225, null=True, blank=True)

    admin1_content = models.CharField(max_length=225, null=True, blank=True)
    admin1_woeid = models.CharField(max_length=225, null=True, blank=True)
    admin1_type = models.CharField(max_length=225, null=True, blank=True)

    admin2_content = models.CharField(max_length=225, null=True, blank=True)
    admin2_woeid = models.CharField(max_length=225, null=True, blank=True)
    admin2_type = models.CharField(max_length=225, null=True, blank=True)

    admin3_content = models.CharField(max_length=225, null=True, blank=True)
    admin3_woeid = models.CharField(max_length=225, null=True, blank=True)
    admin3_type = models.CharField(max_length=225, null=True, blank=True)

    latitude = models.CharField(max_length=225, null=True, blank=True)
    longitude = models.CharField(max_length=225, null=True, blank=True)

    locality_content = models.CharField(max_length=225, null=True, blank=True)
    locality_woeid = models.CharField(max_length=225, null=True, blank=True)
    locality_type = models.CharField(max_length=225, null=True, blank=True)

    country_content = models.CharField(max_length=225, null=True, blank=True)
    country_woeid = models.CharField(max_length=225, null=True, blank=True)
    country_code = models.CharField(max_length=225, null=True, blank=True)
    country_type = models.CharField(max_length=225, null=True, blank=True)

    northEast_latitude = models.CharField(max_length=225, null=True, blank=True)
    northEast_longitude = models.CharField(max_length=225, null=True, blank=True)

    southWest_latitude = models.CharField(max_length=225, null=True, blank=True)
    southWest_longitude = models.CharField(max_length=225, null=True, blank=True)

    sysname = AutoSlugField(max_length=255, populate_from='name', always_update=True, unique=True)

    objects = QuerySetManager()

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __unicode__(self):
        return self.name


class WeatherLog(Timestamps):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name=_("City Location"))
    title = models.CharField(_("Title"), max_length=225, null=False, blank=False)
    pressure = models.CharField(max_length=225, null=True, blank=True)
    rising = models.CharField(max_length=225, null=True, blank=True)
    visibility = models.DecimalField(_("visibility (km)"), max_digits=5, decimal_places=2)
    humidity = models.IntegerField(_("humidity (%)"))

    date = models.CharField(max_length=225, null=True, blank=True)
    text = models.CharField(max_length=225, null=True, blank=True)
    temp = models.IntegerField(_("temperature"))

    city = models.CharField(max_length=225, null=True, blank=True)
    region = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)

    sunset = models.CharField(max_length=225, null=True, blank=True)
    sunrise = models.CharField(max_length=225, null=True, blank=True)

    wind_direction = models.CharField(max_length=225, null=True, blank=True)
    wind_speed = models.DecimalField(_("wind speed (km/h)"), max_digits=5, decimal_places=2)
    wind_chill = models.CharField(max_length=225, null=True, blank=True)

    forecast = JSONField()

    objects = QuerySetManager()

    class Meta:
        verbose_name = _("Weather log")
        verbose_name_plural = _("Weather logs")
        ordering = ("title",)

    def __unicode__(self):
        return "%s @ %s" % (
            self.location.name,
            self.created_at.strftime("%Y-%m-%dT%H:%M"),
        )