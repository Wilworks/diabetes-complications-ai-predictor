from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    """Model to store patient data and prediction results"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Demographics
    age = models.FloatField()
    sex = models.IntegerField(choices=[(0, 'Female'), (1, 'Male')])
    bmi = models.FloatField()
    
    # Vital Signs
    systolic_bp = models.FloatField(help_text="Systolic Blood Pressure")
    diastolic_bp = models.FloatField(help_text="Diastolic Blood Pressure")
    
    # Laboratory Tests
    hba1c = models.FloatField(help_text="Glycated Hemoglobin")
    fasting_plasma_sugar = models.FloatField()
    postprandial_sugar = models.FloatField()
    
    # Medical History
    family_history = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])
    onset_age = models.FloatField(help_text="Age when diabetes was diagnosed")
    diabetes_duration = models.FloatField(help_text="Duration in years")
    
    # Lifestyle
    smoking = models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'Ex-smoker')])
    physical_activity = models.IntegerField(choices=[(0, 'Low'), (1, 'Moderate'), (2, 'High')])
    
    # Medication
    medication_use = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')])
    medication_adherence = models.IntegerField(choices=[(0, 'Poor'), (1, 'Moderate'), (2, 'Good')])
    
    # Prediction Results
    nephropathy_risk = models.FloatField(null=True, blank=True)
    neuropathy_risk = models.FloatField(null=True, blank=True)
    retinopathy_risk = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Prediction for {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']