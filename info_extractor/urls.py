from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views, views_trader, views_instrument, views_portfolio

app_name = 'info_extractor'

urlpatterns = [
    path('', views.home, name='home'),

    path('instrument/<int:instrument_id>/report/upload', views_instrument.report_upload, name='report_upload'),
    path('instrument/<int:instrument_id>/report/process', views_instrument.report_process, name='report_process'),

    path('instrument/<int:instrument_id>/stock/upload', views_instrument.stock_upload, name='stock_upload'),
    path('instrument/<int:instrument_id>/stock/process', views_instrument.stock_process, name='stock_process'),

    path('instrument/list', views_instrument.instrument_list, name='instrument_list'),
    path('instrument/add', views_instrument.instrument_add, name='instrument_add'),
    path('instrument/process', views_instrument.instrument_process, name='instrument_process'),

    path('instrument/<int:instrument_id>', views_instrument.home, name='instrument'),
    path('instrument/<int:instrument_id>/reports', views_instrument.reports, name='instrument_reports'),
    path('instrument/<int:instrument_id>/report/<int:report_id>', views_instrument.report, name='instruments_report'),
    path('instrument/<int:instrument_id>/tables', views_instrument.tables, name='instrument_tables'),
    path('instrument/<int:instrument_id>/stock', views_instrument.stock, name='instrument_stock'),

    path('trader/list', views_trader.list, name='trader_list'),

    path('portfolio/transactions', views_portfolio.transactions, name='portfolio_transactions'),
    path('portfolio/position', views_portfolio.current_position, name='portfolio_position'),
    path('portfolio/add_transaction', views_portfolio.add_transaction, name='portfolio_add'),
    path('portfolio/process_add_transaction', views_portfolio.process_add_transaction, name='portfolio_process_add_transaction')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)