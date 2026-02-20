"""Views for selections app"""

# from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .models import Selection, VerseRange


class SelectionView(LoginRequiredMixin, View):
    def post(self, request, id):
        """Edit a selection"""
        # Todo: Use graphql to make easier
        data = request.POST
        return redirect(request.path)

    def get(self, request, id):
        selection = Selection.objects.get(id)
        return render(request, "selection.html", context=selection)


class SelectionsView(LoginRequiredMixin, View):
    def post(self, request):
        """Will create a selection from the multiple VerseRanges given"""
        # Todo: Create ModelForm for Selection verification
        data = request.POST
        verse_starts, verse_ends = [*map(request.POST.getlist, ("start", "end"))]
        new_selection = Selection(
            user=request.user,
            label=data.get("label"),
            voice=data.get("voice"),
            repeat=data.get("repeat"),
            version=data.get("version"),
        )
        new_selection.save()
        for start_verse, end_verse in zip(verse_starts, verse_ends):
            VerseRange(start=start_verse, end=end_verse, selection=new_selection).save()

        return redirect(f"/selections/{new_selection.id}/")

    def get(self, request):
        data = request.GET
        # Use the GET parameters to get parameters to streamline selections
        # Use page-based pagination to get selections to display
        return render(request, "selections.html")
