"""Views for selections app"""

# from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import Selection, VerseRange


class SelectionView(LoginRequiredMixin, View):
    def post(self, request):
        """Will create a selection from the multiple VerseRanges given"""
        # Todo: Create ModelForm for Selection
        data = request.POST
        user = request.user
        verse_starts, verse_ends = [*map(request.POST.getlist, ("start", "end"))]
        new_selection = Selection(
            user=user,
            label=data.get("label"),
            voice=data.get("voice"),
            repeat=data.get("repeat"),
            version=data.get("version"),
        )
        for start_verse, end_verse in zip(verse_starts, verse_ends):
            VerseRange(start=start_verse, end=end_verse, selection=new_selection)

    def get(self, request):
        return render(request, "selections.html")
