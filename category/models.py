from django.db import models
from main.base_model import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=60)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='parent_category')

    def __str__(self) -> str:
        return f'name:{self.name}'


# Create your models here.
