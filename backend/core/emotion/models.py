from django.db import models

class EEGSignal(models.Model):
    Mean = models.FloatField(db_column='mean')
    Max = models.FloatField(db_column='max_value')
    Standard_Deviation = models.FloatField(db_column='standard_deviation')
    RMS = models.FloatField(db_column='rms')
    Peak_to_Peak = models.FloatField()
    Abs_Diff_Signal = models.FloatField()
    Alpha_Power = models.FloatField(db_column='alpha_power')
    Kurtosis = models.FloatField(db_column='kurtosis',null=True, blank=True)
    Skewness = models.FloatField(db_column='skewness', null=True, blank=True)
    timestamp = models.DateTimeField(db_column='timestamp') 

