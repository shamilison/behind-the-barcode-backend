from django.db import models


class OpenFoodFact(models.Model):
    barcode = models.CharField(max_length=64, primary_key=True)
    product_name = models.TextField(null=True, blank=True)
    brands = models.TextField(null=True, blank=True)
    brands_en = models.TextField(null=True, blank=True)
    brands_tags = models.TextField(null=True, blank=True)
    origins = models.TextField(null=True, blank=True)
    origins_en = models.TextField(null=True, blank=True)
    origins_tags = models.TextField(null=True, blank=True)
    countries = models.TextField(null=True, blank=True)
    countries_en = models.TextField(null=True, blank=True)
    countries_tags = models.TextField(null=True, blank=True)
    cities = models.TextField(null=True, blank=True)
    cities_tags = models.TextField(null=True, blank=True)
    manufacturing_places = models.TextField(null=True, blank=True)
    manufacturing_places_tags = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.brands} ({self.barcode})"

    class Meta:
        verbose_name_plural = "Open Food Facts"
        ordering = ['barcode']
