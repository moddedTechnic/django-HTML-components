from django.urls import include, path

from . import user

app_name = 'components'

urlpatterns = [
    path('user/login',  user.log_in,  name='login'),
    path('user/logout', user.log_out, name='logout'),
    path('user/signup', user.sign_up, name='signup'),
]
