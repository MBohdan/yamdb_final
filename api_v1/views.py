from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          ReviewCommentPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadTitleSerializer,
                          ReviewSerializer, UserSerializer,
                          WriteTitleSerializer, CreateUserSerializer)
from .utils import send_mail_to_user

BASE_USERNAME = 'User'


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        username = serializer.data["username"]
        user, created = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail_to_user(email, confirmation_code)
        return Response({"email": email})


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'confirmation_code': 'Неверный код для данного email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdmin,)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)


# class SendCodeView(APIView):
#     def post(self, request):
#         code = default_token_generator.make_token(request.user)
#         email = self.request.data.get("email")
#         sender = os.getenv("EMAIL")
#         message = f"Confirmation code: {code}"
#         send_mail(
#             "Registration on yamdb",
#             message,
#             sender,
#             [email],
#             fail_silently=False,
#         )
#         return Response(status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return WriteTitleSerializer
        else:
            return ReadTitleSerializer


class GenreViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                   viewsets.GenericViewSet, ):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    lookup_field = "slug"


class CategoryViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                      viewsets.GenericViewSet, ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name", ]
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        queryset = get_object_or_404(Title,
                                     pk=self.kwargs['title_id']).reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(
            author=self.request.user, title_id=title.id,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        queryset = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"), ).comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"),
        )
        serializer.save(
            author=self.request.user,
            review_id=title.id
        )
