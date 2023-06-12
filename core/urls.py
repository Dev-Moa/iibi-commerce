from django.urls import path
from . import views
urlpatterns = [
     # _______________________PRODUCT URLS____________________________________________________________
    path('',views.IndexView.as_view(),name="home"),
    path('signup',views.SignUpView.as_view(),name="signup"),
    path('products/add',views.CreateProduct.as_view(),name="create-product"),
    path('products/',views.RetrieveProduct.as_view(),name="products"), 
    path('products/<int:id>',views.DetailProduct.as_view(),name="product_detail"),
    path("product/<int:id>/update", views.UpdateProduct.as_view(), name="update-product"),
    path('products/<int:id>/delete',views.DeleteProduct.as_view(),name="delete-product"),
    # _______________________OTHER URLS____________________________________________________________
    path('products/<int:id>/profile',views.UserProfile.as_view(),name="profile"),
    path('category/<str:name>',views.CategoryDetail.as_view(),name="category_detail"),
    path('carts/',views.AddToCart.as_view(),name="cart-list"),
    path('remove-cart/<int:id>',views.RemoveCart.as_view(),name="remove-cart")
]
