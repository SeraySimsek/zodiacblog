from django.urls import path
#from burcblog import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.homepage,name="homepage"),
    path('homepage/',views.homepage, name="homepage"),
    path('astrolojitarihi/',views.astrolojitarihi,name="astrolojitarihi"),
    path('tarot/',views.tarot, name="tarot"),
    path('yukselenhesaplama/',views.yukselenhesapla, name="yukselenhesaplama"),
    path('burcuyumu/',views.burcuyumu, name="burcuyumu"),
    path('testler/',views.testler, name="testler"),
    path('burclar/', views.burclar, name="burclar"),
    path('burchesaplama/', views.burchesaplama, name="burchesaplama"),
    path('evethayır/', views.evethayır, name="evethayır"),
    path('hakkımızda/', views.hakkımızda, name="hakkımızda"),
    path('iletişim/', views.iletişim, name="iletişim"),
    path('bilgitesti/', views.bilgitesti, name="bilgitesti"),
    path('meslek/', views.meslek, name="meslek"),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('register/', views.register, name="register"),
    path('logout/', LogoutView.as_view(next_page='homepage'), name="logout"),


    path('koc/',views.koc, name="koc"),
    path('boga/', views.boga, name="boga"),
    path('akrep/',views.akrep, name="akrep"),
    path('aslan/',views.aslan, name="aslan"),
    path('balık/',views.balık, name="balık"),
    path('başak/',views.başak, name="başak"),
    path('ikizler/',views.ikizler, name="ikizler"),
    path('kova/',views.kova, name="kova"),
    path('oglak/',views.oglak, name="oglak"),
    path('terazi/',views.terazi, name="terazi"),
    path('yay/',views.yay, name="yay"),
    path('yengeç/',views.yengeç, name="yengeç"),

    path('shopping/', views.shopping, name="shopping"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('kahveFalı/', views.kahveFalı, name="kahveFalı"),
    path('hesapayarları/', views.hesapayarları, name="hesapayarları"),
    path('YeniGonderi/', views.add_new_post_page, name='add_new_post'),
    path('BurcYorumum/', views.view_zodiac, name='view_zodiac'),
    path('FalYorumum/', views.view_fortune_telling, name='view_fortune_telling'),
    path('error/', views.error_page, name='error'),
]