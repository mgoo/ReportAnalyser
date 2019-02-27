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


class HistoricPrices(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adj_close = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return "Historic Price {id: %d}" % self.id
