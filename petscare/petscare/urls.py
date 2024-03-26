"""
URL configuration for petscare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from petsapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about',views.about),
    path('contact',views.contact),
    path('services',views.services),

    path('log', views.log),
    path('reg1', views.uregister),
    path('reg2',views.cregister),
    path('uprofile', views.uprofile),
    path('cprofile1', views.cprofile),
    path('aprofile', views.aprofile),

    path('req',views.request),
    path('update',views.update),
    path('delete',views.delete),
    path('viewcare',views.viewcare),
    path('viewuser',views.viewusers),

    path('cpswd',views.changepswd),
    path('umyprof',views.umyprof),
    path('uedit',views.uedit),
    path('userupdate',views.userupdate),
    path('locfil',views.locfil),

    path('cmyprof',views.cmyprof),
    path('cedit',views.cedit),
    path('ctupdate',views.ctupdate),
    path('feed',views.feed),
    path('vfeed',views.viewfeed),
    path('avfeed',views.advfeed),

    path('adddetails',views.add_details),
    path('viewdetails',views.view_details),
    path('dct',views.detailsct),
    path('deleteserv',views.deleteserv),
    path('care/<a>', views.care),

    path('booking',views.book),
    path('viewbooking',views.viewbooking),
    path('advbook',views.advbook),
    path('vbct',views.viewbookingct),
    path('accept',views.accept),
    path('reject',views.reject),

    path('ctvu',views.ctviewbyuser),
    path('det',views.det),

    path('payment/<int:id>',views.payment),
    path('pay/<int:id>',views.pay),

    path('wait',views.wait),
    path('paycancel',views.can),

    path('logout',views.logout),
    path('logout2',views.logout2),

    path("success",views.success),
    path('vadpay',views.adpaytot),
    path('ctpaytot',views.ctpaytot),

    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),
    path('comp',views.comp),
    path('acom',views.vcompadmin),
    path('ucom',views.vcompuser),
    path('warning',views.warning),
    path('ctwarning',views.ctwarning),
    path('deletect',views.deletect),


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)