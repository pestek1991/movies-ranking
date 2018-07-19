# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
import re

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=30, verbose_name="Tytuł")
    director = models.CharField(max_length=50, verbose_name="Reżyseria")
    writters = models.CharField(max_length=50, verbose_name="Scenariusz")
    length = models.DurationField(verbose_name="Długość")
    country = models.CharField(max_length=50, verbose_name="Kraj")
    add_date = models.DateField( verbose_name="Premiera")
    image = models.FileField(upload_to="images/", verbose_name="Plakat")
    trailer_url = models.URLField(verbose_name="Link do trailera Yutube")


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-add_date"]

class MovieForm(ModelForm):

    #title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'wpisz tytuł filmu'}))

    add_date = forms.DateField(widget=AdminDateWidget())

    class Meta:
        model = Movie
        fields = '__all__'

    def clean_trailer_url(self):
        url = self.cleaned_data['trailer_url']
        if not re.match("^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_])+", url):
            raise forms.ValidationError("Wpisz poprawny adres filmu  z Youtuba")
        return url








