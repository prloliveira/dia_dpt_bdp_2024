from django.urls import include, path
from polls.views import *
urlpatterns = [
    path('', data_collection_view, name='data_collection'),
    path('grafico/', graph_view, name='graph_page'),
    path('bar-chart-data/', bar_chart_data_view, name='bar_chart_data'),
    path('chart-data/', chart_data_questions, name='chart_data_questions'),
    path('dummy/', create_dummy_data, name='create_dummy_data'),
    path("__reload__/", include("django_browser_reload.urls")),
]