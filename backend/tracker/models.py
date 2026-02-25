from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):

    TRANSACTION_TYPE = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    CATEGORIES = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('rent', 'Rent'),
        ('shopping', 'Shopping'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    note = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"