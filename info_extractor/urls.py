from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views, views_trader, views_instrument, views_portfolio, views_compare, \
    views_markets

app_name = 'info_extractor'

urlpatterns = [
    path('', views.home, name='home'),

    path('instrument/<int:instrument_id>/report/upload', views_instrument.report_upload, name='report_upload'),
    path('instrument/<int:instrument_id>/report/process', views_instrument.report_process, name='report_process'),

    path('instrument/<int:instrument_id>/stock/process', views_instrument.stock_process, name='stock_process'),

    path('instrument/list', views_instrument.instrument_list, name='instrument_list'),
    path('instrument/add', views_instrument.instrument_add, name='instrument_add'),
    path('instrument/process', views_instrument.instrument_process, name='instrument_process'),

    path('instrument/<int:instrument_id>', views_instrument.home, name='instrument'),
    path('instrument/<int:instrument_id>/reports', views_instrument.reports, name='instrument_reports'),
    path('instrument/<int:instrument_id>/report/<int:report_id>', views_instrument.report, name='instruments_report'),
    path('instrument/<int:instrument_id>/tables', views_instrument.tables, name='instrument_tables'),
    path('instrument/<int:instrument_id>/stock', views_instrument.stock_upload, name='instrument_stock'),
    path('instrument/<int:instrument_id>/analysis', views_instrument.analysis, name='instrument_analysis'),

    path('trader/list', views_trader.list, name='trader_list'),

    path('portfolio/transactions', views_portfolio.transactions, name='portfolio_transactions'),
    path('portfolio/position', views_portfolio.current_position, name='portfolio_position'),
    path('portfolio/add_transaction', views_portfolio.add_transaction, name='portfolio_add'),
    path('portfolio/process_add_transaction', views_portfolio.process_add_transaction, name='portfolio_process_add_transaction'),

    path('compare/home', views_compare.home, name='compare_home'),
    path('compare/timeperiod', views_compare.compare_time_period, name='compare_timeperiod'),
    path('compare/timeperiodresults', views_compare.compare_time_period_results, name='compare_timeperiod_results'),
    path('compare/timeseries', views_compare.compare_time_series, name='compare_timeseries'),
    path('compare/timeseriesresults', views_compare.compare_time_series_results, name='compare_timeseries_results'),

    path('market/list', views_markets.market_list, name='market_list'),
    path('market/<int:market_id>/view', views_markets.market, name='market_view'),
    path('market/<int:market_id>/upload', views_markets.upload_data_form, name='market_upload'),
    path('market/<int:market_id>/process_upload', views_markets.upload_data, name='market_upload_process'),
    path('market/add', views_markets.add_market_form, name='market_add'),
    path('market/process_add', views_markets.add_market, name='market_add_process')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)