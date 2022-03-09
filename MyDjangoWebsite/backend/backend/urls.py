from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from DavidsShop import views, forms, models
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'basket', views.BasketViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'users', views.APIUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DavidsShop.urls')),
    path('', views.index, name="homepage"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.UserSignUpView.as_view(), name="register"),
    path('basket/', views.show_basket, name="show_basket"),
    path('addbasket/<int:ProductID>', views.add_to_basket, name="add_basket"),
    path('addbasket2/<int:ProductID>', views.add_to_basket2, name="add_basket2"),
    path('remove_item/<int:SBI>', views.remove_item, name="remove_item"),
    path('order/', views.order, name="order"),
    path('orderhistory/', views.previous_orders, name="order_history"),
    path('login/', views.LoginView.as_view(template_name='login.html', authentication_form=forms.UserLoginForm), name='login'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apiregister/', views.UserRegistrationAPIView.as_view(), name="api_register"),
    path('apiadd/', views.AddBasketItemAPIView.as_view(), name="api_add_to_basket"),
    path('apiremove/', views.RemoveBasketItemAPIView.as_view(), name="api_remove_from_basket"),
    path('apicheckout/', views.CheckoutAPIView.as_view(), name="api_checkout")
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
