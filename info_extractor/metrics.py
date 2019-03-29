from django.db.models import Sum, Max

from info_extractor.models import Dividend


class Metric:

    def get_name(self):
        pass

    def process(self, instrument, start_date, end_date) -> float:
        pass


class AvgDividendYield(Metric):

    def get_name(self):
        return "Average Dividend Yield"

    def process(self, instrument, start_date, end_date) -> float:
        div_list = Dividend.objects \
            .filter(
                instrument_id=instrument.id,
                date__gt=start_date,
                date__lt=end_date
            ) \
            .values()

        div_yields = [div_instance['dps'] / instrument.get_price_at(div_instance['date']) for div_instance in div_list]

        return sum(div_yields) / len(div_yields) * 100


class DividendYieldAt(Metric):

    def get_name(self):
        return "Dividend Yield"

    def process(self, instrument, start_date, end_date) -> float:
        date = Dividend.objects \
            .filter(
                instrument_id=instrument.id,
                date__gt=start_date,
                date__lt=end_date
            ).aggregate(Max('date'))['date__max']
        dps = Dividend.objects \
            .filter(instrument_id=instrument.id, date=date) \
            .values('dps')[0]['dps']
        return dps / instrument.get_price_at(date) * 100


class PriceChange(Metric):

    def get_name(self):
        return "Price Change"

    def process(self, instrument, start_date, end_date) -> float:
        start_price = instrument.get_price_at(start_date)
        end_price = instrument.get_price_at(end_date)
        return (end_price - start_price) / start_price * 100


class RealPriceChange(Metric):

    def get_name(self):
        return "Real Price Change"

    def process(self, instrument, start_date, end_date):
        start_price = instrument.market.convert_price(instrument.get_price_at(start_date), start_date, end_date)
        end_price = instrument.market.convert_price(instrument.get_price_at(end_date), end_date, end_date)

        return (end_price - start_price) / start_price * 100