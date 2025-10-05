from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'age', 'nephropathy_risk', 'neuropathy_risk', 'retinopathy_risk']
    list_filter = ['created_at', 'sex', 'smoking', 'physical_activity']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'created_at')
        }),
        ('Demographics', {
            'fields': ('age', 'sex', 'bmi')
        }),
        ('Vital Signs', {
            'fields': ('systolic_bp', 'diastolic_bp')
        }),
        ('Laboratory Tests', {
            'fields': ('hba1c', 'fasting_plasma_sugar', 'postprandial_sugar')
        }),
        ('Medical History', {
            'fields': ('family_history', 'onset_age', 'diabetes_duration')
        }),
        ('Lifestyle Factors', {
            'fields': ('smoking', 'physical_activity')
        }),
        ('Medication', {
            'fields': ('medication_use', 'medication_adherence')
        }),
        ('Prediction Results', {
            'fields': ('nephropathy_risk', 'neuropathy_risk', 'retinopathy_risk'),
            'classes': ('wide',)
        }),
    )