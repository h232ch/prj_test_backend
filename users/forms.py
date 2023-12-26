from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput

from users.models import MyUser


class CustomUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""

    password1 = CharField(label="Password", widget=PasswordInput)
    password2 = CharField(
        label="Password confirmation", widget=PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ["email",]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        disabled password hash display field.
        """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ["email", "password"]