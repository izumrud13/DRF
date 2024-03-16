from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from training.models import Course, Lesson
from training.permissions import IsModerator, IsOwner
from training.serializers import CourseSerializers, LessonSerializers


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
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


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
