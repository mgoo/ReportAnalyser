from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=8)
    market = models.CharField(max_length=5)

    def __str__(self):
        return self.name + ' - ' + self.market


class ReportAnalysis(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING)
    year = models.IntegerField()
    polarity = models.FloatField()

    def __str__(self):
        return "Report Analysis {id: %d}" % self.id
