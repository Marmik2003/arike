from django.db import models
from arike.utils.models import BaseModel


# Cpnstants
LOCAL_BODY_CHOICES = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
)

FACILITY_KIND = (
    ('phc', 'PHC'),
    ('chc', 'CHC'),
)


# Models
class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LocalBody(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    body_type = models.IntegerField(choices=LOCAL_BODY_CHOICES)
    localbody_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = (
            "district",
            "body_type",
            "name",
        )
        verbose_name_plural = "Local Bodies"

    def __str__(self):
        return f"{self.name} ({self.body_type})"


class Ward(models.Model):
    name = models.CharField(max_length=255)
    localbody = models.ForeignKey(LocalBody, on_delete=models.PROTECT)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name} ({self.number})"

    class Meta:
        unique_together = (
            "localbody",
            "number",
        )


class Facility(BaseModel):
    kind = models.CharField(max_length=4, choices=FACILITY_KIND)
    name = models.CharField(max_length=255)
    address = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    pincode = models.IntegerField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.pincode})"

    class Meta:
        unique_together = (
            "name",
            "ward",
            "pincode",
        )
        verbose_name_plural = "Facilities"
