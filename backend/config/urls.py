"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def root_view(request):
    return HttpResponse("Backend API is running smoothly!")


from django.contrib import admin
from django.urls import path, include
from social.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # first few paths mostly for authentication
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    # anyth that includes api/ redirect to the urls in the api app, then handle from there. 
    path("social/", include("social.urls")),
    path("social/accounts/", include("accounts.urls")),
    path('promotions/', include('promotions.urls')),
    path('/', root_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
