from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from requests_oauthlib import OAuth2Session, OAuth1Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from django.conf import settings
from .serializers import VendorSerializer, AddressSerializer
from .models import Address, User
# Create your views here.


class CreateVendorView(CreateAPIView):

    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        if request.user.vendor.first():
            return Response(
                {"error": "Already vendor account exists with your account"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddressView(CreateAPIView, ListAPIView):

    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddressUpdate(RetrieveUpdateDestroyAPIView):

    serializer_class = AddressSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        uid = self.kwargs[self.lookup_field]
        return Address.objects.filter(user=self.request.user, uid=uid)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GoogleOAuth2(APIView):
    """
    Login with Google OAuth2
    """

    permission_classes = [AllowAny]

    def get(self, request):
        client_id = settings.GOOGLE_CLIENT_ID
        scope = settings.GOOGLE_OAUTH2_SCOPE
        redirect_uri = request.query_params.get('redirect_uri')
        if redirect_uri not in settings.SOCIAL_AUTH_ALLOWED_REDIRECT_URIS:
            return Response(
                {
                    'error': 'Wrong Redirect URI'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        google = OAuth2Session(client_id,
                               scope=scope,
                               redirect_uri=redirect_uri)
        authorization_url, state = google.authorization_url(
            settings.GOOGLE_AUTHORIZATION_BASE_URL,
            access_type='offline',
            prompt='select_account'
        )
        return Response({'authorization_url': authorization_url})

    def post(self, request):

        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET

        state = request.data.get('state')
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')

        google = OAuth2Session(
            client_id,
            redirect_uri=redirect_uri,
            state=state
        )
        try:
            google.fetch_token(
                settings.GOOGLE_TOKEN_URL,
                client_secret=client_secret,
                code=code,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        user_info = google.get(
            'https://www.googleapis.com/oauth2/v1/userinfo').json()
        user_email = user_info['email']
        user_name = user_info.get("name")
        if not user_name:
            user_name = "Jhon Doe"
        first, last = user_name.split(" ")[:2]
        try:
            user = User.objects.get(email=user_email)
            if user and user.auth_provider != 'google':
                return Response(
                    {"error": f"Please use {user.get_auth_provider_display()} to login."},
                    400)
        except User.DoesNotExist:
            # Create a user and assign provider to google
            user = User(email=user_email, first_name=first,
                        last_name=last, auth_provider='google', username=user_email)
            user.save()
        except Exception as e:
            return Response({"error": "User not found"}, 404)

        refresh_token = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        })


class FacebookOauth(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        client_id = settings.FACEBOOK_APP_ID
        redirect_uri = request.query_params.get('redirect_uri')
        if redirect_uri not in settings.SOCIAL_AUTH_ALLOWED_REDIRECT_URIS:
            return Response(
                {
                    'error': 'Wrong Redirect URI'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        facebook = OAuth2Session(
            client_id, redirect_uri=redirect_uri, scope="email,public_profile")
        authorization_url, state = facebook.authorization_url(
            settings.FACEBOOK_AUTHORIZATION_BASE_URL,
        )
        return Response({'authorization_url': authorization_url})

    def post(self, request):

        client_id = settings.FACEBOOK_APP_ID
        client_secret = settings.FACEBOOK_APP_SECRET

        state = request.data.get('state')
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')

        facebook = OAuth2Session(
            client_id,
            redirect_uri=redirect_uri,
            state=state
        )
        facebook = facebook_compliance_fix(facebook)
        try:
            facebook.fetch_token(
                settings.FACEBOOK_TOKEN_URL,
                client_secret=client_secret,
                code=code,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        user_info = facebook.get(
            'https://graph.facebook.com/v19.0/me?fields=first_name,last_name,email'
        ).json()
        user_email = user_info['email']
        first, last = user_info['first_name'], user_info['last_name']
        try:
            user = User.objects.get(email=user_email)
            if user and user.auth_provider != 'facebook':
                return Response(
                    {"error": f"Please use {user.get_auth_provider_display()} to login."},
                    400)
        except User.DoesNotExist:
            # Create a user and assign provider to google
            user = User(email=user_email, first_name=first,
                        last_name=last, auth_provider='facebook', username=user_email)
            user.save()
        except Exception as e:
            return Response({"error": "User not found"}, 404)

        refresh_token = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        })
