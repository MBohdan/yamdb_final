from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                          RegisterView, ReviewViewSet, TitleViewSet, TokenView,
                          UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="Users")
router_v1.register(r"genres", GenreViewSet, basename="GenreModel", )
router_v1.register(r"categories", CategoryViewSet, basename="CategoryModel", )
router_v1.register(r"titles", TitleViewSet, basename="TitleModel"),
router_v1.register(r"titles/(?P<title_id>\d+)/reviews",
                   ReviewViewSet, basename="ReviewModel")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet, basename="CommentModel", )

urlpatterns_WHY = [
    path('email/', RegisterView.as_view(),
         name='get_confirmation_code'),
    path('token/', TokenView.as_view(), name='get_token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(urlpatterns_WHY))
]
