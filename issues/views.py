import json

from django.shortcuts import render
from issues.models import Reporter, Issue
from django.conf import settings
from django.http import JsonResponse

def view_reporters(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    file_path = settings.BASE_DIR / "reporters.json"
    with open(file_path, "r", encoding="utf-8") as file:
        reporters = json.load(file)

    reporter_id = request.GET.get("id")
    if reporter_id is None:
        return JsonResponse(reporters, safe=False)

    try:
        reporter_id = int(reporter_id)
    except ValueError:
        return JsonResponse({"error": "id must be an integer"}, status=400)

    reporter = next((r for r in reporters if r["id"] == reporter_id), None)
    if reporter is None:
        return JsonResponse({"error": "Reporter not found"}, status=404)

    return JsonResponse(reporter,safe=False)


def view_issues(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    file_path = settings.BASE_DIR / "issues.json"
    with open(file_path, "r", encoding="utf-8") as file:
        issues = json.load(file)

    issue_id = request.GET.get("id")
    if issue_id is not None:
        try:
            issue_id = int(issue_id)
        except ValueError:
            return JsonResponse({"error": "id must be an integer"}, status=400)

        issue = next((i for i in issues if i["id"] == issue_id), None)
        if issue is None:
            return JsonResponse({"error": "Issue not found"}, status=404)
        return JsonResponse(issue)

    status = request.GET.get("status")
    if status is not None:
        issues = [i for i in issues if i["status"] == status]

    return JsonResponse(issues, safe=False)


def get_reporters_by_id(request, reporter_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    file_path = settings.BASE_DIR / "reporters.json"
    with open(file_path,"r") as f:
        reporters = json.load(f);
    reporter = next((r for r in reporters if r["id"] == reporter_id), None)
    if reporter is None:
        return JsonResponse({"error": "Reporter not found"}, status=404)
    return JsonResponse(reporter, safe=False)
def get_issues_by_id(request, issue_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    file_path = settings.BASE_DIR / "issues.json"
    with open(file_path,"r") as f:
        issues = json.load(f);
    issue = next((i for i in issues if i["id"] == issue_id), None)
    if issue is None:
        return JsonResponse({"error": "Issue not found"}, status=404)
    return JsonResponse(issue, safe=False)
def get_issues_by_status(request, status):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    file_path = settings.BASE_DIR / "issues.json"
    with open(file_path,"r") as f:
        issues = json.load(f);
    filtered_issues = [i for i in issues if i["status"] == status]
    return JsonResponse(filtered_issues, safe=False)