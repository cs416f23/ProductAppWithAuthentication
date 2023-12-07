from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.create_product, name='create_product'),
    path('update/<int:product_id>', views.update_product, name='update_product'),
    path('delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('search/', views.search_product, name='search_product'),
    path('delete/', views.delete_product_with_ajax, name='delete_product_with_ajax'),

]
# Necessary for images to be loaded correctly
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)