from rest_framework import viewsets
from .serializer import ProblemsSerializer, ReplySerializer
from .models import ProblemsModel, ReplyModel

class ProblemsViewSet(viewsets.ModelViewSet):
    queryset = ProblemsModel.objects.all()
    serializer_class = ProblemsSerializer

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = ReplyModel.objects.all()
    serializer_class = ProblemsSerializer