from django.db import models

class UserData(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    DAS_CHOICES = [
        ('AAS', 'AAS'),
        ('AFI', 'AFI'),
        ('AII', 'AII'),
        ('ASB', 'ASB'),
        ('DIR', 'DIREÇÃO'),
        ('UATP', 'UATP'),
        ('UPC', 'UPC'),
    ]
    DAS_FUNCTION = [
        ('E', 'ESTAGIÁRIO'),
        ('T', 'TÉCNICO'),
        ('C', 'COORDENADOR'),
        ('D', 'DIREÇÃO'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=False)
    birth_date = models.DateField()
    year_joined = models.IntegerField()
    unit_area = models.CharField(max_length=4, choices=DAS_CHOICES, null=False, blank=False)
    function = models.CharField(max_length=1, choices=DAS_FUNCTION, null=False, blank=False)

    def __str__(self):
        return f"{self.gender}, {self.birth_date}, {self.year_joined}, {self.unit_area}"