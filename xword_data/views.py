import xword_data.forms
import xword_data.models
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.


def drill(request):

    if request.method == "POST":
        form = xword_data.forms.AnswerForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(
                reverse(
                    "xword-answer", kwargs={"clue_id": form.cleaned_data.get("clue_id")}
                )
            )

        clue = get_object_or_404(xword_data.models.Clue, id=form.data.get("clue_id"))
    else:
        clue = (
            xword_data.models.Clue.objects.select_related("puzzle", "entry")
            .order_by("?")
            .first()
        )

        form = xword_data.forms.AnswerForm(initial={"clue_id": clue.id})

    if "clue_attempt_count" in request.session:
        request.session["clue_attempt_count"] += 1
    else:
        request.session["clue_attempt_count"] = 1

    context = {"form": form, "clue_id": clue.id, "clue": clue}
    return render(request, "xword-drill.html", context)


def answer(request, clue_id):
    clue = get_object_or_404(xword_data.models.Clue, id=clue_id)

    if "clue_attempt_count" not in request.session:
        request.session["clue_attempt_count"] = 0
        request.session["clue_correct_answered_count"] = 0

    if "clue_correct_answered_count" in request.session:
        if (
            request.session["clue_correct_answered_count"]
            < request.session["clue_attempt_count"]
        ):
            request.session["clue_correct_answered_count"] += 1
    else:
        request.session["clue_correct_answered_count"] = 1

    is_unique_appearance = (
        xword_data.models.Entry.objects.filter(entry_text=clue.entry.entry_text).count()
        == 1
    )

    context = {
        "clue": clue,
        "is_unique_appearance": is_unique_appearance,
        "clue_attempt_count": request.session["clue_attempt_count"],
        "clue_correct_answered_count": request.session["clue_correct_answered_count"],
        "entry_counts": xword_data.models.Clue.objects.select_related("puzzle", "entry")
        .all()
        .values("entry__entry_text")
        .annotate(count=Count("entry__entry_text"))
        .order_by("-count"),
    }

    return render(request, "xword-answer.html", context)
