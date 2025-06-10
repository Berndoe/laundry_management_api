from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from accounts import views

# route for company only
company_router = DefaultRouter()
company_router.register('companies', views.CompanyViewSet, basename='company')

# route for employees and customers
router = DefaultRouter()
router.register('company/employees', views.EmployeeViewSet, basename='employee')
router.register('company/customers', views.CustomerViewSet, basename='customer')
auth_urls = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/password/reset', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

urlpatterns = []
urlpatterns += company_router.urls  # Add company routes first
urlpatterns += router.urls          # Add employee and customer routes
urlpatterns += auth_urls

