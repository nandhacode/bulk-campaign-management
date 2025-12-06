from django import forms
from .models import Campaign
from django.utils import timezone
from datetime import timedelta

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ["name", "subject", "content", "scheduled_time", "status"]
        widgets = {
            "scheduled_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control"
                }
            )
        }
    
    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data.get("scheduled_time")

        if scheduled_time <= timezone.now()+timedelta(hours=5, minutes=30):
            raise forms.ValidationError("Scheduled time must be a future date & time.")

        return scheduled_time



class RecipientUploadForm(forms.Form):
    file = forms.FileField()