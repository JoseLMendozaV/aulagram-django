from django import forms

from .models import Comment, Post


INPUT_CLASS = (
    "mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 "
    "outline-none focus:border-fuchsia-500 focus:ring-2 focus:ring-fuchsia-100"
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("image", "caption")
        widgets = {"caption": forms.Textarea(attrs={"rows": 4, "class": INPUT_CLASS})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs["class"] = INPUT_CLASS

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("La imagen no puede pesar mas de 5 MB.")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "class": "w-full border-0 bg-transparent text-sm outline-none focus:ring-0",
                    "placeholder": "Agrega un comentario...",
                    "aria-label": "Comentario",
                }
            )
        }
