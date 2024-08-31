from django.db import models
from django.contrib.postgres.fields import ArrayField

class Building(models.Model):
    id = models.AutoField(primary_key=True)
    floor_map = ArrayField(
        ArrayField(
            ArrayField(
                models.IntegerField(), 
                blank=True, 
                null=True
            ),
            blank=True,
            null=True
        ),
        blank=True,
        null=True
    )
    tti = ArrayField(
        ArrayField(
            ArrayField(
                models.IntegerField(), 
                blank=True, 
                null=True
            ),
            blank=True,
            null=True
        ),
        blank=True,
        null=True
    )
    fire = ArrayField(
        ArrayField(
            ArrayField(
                models.IntegerField(), 
                blank=True, 
                null=True
            ),
            blank=True,
            null=True
        ),
        blank=True,
        null=True
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id is {self.id}, in city {self.city}'

    class Meta:
        db_table = 'buildings'
        verbose_name = 'Building'
        verbose_name_plural = 'Buildings'
        ordering = ['id']
