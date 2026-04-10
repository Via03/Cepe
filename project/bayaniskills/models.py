from django.contrib.auth.models import AbstractUser
from django.db import models


# 🔷 Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('bayani', 'Bayani'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client'
    )

    def __str__(self):
        return self.username


# 🔷 Skill Model
class Skill(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.user.username}"


# 🔷 Booking Model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_bookings'
    )
    bayani = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bayani_bookings'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.client.username} booked {self.skill.name}"

    # 🔒 Safety: prevent invalid bookings
    def save(self, *args, **kwargs):
        if self.client == self.bayani:
            raise ValueError("You cannot book your own skill.")
        super().save(*args, **kwargs)