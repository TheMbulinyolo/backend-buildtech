from rest_framework import generics, permissions
from .models import Participant
from .serializers import ParticipantSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.core.mail import send_mail
from django.conf import settings

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