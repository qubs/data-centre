import datetime

from django.db import models
from django.core.exceptions import ValidationError


def validate_year(year):
    if year is None:
        return  # Years can be null
    if year < 1800 or year > datetime.datetime.now().year:
        raise ValidationError("Not a valid year.")


def validate_day_of_month(day):
    if day is None:
        return  # Days can be null
    elif day > 31 or day < 1:
        raise ValidationError("Not a valid day.")


class Specimen(models.Model):
    """
    A model of a herbarium_data specimen entry.
    """

    MONTH_CHOICES = (
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December")
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    dataset = models.CharField(max_length=50)

    genus = models.CharField(max_length=50, db_index=True)
    species = models.CharField(max_length=50, db_index=True)
    common_name = models.CharField(max_length=255)

    dth = models.CharField(max_length=10)
    accession = models.PositiveIntegerField(null=True)

    year_collected = models.PositiveSmallIntegerField(null=True, validators=[validate_year])
    month_collected = models.PositiveSmallIntegerField(null=True, choices=MONTH_CHOICES)
    day_collected = models.PositiveSmallIntegerField(null=True, validators=[validate_day_of_month])

    collectors = models.TextField(default="")

    map_included = models.NullBooleanField()
    map_reference = models.CharField(max_length=255)

    county = models.CharField(max_length=127, default="")
    township = models.CharField(max_length=127, default="")
    country = models.CharField(max_length=127, default="")

    location = models.CharField(max_length=127, default="")
    habitat = models.CharField(max_length=127, default="")

    notes = models.TextField(default="")

    image = models.ImageField(null=True)

    def __repr__(self):
        return "<Specimen {} | {} {}>".format(self.accession, self.genus, self.species)

    def __str__(self):
        return "Specimen {}: {} {}".format(self.accession, self.genus, self.species)
