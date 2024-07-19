import xword_data.models
from django import forms


class AnswerForm(forms.Form):
    answer = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "placeholder": "Answer",
            }
        )
    )

    clue_id = forms.CharField(widget=forms.HiddenInput())

    def clean_answer(self):
        clue = xword_data.models.Clue.objects.get(pk=self.data.get("clue_id"))
        answer = self.cleaned_data.get("answer")

        if answer.lower() != clue.entry.entry_text.lower():
            raise forms.ValidationError("not correct")
        return answer
