from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("cliente", "Cliente"),
        ("operador", "Operador"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="operador")
    profile_image = models.ImageField(upload_to="profiles/", default="profiles/default.png", blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
