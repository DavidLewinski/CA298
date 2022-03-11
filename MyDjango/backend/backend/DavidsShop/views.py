from django.shortcuts import render, redirect
from django.views.generic import CreateView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import *
from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from .forms import *

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class BasketViewSet(viewsets.ModelViewSet):
  serializer_class = BasketSerializer
  queryset = Basket.objects.all()
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
      user = self.request.user # get the current user
      if user.is_superuser:
          return Basket.objects.all() # return all the baskets if a superuser requests
      else:
          # For normal users, only return the current active basket
          shopping_basket = Basket.objects.filter(UserID=user, is_active=True)
          return shopping_basket

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user # get the current user
        if user.is_superuser:
            return Order.objects.all() # return all the baskets if a superuser requests
        else:
            # For normal users, only return the current active basket
            orders = Order.objects.filter(UserID=user)
            return orders

class RemoveBasketItemAPIView(generics.CreateAPIView):
    serializer_class = RemoveBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

class CheckoutAPIView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = APIUser.objects.all()
    serializer_class = APIUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

def homepage(request):
    return render(request, "homepage.html")

def index(request):
    products = Product.objects.all()
    return render(request, "homepage.html", {"products": products})

def product(request, ProductID):
    product = Product.objects.get(id=ProductID)
    return render(request, "product.html", {"product": product})

def product_individual(request, ProductID):
    product = Product.objects.get(id=ProductID)
    return render(request, "product_individual.html", {"product": product})

# def search(request):
#     searched = request.POST["searched"]
#     search = Product.objects.filter(ProductID_contains=searched)
#     return render(request, ".html", {"searched":searched, "search":search})

class UserSignUpView(CreateView):
    model = APIUser
    form_class = UserSignUpForm
    template_name = "user_register.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")

class UserLoginView(LoginView):
    template_name = "login.html"

def logout_user(request):
    logout(request)
    return redirect("/")

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] #No login is needed to access this route
    queryset = APIUser.objects.all()

class AddBasketItemAPIView(generics.CreateAPIView):
    serializer_class = AddBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

@login_required
def add_to_basket(request, ProductID):
    user = request.user
    basket = Basket.objects.filter(UserID=user, is_active=True).first()
    if basket is None:
        Basket.objects.create(UserID = user)
        basket = Basket.objects.filter(UserID=user, is_active=True).first()
    product = Product.objects.get(id=ProductID)
    SBI = BasketItem.objects.filter(BasketID=basket, ProductID = product).first()
    if SBI is None:
        SBI = BasketItem(BasketID=basket, ProductID = product)
        SBI.save()
    else:
        SBI.Quantity = SBI.Quantity + 1
        SBI.save()
    products = Product.objects.all()
    return render(request, "homepage.html", {"products": products, "added":ProductID})

@login_required
def add_to_basket2(request, ProductID):
    user = request.user
    basket = Basket.objects.filter(UserID=user, is_active=True).first()
    if basket is None:
        Basket.objects.create(UserID = user)
        basket = Basket.objects.filter(UserID=user, is_active=True).first()
    product = Product.objects.get(id=ProductID)
    SBI = BasketItem.objects.filter(BasketID=basket, ProductID = product).first()
    if SBI is None:
        SBI = BasketItem(BasketID=basket, ProductID = product)
        SBI.save()
    else:
        SBI.Quantity = SBI.Quantity + 1
        SBI.save()
    return render(request, "product_individual.html", {"product": product, "added":True})

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(UserID=user, is_active=True).first()
    if basket is None:
        return render(request, "basket.html", {"empty":True})
    else:
        SBI = BasketItem.objects.filter(BasketID=basket)
        if SBI.exists():
            total = 0.00
            for item in SBI:
                total += float(item.Price())
            return render(request, "basket.html", {"basket":basket, "SBI":SBI, "total":total})
        else:
            return render(request, "basket.html", {"empty":True})

@login_required
def remove_item(request, SBI):
    basketitem = BasketItem.objects.get(id=SBI)
    if basketitem is None:
        return redirect("/basket")
    else:
        if basketitem.Quantity > 1:
            basketitem.Quantity = basketitem.Quantity - 1
            basketitem.save()
        else:
            basketitem.delete()
    return redirect("/basket")

@login_required
def order(request):
    user = request.user
    basket = Basket.objects.filter(UserID=user, is_active=True).first()
    if basket is None:
        return redirect("/basket/")
    SBI = BasketItem.objects.filter(BasketID=basket)
    if not SBI.exists():
        return redirect("/basket/")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.UserID = user
            order.BasketID = basket
            total = 0.00
            for item in SBI:
                total += float(item.Price())
            order.TotalPrice = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, "ordercomplete.html", {"order":order, "basket":basket, "SBI":SBI})
        else:
            total = 0.00
            for item in SBI:
                total += float(item.Price())
            return render(request, "order.html", {"form":form, "basket":basket, "SBI":SBI, "total":total})
    else:
        total = 0.00
        for item in SBI:
            total += float(item.Price())
        form = OrderForm()
        return render(request, "order.html", {"form":form, "basket":basket, "SBI":SBI, "total":total})

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(UserID=user)
    return render(request, 'orderhistory.html', {'orders':orders})