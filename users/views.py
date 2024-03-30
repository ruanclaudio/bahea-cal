from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.models import Team


@require_http_methods(["POST"])
def confirm(request):
    if not request.user.is_authenticated:
        raise BadRequest("Usuário não autenticado")

    if not (subscription := request.POST.get("subscription")):
        raise BadRequest("Inscrição não informada")

    try:
        team = Team.objects.get(ref=subscription)
    except Team.DoesNotExist:
        raise BadRequest("Inscrição não encontrada")
    else:
        request.user.subscriptions.add(team)

    return render(request, "users/confirmed.html")