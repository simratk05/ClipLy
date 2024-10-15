
from django.urls import path
from .import views

urlpatterns = [
    path('',views.homepage,name=""),
    path('register',views.register,name="register"),
    path('my-login',views.my_login,name="my-login"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('add_bookmark/', views.add_bookmark, name='add_bookmark'),
    path('user-logout',views.user_logout,name="user-logout"),
    path('my_bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('update_bookmarks/<str:pk>', views.update_bookmarks, name='update_bookmarks'),
    path('delete_bookmark/<str:pk>', views.delete_bookmark, name='delete_bookmark'),
    path('save_bookmark', views.save_bookmark, name='save_bookmark'),
    path('profile', views.profile, name='profile'),
    path('delete_account', views.delete_account, name='delete_account'),
    # path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
