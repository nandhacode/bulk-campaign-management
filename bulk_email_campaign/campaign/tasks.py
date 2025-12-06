from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Campaign, Recipient, DeliveryLog
from io import BytesIO
from django.core.mail import EmailMessage
import pandas as pd
from django.conf import settings


@shared_task
def schedule_campaign_task(campaign_id):
    print("================== Email Campaign Started ====================")
    campaign = Campaign.objects.get(id=campaign_id)
    campaign.status = "in_progress"
    campaign.save()

    sent_count = failed_count = 0

    recipients = Recipient.objects.filter(subscription_status="Subscribed")

    for r in recipients:
        print(f"Recipent Name {r.name} <---> Email {r.email}")
        try:
            send_mail(
                subject=campaign.subject,
                message=campaign.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[r.email],
            )
            DeliveryLog.objects.create(
                campaign=campaign,
                recipient=r,
                recipient_email=r.email,
                sent_at=timezone.now()+timedelta(hours=5, minutes=30),
                status="Sent"
            )
            sent_count+=1
        except Exception as e:
            DeliveryLog.objects.create(
                campaign=campaign,
                recipient=r,
                status="Failed",
                recipient_email=r.email,
                failure_reason=str(e)
            )
            failed_count+=1

    campaign.total_recipients = len(recipients)
    campaign.sent_count = sent_count
    campaign.failed_count = failed_count
    campaign.status = "completed"
    campaign.save()
    print(f"================== Email Campaign Ended --- Campaign ID {campaign_id} ====================")
    campaign_report = Campaign.objects.filter(id=campaign_id).values('name','subject','content','scheduled_time','status','total_recipients','sent_count','failed_count')
    df = pd.DataFrame(list(campaign_report))
    df = df.rename(columns={
        'name': 'Campaign Name',
        'subject': 'Email Subject',
        'content': 'Email Content',
        'scheduled_time': 'Scheduled Date',
        'status': 'Status',
        'total_recipients': 'Total Recipients',
        'sent_count': 'Sent Count',
        'failed_count': 'Failed Count'
    })
    
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    campaign_name = campaign_report[0]['name']

    email = EmailMessage(
        subject=f"{campaign_name} Campaign CSV Report",
        body="Hello Admin,\n\nAttached is the latest dynamic report.\n\nRegards,\nSystem",
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER],
    )
    
    email.attach(
        f"{campaign_name}_report.csv",
        csv_buffer.getvalue(),
        "text/csv"
    )
    
    try:
        email.send()
        print("================== Campaign report sent to Admin ====================")
    except Exception as e:
        print(f"Campaign report Status Error : {e}")

@shared_task
def check_and_send_scheduled():
    campaigns = Campaign.objects.filter(
        status="scheduled",
        scheduled_time__lte=timezone.now()+timedelta(hours=5, minutes=30)
    )
    print(f"Time : {timezone.now()+ timedelta(hours=5, minutes=30)}")
    print(f"============== {campaigns} Campaign Timer Triggered ==============")
    if campaigns:
        print(f"Time : {timezone.now()}")
        for c in campaigns:
            print(f"Campaign Name : {c.name}")
            schedule_campaign_task.delay(c.id)