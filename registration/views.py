from rest_framework import generics, permissions , status
from .models import Participant
from .serializers import ParticipantSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import Participant
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

class ParticipantCreateView(generics.CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

class ParticipantListView(generics.ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAdminUser]

class ParticipantValidateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_update(self, serializer):
        # Update the participant's status to 'VALIDATED'
        instance = serializer.save(status='VALIDATED')

        # Send email notification to the participant
        subject = "Confirmation d'inscription - Validation réussie"
        message = (
            f"Bonjour {instance.first_name} {instance.last_name},\n\n"
            "Nous avons le plaisir de vous informer que votre inscription à Notre formation chez Modern Technology Building a été validée avec succès !\n"
            "Vous êtes maintenant un participant officiel !\n\n"
            "Cordialement,\n"
            "L'équipe d'administration !"
        )
        recipient_email = instance.email
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error if email sending fails (optional)
            print(f"Failed to send email to {recipient_email}: {str(e)}")


class UpdatePayementView(APIView):

    permissions_classes = [permissions.AllowAny]

    def post(self, request):

        email = request.data.get('email')
        validator = request.data.get('validator')
        if not email:
            return Response({'error':'Email is required '}, status=status.HTTP_400_BAD_REQUEST)
        
        participant = get_object_or_404(Participant, email = email )
        participant.status = 'PAID'
        participant.validator = validator
        participant.save(update_fields=['status','validator'])

        return Response(ParticipantSerializer(participant).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_email(request) :
    email = request.data.get('email')

    try:
        participant = Participant.objects.get(email=email)

        if participant.status in ['PAID', 'VALIDATED']:
            return Response({'status': 'paid'}, status=status.HTTP_200_OK)

        return Response({'status': 'exist'}, status=status.HTTP_200_OK)

    except Participant.DoesNotExist:
        return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)
