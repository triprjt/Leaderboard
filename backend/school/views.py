from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student
from .serializers import StudentSerializer
from datetime import timedelta
from django.utils.timezone import now
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import render

def index(request):
        return render(request, 'index.html')

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer    

    

    def get_queryset(self):
        queryset = Student.objects.all().order_by('-points')
        return queryset

    @action(detail=False, methods=['get'])
    def by_roll_no(self, request):
        roll_no = request.query_params.get('roll_no', None)
        if roll_no is not None:
            queryset = Student.objects.filter(roll_no=roll_no)
            queryset = queryset.order_by('-points')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Roll number is not provided."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_filter(self, request):
        filter_type = request.query_params.get('type', None)
        filter_value = request.query_params.get('value', None)
        # print('type' + filter_type + 'value' + filter_value)
        if filter_type is not None and filter_value is not None:
            queryset = Student.objects.filter(**{filter_type: filter_value})
            queryset = queryset.order_by('-points')
        else:
            queryset = Student.objects.all().order_by('-points')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_friends(self, request):
        roll_no = request.query_params.get('roll_no', None)
        if roll_no is not None:
            student = Student.objects.get(roll_no=roll_no)
            queryset = student.friends.all()
            friends_serializer = self.get_serializer(queryset, many=True)

            # Use the same serializer to serialize the student
            student_serializer = self.get_serializer(student)

            # Return both serialized student and friends in the response
            return Response({
                'student': student_serializer.data,
                'friends': friends_serializer.data
            })

        else:
            return Response({"error": "Roll number is not provided."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_timeframe(self, request):
        timeframe = request.query_params.get('timeframe', 'all')
        if timeframe == 'week':
            start_date = now() - timedelta(days=7)
            queryset = Student.objects.filter(updated_at__gte=start_date)
        else:
            queryset = Student.objects.all()
        queryset = queryset.order_by('-points')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_points(self, request, pk=None):
        student = self.get_object()
        points = request.data.get('points', None)
        if points is not None:
            try:
                points = int(points)
                student.update(points=points)
                return Response({"message": f"Points updated for student with roll number {student.roll_no}."}, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "Points value must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error: Incomplete data provided"}, status=status.HTTP_400_BAD_REQUEST)
