"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.menu_dashboard, name='menu_dashboard'),
    #path("admin/", admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    #ADMIN
    path('admin-dashboard/',views.admin_dashboard, name="admin_dashboard"),
    path('user-list/', views.user_list, name="user_list"),
    path('create-user/', views.create_user, name="create_user"),
    path('edit-user/<int:user_id>', views.edit_user, name="edit_user"),
    path('delete-user/<int:user_id>', views.delete_user, name="delete_user"),

    #PROFESOR
    path('professor-dashboard/', views.professor_dashboard, name="professor_dashboard"),
    path('create-document/', views.create_document, name="create_document"),
    path('document-list/', views.document_list, name="document_list"),
    path('share-document/<int:document_id>', views.share_document, name="share_document"),
    path('perform-share/<int:document_id>', views.perform_share, name="perform_share"),
    path('edit-document/<int:document_id>/', views.edit_document, name='edit_document'),
    path('delete-document/<int:document_id>', views.delete_document, name="delete_document"),


    #STUDENT
    path('student-dashboard/', views.student_dashboard, name="student_dashboard"),
    path('student/shared-documents/', views.student_shared_documents, name='student_shared_documents'),

    path('download/<int:doc_id>/', views.download_document, name='download_document'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
