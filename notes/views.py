from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Note


def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/list.html', {'notes': notes})


@require_http_methods(["POST"])
def note_create(request):
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    if title:
        Note.objects.create(title=title, content=content)
    return redirect('note_list')


def health_check(request):
    """Simple endpoint used by CI/CD & container orchestrators to verify
    the app (and its DB connection) is up."""
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "ok"
    except Exception as exc:  # pragma: no cover
        db_status = f"error: {exc}"
    return JsonResponse({"status": "ok", "database": db_status})
