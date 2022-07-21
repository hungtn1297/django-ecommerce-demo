from django import forms
from .models import Customer

class RegisterForm(forms.Form):
    user_name = forms.CharField(label='Username', required=True)
    full_name = forms.CharField(label='Fullname', required=True)
    phone = forms.CharField(label='Phone', required=True, max_length=10)
    email = forms.CharField(label='Email', required=True, widget=forms.EmailInput)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat Password', required=True, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    user_name = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)


class PaymentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.order = kwargs.pop('order')
        super(PaymentForm, self).__init__(*args, **kwargs)
        customer_obj = Customer.objects.get(id=self.request.session['customer_id'])
        self.fields["customer_id"].initial = customer_obj.id
        if self.order:
            self.fields["full_name"].initial = self.order.full_name
            self.fields["phone"].initial = self.order.phone
            self.fields["email"].initial = self.order.email
            self.fields["address"].initial = self.order.address
            self.fields["full_name"].widget.attrs['readonly'] = True
            self.fields["email"].widget.attrs['readonly'] = True
            self.fields["address"].widget.attrs['readonly'] = True
            self.fields["phone"].widget.attrs['readonly'] = True

        else:
            self.fields["customer_id"].initial = customer_obj.id
            self.fields["full_name"].initial = customer_obj.full_name
            self.fields["phone"].initial = customer_obj.phone
            self.fields["email"].initial = customer_obj.email

    customer_id = forms.CharField(label='', widget=forms.HiddenInput)
    full_name = forms.CharField(label='Fullname', required=True)
    phone = forms.CharField(label='Phone', required=True, max_length=10)
    email = forms.CharField(label='Email', required=True, widget=forms.EmailInput)
    address = forms.CharField(label='Address', required=True)
