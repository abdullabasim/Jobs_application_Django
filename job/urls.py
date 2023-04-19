from django.urls import path,include
from . import views


urlpatterns = [
    path('jobs/', views.jobList.as_view(),name='jobs'),
    path('jobs/<str:pk>', views.jobDetail.as_view(),name='job'),

    path('stats/<str:topic>', views.getTopicStats,name='get_topic_stats'),
    path('jobs/<str:pk>/apply', views.applyToJob,name='get_topic_stats'),
    path('me/jobs/applied', views.getCurrentUserAppliedJobs, name='me_jobs_applied'),
    path('jobs/<str:pk>/check', views.isApplied, name='is_applied_job'),
    path('me/jobs', views.getCurrentUserJobs, name='me_jobs'),
    path('jobs/<str:pk>/candidates', views.getCandidateApplied, name='candidates_job_applied'),

]