from django.db import models
from django.db.models import Max


class Market(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return "Market {id: %d}" % self.id

    def convert_price(self, price, at_date, to_date):
        current_cpi = self.cpi_at(at_date)
        other_cpi = self.cpi_at(to_date)

        return price * (other_cpi / current_cpi)


    def cpi_at(self, date):
        cpi_query = MarketData.objects.filter(market_id=self.id, measure='CPI')

        after = cpi_query.filter(date__gte=date).order_by('date').values()
        before = cpi_query.filter(date__lte=date).order_by('-date').values()

        if len(after) == 0: # If the date is newer than all the data
            return before[0]['value']
        if len(before) == 0: # If the date is earlier than all the data
            return after[0]['value']

        after = after[0]
        before = before[0]
        after_days = (after['date'] - date.date()).days
        before_days = (date.date() - before['date']).days
        total_days = after_days + before_days

        return after['value'] * (after_days / total_days) + before['value'] * (before_days / total_days)



class MarketData(models.Model):
    market = models.ForeignKey(Market, on_delete=models.DO_NOTHING)
    measure = models.CharField(db_index=True, max_length=128)
    value = models.FloatField()
    date = models.DateField(db_index=True)

    def __str__(self):
        return "MarketData {id: %d}" % self.id


class Instrument(models.Model):
    name = models.CharField(max_length=8)
    market = models.ForeignKey(Market, on_delete=models.DO_NOTHING)

    def get_current_price(self) -> float:
        date = HistoricPrices.objects\
            .filter(instrument_id=self.id)\
            .latest('date')\
            .date

        return HistoricPrices.objects\
            .filter(date=date, instrument_id=self.id)\
            .values('close')[0]['close']

    def get_price_history(self):
        query_result = HistoricPrices.objects\
            .filter(instrument_id=self.id)\
            .values('close', 'date')

        history = {instance['date'].strftime('%Y-%m-%d'): instance['close'] for instance in query_result}

        return history

    def get_price_at(self, date) -> float:
        most_recent_date = HistoricPrices.objects \
            .filter(instrument_id=self.id, date__lte=date) \
            .aggregate(Max('date'))['date__max']

        return HistoricPrices.objects\
            .filter(date=most_recent_date, instrument_id=self.id)\
            .values('close')[0]['close']

    def __str__(self):
        return self.name + ' - ' + self.market.name

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


class Dividend(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING)
    date = models.DateField()
    dps = models.FloatField()

    def __str__(self):
        return "Dividend {id: %d}" % self.id
