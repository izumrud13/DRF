from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import UserListAPIView, UserCreateAPIView, UserDetailAPIView, UserUpdateAPIView, UserDestroyAPIView


app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-get'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('payment/', views.PaymentListView.as_view(), name='payments'),
]