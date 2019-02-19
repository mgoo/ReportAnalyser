from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=8)
    market = models.CharField(max_length=5)

    def __str__(self):
        return self.name + ' - ' + self.market

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class ReportAnalysis(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING)
    year = models.IntegerField()
    polarity = models.FloatField()

    def __str__(self):
        return "Report Analysis {id: %d}" % self.id


class Transaction(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    price = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return "Transaction {id: %d}" % self.id