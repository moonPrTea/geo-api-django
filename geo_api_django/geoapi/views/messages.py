from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import (
    InputMessageCreateSerializer,
    OutputMessageCreateSerializer
)

class MessageCreateApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        message_data = InputMessageCreateSerializer(
            data = request.data,
            context={'request': request}
        )
        
        message_data.is_valid(raise_exception=True)
        
        new_message = message_data.save()
        message_content = OutputMessageCreateSerializer(new_message)
        return Response(
            {
                'message': "message successfully created",
                "object": message_content.data
            },
        )