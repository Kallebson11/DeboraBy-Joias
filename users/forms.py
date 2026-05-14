# users/forms.py
from django import forms
from django.contrib.auth.models import User


class PasswordRecoveryForm(forms.Form):
    """Formulário para recuperação/redefinição de senha"""
    username         = forms.CharField(label='Usuário', max_length=100)
    new_password     = forms.CharField(label='Nova senha',       widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário não encontrado.")
        return username

    def clean_new_password(self):
        """
        Aplica as mesmas regras dos validators customizados,
        pois forms.Form simples não passa pelo AUTH_PASSWORD_VALIDATORS.
        """
        password = self.cleaned_data.get('new_password')
        if not password:
            return password

        # Mínimo de 8 caracteres
        if len(password) < 8:
            raise forms.ValidationError(
                "A senha deve ter pelo menos 8 caracteres."
            )

        # Pelo menos uma letra maiúscula
        if not any(c.isupper() for c in password):
            raise forms.ValidationError(
                "A senha deve conter pelo menos uma letra maiúscula (A-Z)."
            )

        # Pelo menos uma letra minúscula
        if not any(c.islower() for c in password):
            raise forms.ValidationError(
                "A senha deve conter pelo menos uma letra minúscula (a-z)."
            )

        # Não pode ser só números
        if password.isdigit():
            raise forms.ValidationError(
                "A senha não pode ser composta apenas por números."
            )

        # Pelo menos um caractere especial
        special_chars = set('!@#$%&*()_+-=[]{}|;:,.<>?')
        if not any(c in special_chars for c in password):
            raise forms.ValidationError(
                "A senha deve conter pelo menos um caractere especial (!@#$%...)."
            )

        # Sem espaços
        if ' ' in password:
            raise forms.ValidationError(
                "A senha não pode conter espaços."
            )

        return password

    def clean(self):
        cleaned_data     = super().clean()
        new_password     = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data