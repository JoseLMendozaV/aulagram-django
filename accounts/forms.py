from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, User


INPUT_CLASS = (
    "mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 "
    "outline-none transition focus:border-fuchsia-500 focus:ring-2 focus:ring-fuchsia-100"
)


class StyledFormMixin:
    """Anade clases Tailwind sin repetirlas en cada widget."""

    def apply_styles(self):
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs["class"] = INPUT_CLASS


class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(label="Correo electronico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email


class UserUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Nombre", "last_name": "Apellido"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()


class ProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "location", "website", "skills")
        widgets = {
            "avatar": forms.FileInput(),
            "bio": forms.Textarea(attrs={"rows": 3}),
            "skills": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()
        self.fields["avatar"].widget.attrs.update(
            {
                "class": "sr-only",
                "accept": "image/jpeg,image/png,image/webp,image/gif",
                "data-avatar-input": "",
            }
        )
        self.fields["bio"].widget.attrs.update(
            {"data-bio-input": "", "placeholder": "Cuenta algo sobre ti..."}
        )
        self.fields["skills"].widget.attrs.update(
            {"class": "h-4 w-4 rounded border-slate-300 text-fuchsia-600 focus:ring-fuchsia-500"}
        )


class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("role",)
        widgets = {"role": forms.Select(attrs={"class": INPUT_CLASS})}
