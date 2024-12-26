from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import StartUpProfileSerializer, InvestorProfileSerializer


class InvestorRegistrationView(CreateAPIView):
    serializer_class = InvestorProfileSerializer
    permission_classes = [AllowAny]


class StartupRegistrationView(CreateAPIView):
    serializer_class = StartUpProfileSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        context_data = request.data.get('context', {})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
