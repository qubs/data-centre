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

    # Generated Attributes

    def latin_name(self):
        return "{} {}".format(self.genus, self.species)

    def date_collected_str(self):
        if self.year_collected:
            if self.month_collected:
                if self.day_collected:
                    return "{} {}, {}".format(self.get_month_collected_display(), self.day_collected,
                                              self.year_collected)
                else:
                    return "{}, {}".format(self.get_month_collected_display(), self.year_collected)
            else:
                return self.year_collected
        return None

    date_collected_str.short_description = "Date Collected"

    # Schema Attributes

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    dataset = models.CharField(max_length=50, default="")

    genus = models.CharField(max_length=50, default="", db_index=True)
    species = models.CharField(max_length=50, default="", db_index=True)
    common_name = models.CharField(max_length=255, default="")

    dth = models.CharField(max_length=10, default="")
    accession = models.CharField(max_length=20, default="")

    year_collected = models.PositiveSmallIntegerField(null=True, validators=[validate_year])
    month_collected = models.PositiveSmallIntegerField(null=True, choices=MONTH_CHOICES)
    day_collected = models.PositiveSmallIntegerField(null=True, validators=[validate_day_of_month])

    collectors = models.TextField(default="")

    map_included = models.NullBooleanField()
    map_reference = models.CharField(max_length=255, default="")

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
