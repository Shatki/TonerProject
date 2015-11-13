from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account

class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username')

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
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        user = super(AccountCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

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


class AccountAdmin(UserAdmin):
    list_display = ('username',
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
             (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'company_name',
                                             'user_photo', 'tagline')}),
            ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_company', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
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
    # change_password_form = AdminPasswordChangeForm

admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
