from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class':"btn-none", "type":"button", "style":"position:absolute;left:-9999px;"}),
    )


class ImageUploadForm(forms.Form):
    image = forms.ImageField()