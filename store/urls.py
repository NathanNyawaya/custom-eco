from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.ads, name="ads"),
    path('search/', views.search, name='search'),
    path('store/', views.ads, name='ads'),
	path('store/', views.store, name='store'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('store/<str:id>', views.product_details, name="product_details"),
	path('search/<str:id>', views.product_details, name="product_details"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]