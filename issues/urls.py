from django.urls import path

from issues.views import get_issues_by_id, get_issues_by_status, view_reporters, view_issues, get_reporters_by_id
urlpatterns = [path("reporters/", view_reporters, name="view_reporters"),
               path("issues/", view_issues, name="view_issues"),
               path("reporters/<int:reporter_id>/", get_reporters_by_id, name="get_reporters_by_id"),
               path("issues/<int:issue_id>/", get_issues_by_id, name="get_issues_by_id"),
               path("issues/status/<str:status>/", get_issues_by_status, name="get_issues_by_status")]