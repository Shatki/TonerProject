from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Account, Bank


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            Account._default_manager.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class BankChangeForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('bank_name',
                  'bank_address',
                  'bank_account',
                  'bank_bik',)


class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='password', help_text='There is no way to see this password.')

    class Meta:
        model = Account
        fields = ('username',
                  'email',
                  'password',
                  'is_admin',
                  'is_staff',
                  'is_company',
                  'user_permissions',)

    def clean_password(self):
        return self.initial['password']


class BankAdmin(UserAdmin):
    list_display = ('bank_name',
                    'bank_address',
                    'bank_account',
                    'bank_bik',)
    ordering = ('bank_name',)



@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('company_name',
                    'company_phone',
                    'username',
                    'email',
                    'is_staff',
                    'is_admin',
                    'is_company',
                    )

    list_filter = ('is_admin',
                   'is_staff',
                   'is_company',
                   )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name',
                                      'user_photo', 'tagline')}),
        ('Company info', {'fields': ('company_name', 'company_boss_first_name',
                                     'company_boss_second_name', 'company_boss_last_name',
                                     'company_inn', 'company_ogrn', 'company_okpo', 'company_okato',
                                     'company_phone', 'user_bank', 'user_bank_account')}),

        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_company', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_admin')
        }),
    )

    search_fields = ('username',
                     'email',
                     'company_name',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    form = AccountChangeForm
    add_form = AccountCreationForm


admin.site.unregister(Group)
admin.site.register(Bank)
