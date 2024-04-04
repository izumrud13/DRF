from django.http import Http404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from training.models import Course, Lesson, Subscription
from training.pagination import CourseAndLessonPagination
from training.permissions import IsModerator, IsOwner
from training.serializers import CourseSerializers, LessonSerializers, SubscriptionSerializer
from users.serializers import UserSerializer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    pagination_class = CourseAndLessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания подписки"""
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """Присваивание подписки к текущему курсу и пользователю"""
        new_sub = serializer.save()
        new_sub.user = self.request.user
        course_pk = self.kwargs.get('pk')
        new_sub.course = Course.objects.get(pk=course_pk)
        new_sub.save()
        queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления подписки"""
    queryset = Subscription.objects.all()


class SubscriptionView(APIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request):
        user = self.request.user
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        name = request.data.get('name')

        if name is None:
            return Response({"message": "name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(name=name)
        except Course.DoesNotExist:
            raise Http404('Course not found')

        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        return Response({"message": message, 'user': user_data})

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()
