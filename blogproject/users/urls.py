from django.conf.urls import url

from  . import views


app_name = 'users'
urlpatterns=[
    url(r'^register/',views.register,name='register'),
    # url(r'^$', 'blog.views.index', name='index'),
]