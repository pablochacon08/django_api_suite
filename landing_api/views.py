from datetime import datetime

from firebase_admin import db
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_entries"

    def get(self, request):
        try:
            ref = db.reference(self.collection_name)
            data = ref.get() or []
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data.copy()
            ref = db.reference(self.collection_name)
            current_time = datetime.now()
            custom_format = (
                current_time.strftime("%d/%m/%Y, %I:%M:%S %p")
                .lower()
                .replace("am", "a. m.")
                .replace("pm", "p. m.")
            )
            data.update({"timestamp": custom_format})
            new_resource = ref.push(data)
            return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
