from django.urls import path
from . import views

urlpatterns = [
    # path('', views.bulk_upload_form, name="display_form"),
    path('', views.campaign_list, name="campaign_list"),
    path('campaign/update/<int:id>', views.update_campaign_status, name="update_campaign_status"),
    path('campaign/create', views.campaign_create, name="campaign_create"),
    path('campaign/details/<int:id>', views.campaign_detail, name="campaign_detail"),
    path('upload/recipient', views.upload_bulk_recipent, name="validate_upload_file"),
]