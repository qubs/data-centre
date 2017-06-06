from django.db import models


class Specimen(models.Model):
    """
    A model of a herbarium specimen entry.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    dataset = models.CharField(max_length=50)

    genus = models.CharField(max_length=50, db_index=True)
    species = models.CharField(max_length=50, db_index=True)
    common_name = models.CharField(max_length=255)

    dth = models.CharField(max_length=10)
    accession = models.PositiveIntegerField(null=True)

    date_collected = models.DateField(null=True)

    collectors = models.TextField()

    map_included = models.NullBooleanField()
    map_reference = models.CharField(max_length=255)

    county = models.CharField(max_length=127)
    township = models.CharField(max_length=127)
    location = models.CharField(max_length=127)
    habitat = models.CharField(max_length=127)

    notes = models.TextField()

    image = models.ImageField(null=True)

    def __repr__(self):
        return "<Specimen {} | {} {}>".format(self.accession, self.genus, self.species)

    def __str__(self):
        return "Specimen {}: {} {}".format(self.accession, self.genus, self.species)
