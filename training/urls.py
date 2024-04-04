from django.urls import path

from training.apps import TrainingConfig
from rest_framework.routers import DefaultRouter

from training.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView, SubscriptionView

app_name = TrainingConfig.name
router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('courses/create_sub/<int:pk>/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('courses/delete_sub/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
] + router.urls
