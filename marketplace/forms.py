from django import forms
from django.contrib.auth import get_user_model
from .models import Offering, Trade, Gang, Hobby

class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['offering_type', 'name', 'hobby', 'description', 'stock_status']

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['offered_offering', 'quantity', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['offered_offering'].queryset = Offering.objects.filter(owner=user)


class GangForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        queryset = get_user_model().objects.all().order_by('username')
        if user and user.is_authenticated:
            queryset = queryset.exclude(id=user.id)
        self.fields['members'].queryset = queryset

    class Meta:
        model = Gang
        fields = ['name', 'description', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }


class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ['output_type', 'name']