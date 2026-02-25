from django.urls import path
from . import views


urlpatterns = [
    
    path("", views.transaction_list),
    path("login/", views.login_view),
   
    path("edit/<int:txn_id>/", views.edit_transaction),   # ✅ ADD THIS
    path("monthly/", views.monthly_summary),
    path("logout/", views.logout_view),                    # (see issue 2)
]