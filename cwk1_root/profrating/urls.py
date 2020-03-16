

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'ModuleInstance', views.ModuleInstanceViewSet)
router.register(r'Module', views.ModuleViewSet)
router.register(r'Professor', views.ProfessorViewSet)
router.register(r'ratings', views.RatingViewSet)

urlpatterns = [
    #path('', views.index, name='index'),
    path('profrating/register/', views.create_user, name='create_user'),
    path('profrating/login/', views.user_login, name='user_login'),
    path('profrating/logout/', views.logout_request, name='logout_request'),
    path('profrating/module/', views.GetModule, name='get_module'),
    path('profrating/professor/', views.GetProfessors, name='get_professor'),
    path('profrating/moduleinstance/', views.GetModuleInstance, name='get_moduleInstance'),
    path('profrating/rating/', views.GetRating, name='GetRating'),
    path('profrating/modrating/', views.moduleAvgRating, name='moduleAvgRating'),
    path('profrating/ovrrating/', views.overallAvgRating, name='overallAvgRating'),
    path('profrating/postrating/', views.postRating, name='postRating'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))


]
