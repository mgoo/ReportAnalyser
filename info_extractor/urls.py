from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from .viewer import views as viewer_views
from .trader import views as trader_views
from .portfolio import views as portfolio_views

app_name = 'info_extractor'

urlpatterns = [
    path('', views.home, name='home'),

    path('instrument/<int:instrument_id>/report/upload', views.report_upload, name='report_upload'),
    path('instrument/<int:instrument_id>/report/process', views.report_process, name='report_process'),

    path('instrument/<int:instrument_id>/stock/upload', views.stock_upload, name='stock_upload'),
    path('instrument/<int:instrument_id>/stock/process', views.stock_process, name='stock_process'),

    path('instrument/list', views.instrument_list, name='instrument_list'),
    path('instrument/add', views.instrument_add, name='instrument_add'),
    path('instrument/process', views.instrument_process, name='instrument_process'),

    path('instrument/<int:instrument_id>', viewer_views.home, name='instrument'),
    path('instrument/<int:instrument_id>/reports', viewer_views.reports, name='instrument_reports'),
    path('instrument/<int:instrument_id>/report/<int:report_id>', viewer_views.report, name='instruments_report'),
    path('instrument/<int:instrument_id>/tables', viewer_views.tables, name='instrument_tables'),
    path('instrument/<int:instrument_id>/stock', viewer_views.stock, name='instrument_stock'),

    path('trader/list', trader_views.list, name='trader_list'),

    path('portfolio/transactions', portfolio_views.transactions, name='portfolio_transactions'),
    path('portfolio/position', portfolio_views.current_position, name='portfolio_position'),
    path('portfolio/add_transaction', portfolio_views.add_transaction, name='portfolio_add'),
    path('portfolio/process_add_transaction', portfolio_views.process_add_transaction, name='portfolio_process_add_transaction')

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)