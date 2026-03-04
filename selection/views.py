"""Views for selections app"""

# from django.contrib.auth.decorators import login_required

from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .models import Selection, Verse, VerseRange


class SelectionView(LoginRequiredMixin, View):
    def post(self, request, id):
        """Edit a selection"""
        # Todo: Use graphql to make easier
        data = request.POST
        return redirect(request.path)

    def get(self, request, id):
        selection = Selection.objects.get(id=id)
        ranges_payload = []
        for verse_range in VerseRange.objects.filter(selection=selection):
            verses_objs = Verse.objects.filter(
                id__gte=verse_range.start.id, id__lte=verse_range.end.id
            )
            # Also get hidden and all
            verses = [verse.to_dict(selection.version) for verse in verses_objs]
            ranges_payload.append(verses)

        return render(
            request,
            "selection.html",
            context={"ranges": ranges_payload, "selection": selection.to_dict()},
        )


class SelectionsView(LoginRequiredMixin, View):
    def post(self, request):
        """Will create a selection from the multiple VerseRanges given"""
        # Todo: Create ModelForm for Selection verification
        data = request.POST
        options = {"start": [], "end": []}
        props = ["book", "chapter", "verse"]

        for range_type, vals in options.items():
            for opt_vals in zip(
                *[data.getlist(f"{range_type}_{prop}") for prop in props]
            ):
                vals.append(dict(zip(props, opt_vals)))

        new_selection = Selection(
            user=request.user,
            label=data.get("label"),
            repeat=data.get("repeat"),
            version=data.get("version"),
        )
        new_selection.save()

        for starts, ends in zip(*options.values()):
            VerseRange(
                start=Verse.objects.get(**starts),
                end=Verse.objects.get(**ends),
                selection=new_selection,
            ).save()

        return redirect(f"/selections/{new_selection.id}/")

    def get(self, request):
        data = request.GET
        # Use the GET parameters to get parameters to streamline selections
        # Use page-based pagination to get selections to display
        return render(request, "selections.html")
