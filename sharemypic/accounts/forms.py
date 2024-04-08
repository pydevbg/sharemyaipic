from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()

class SMPUserRegistrationForm(auth_forms.UserCreationForm):
    user = None

    class Meta:
        model = UserModel

        fields = ('username', 'password1',)
