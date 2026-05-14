# users/validators.py
from django.core.exceptions import ValidationError


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f'A senha deve ter pelo menos {self.min_length} caracteres.',
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ''  # ← vazio: Django não exibe nada no formulário


class NoNumericOnlyValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                'A senha não pode ser composta apenas por números.',
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return ''


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(c.isupper() for c in password):
            raise ValidationError(
                'A senha deve conter pelo menos uma letra maiúscula (A-Z).',
                code='password_no_upper',
            )

    def get_help_text(self):
        return ''


class LowercaseValidator:
    def validate(self, password, user=None):
        if not any(c.islower() for c in password):
            raise ValidationError(
                'A senha deve conter pelo menos uma letra minúscula (a-z).',
                code='password_no_lower',
            )

    def get_help_text(self):
        return ''


class SpecialCharValidator:
    SPECIAL_CHARS = set('!@#$%&*()_+-=[]{}|;:,.<>?')

    def validate(self, password, user=None):
        if not any(c in self.SPECIAL_CHARS for c in password):
            raise ValidationError(
                'A senha deve conter pelo menos um caractere especial (!@#$%&*...).',
                code='password_no_special',
            )

    def get_help_text(self):
        return ''


class NoSpacesValidator:
    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(
                'A senha não pode conter espaços.',
                code='password_has_spaces',
            )

    def get_help_text(self):
        return ''


class NoUsernameSimilarityValidator:
    def validate(self, password, user=None):
        if user and user.username:
            if user.username.lower() in password.lower():
                raise ValidationError(
                    'A senha não pode ser igual ou conter seu nome de usuário.',
                    code='password_contains_username',
                )

    def get_help_text(self):
        return ''