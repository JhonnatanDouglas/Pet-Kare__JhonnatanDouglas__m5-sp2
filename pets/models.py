from django.db import models


class Gender(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT_INFORMED = "Not Informed"


class Pet(models.Model):
    class Meta:
        ordering = ("id",)

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=Gender.choices, default=Gender.NOT_INFORMED
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, null=True, related_name="pets"
    )
    traits = models.ManyToManyField("traits.Trait", related_name="traits")

    def __repr__(self) -> str:
        return f"<Pet: {self.id} - {self.name}>"
