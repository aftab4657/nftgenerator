from django.urls import path
from . import views

urlpatterns = [
    path('', views.layers, name='layers'),
    # path('', views.generate_nfts_Layers, name='generate_nfts_layer'),
    path('generate-nfts/', views.generate_nfts, name='generate_nfts'),
    path('get_details/', views.get_task_status, name='get-task-status'),
    path('download_nfts/', views.download_nfts, name='download_nfts'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('upload/', views.upload_file, name='upload_file'),
    path('logout/', views.logout, name='logout'),
    path('layers/', views.layers, name='layers'),
    path('upload-layers/', views.upload_layers, name='upload_layers'),
    path('generate-nfts-layers', views.generate_nfts_Layers, name='generate_nfts_layer'),
    path('upload-ipfs-server', views.upload_on_ipfs_server, name='upload_ipfs_server'),
    path('run-command', views.run_command, name = "run-command"),
    #  path('upload-ipfs/', views.upload_ipfs_server, name='upload-ipfs-server')
    # path('generate-nfts-layers/<int:id>', views.generate_nfts_Layers, name='generate_nfts_layer'),

]
