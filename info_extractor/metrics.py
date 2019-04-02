from django.db.models import Sum, Max

from info_extractor.models import Dividend, HistoricPrices, Instrument


class SingleMetric:

    def get_name(self):
        pass

    def process(self, instrument, start_date, end_date) -> float:
        pass


class AvgDividendYield(SingleMetric):

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


class DividendYieldAt(SingleMetric):

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


class PriceChange(SingleMetric):

    def get_name(self):
        return "Price Change"

    def process(self, instrument, start_date, end_date) -> float:
        start_price = instrument.get_price_at(start_date)
        end_price = instrument.get_price_at(end_date)
        return (end_price - start_price) / start_price * 100


class RealPriceChange(SingleMetric):

    def get_name(self):
        return "Real Price Change"

    def process(self, instrument, start_date, end_date):
        start_price = instrument.market.convert_price(instrument.get_price_at(start_date), start_date, end_date)
        end_price = instrument.market.convert_price(instrument.get_price_at(end_date), end_date, end_date)

        return (end_price - start_price) / start_price * 100


class OverTimeMetric:

    def get_name(self):
        pass

    def process(self, instrument, start_date, end_date):
        pass


class Price(OverTimeMetric):

    def get_name(self):
        return 'Price'

    def process(self, instrument, start_date, end_date):
        stock_data = HistoricPrices. \
            objects. \
            filter(
                instrument_id=instrument.id,
                date__gt=start_date,
                date__lt=end_date
            ). \
            order_by('date'). \
            values()

        stock_price = [(row['date'], (row['low'] + row['open'] + row['close'] + row['high']) / 4) for row in stock_data]
        stock_price.insert(0, ('Date', 'Price'))

        return stock_price


class RealPrice(OverTimeMetric):

    def get_name(self):
        return 'Real Price'

    def process(self, instrument: Instrument, start_date, end_date):
        stock_data = HistoricPrices. \
            objects. \
            filter(
                instrument_id=instrument.id,
                date__gt=start_date,
                date__lt=end_date
            ).\
            order_by('date'). \
            values()

        stock_price = [
            (row['date'], instrument.market.convert_price((row['low'] + row['open'] + row['close'] + row['high']) / 4, row['date'], start_date))
            for row in stock_data
        ]
        stock_price.insert(0, ('Date', 'Price'))

        return stock_price


class Volume(OverTimeMetric):

    def get_name(self):
        return 'Volume'

    def process(self, instrument, start_date, end_date):
        stock_data = HistoricPrices. \
            objects. \
            filter(
                instrument_id=instrument.id,
                date__gt=start_date,
                date__lt=end_date
            ). \
            order_by('date'). \
            values()

        stock_volume = [(row['date'], row['volume']) for row in stock_data]
        stock_volume.insert(0, ('Date', 'Price'))

        return stock_volume


class PriceChangePercent(OverTimeMetric):

    def get_name(self):
        return 'Price Change Percentage'

    def process(self, instrument, start_date, end_date):
        stock_data = HistoricPrices. \
            objects. \
            filter(
                instrument_id=instrument.id,
                date__gt=start_date,
                date__lt=end_date
            ). \
            order_by('date'). \
            values()

        starting_price = stock_data[0]['open']
        def percent_change(start_price, row):
            dayly_price = (row['low'] + row['open'] + row['close'] + row['high']) / 4
            return ((dayly_price - start_price) / start_price) * 100

        stock_price = [(row['date'], percent_change(starting_price, row)) for row in stock_data]
        stock_price.insert(0, ('Date', 'PriceChange'))

        return stock_price
