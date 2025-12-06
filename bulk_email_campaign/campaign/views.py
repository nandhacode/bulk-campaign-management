from django.shortcuts import render, redirect, get_object_or_404
from .utils import call_form
from .models import Recipient, Campaign, DeliveryLog
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import CampaignForm
import pandas as pd
from .tasks import schedule_campaign_task
from django.core.mail import send_mail
from django.http import JsonResponse
from io import BytesIO
from django.core.mail import EmailMessage

def upload_bulk_recipent(request):
    if request.method == 'POST' and request.FILES['file']:
        upload_file = request.FILES['file']
        print(upload_file.name)

        if not upload_file:
            message = "No file uploaded."
            return call_form(request,message)
        
        try:
            if upload_file.name.endswith(".csv"):
                df = pd.read_csv(upload_file)
            elif upload_file.name.endswith(".xlsx") or upload_file.name.endswith(".xls"):
                df = pd.read_excel(upload_file)
            else:
                message = "Invalid file format. Only CSV, XLS, XLSX allowed."
                return call_form(request,message)
        except Exception as e:
            message = f"Error reading file. Invalid or corrupted file. {e}"
            return call_form(request,message)
        
        required_columns = {"Name", "Email", "Subscription"}
        if not required_columns.issubset(list(df.columns)):
            message = f"File must contain columns: {required_columns}"
            return call_form(request,message)

        df = df.dropna(subset=["Name","Email", "Subscription"])

        allowed_values = {"Subscribed", "Unsubscribed"}
        df = df[df["Subscription"].isin(allowed_values)]

        df = df.drop_duplicates(subset=["Email"], keep="first")

        invalid_emails = []
        for email in df["Email"]:
            try:
                validate_email(email)
            except ValidationError:
                invalid_emails.append(email)

        if invalid_emails:
            return call_form(request, f"Invalid email(s): {invalid_emails}")
        
        email_in_file = list(df["Email"])
        email_in_database = set(Recipient.objects.filter(email__in=email_in_file).values_list("email", flat=True))

        to_insert = []

        for _, row in df.iterrows():
            if row["Email"] not in email_in_database:
                to_insert.append(
                    Recipient(
                        name=row["Name"],
                        email=row["Email"],
                        subscription_status=row["Subscription"],
                    )
                )

        if to_insert:
            Recipient.objects.bulk_create(to_insert)
        
        message = f"Total Count of valid records in file : {len(df)} ==> Successfully Inserted Count : {len(to_insert)} ==> Existing Records Count : {len(df)-len(to_insert)}"
        return call_form(request,message)
    else:
        message = ""
        return call_form(request,message)

def campaign_create(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)

        if form.is_valid():
            campaign = form.save()

            return redirect("campaign_list")

    else:
        form = CampaignForm()

    return render(request, "campaign_form.html", {"form": form})


def campaign_list(request):
    campaigns = Campaign.objects.all().order_by("-created_at")
    return render(request, "campaign_list.html", {"campaigns": campaigns})

def update_campaign_status(request,id):
    campaign = get_object_or_404(Campaign, pk=id)
    campaign.status = "scheduled"
    campaign.save()
    return redirect('campaign_list')

def campaign_detail(request, id):
    campaign = get_object_or_404(Campaign, pk=id)
    logs = DeliveryLog.objects.filter(campaign=campaign)

    return render(request, "campaign_details.html", {
        "campaign": campaign,
        "logs": logs
    })