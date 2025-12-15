# 📧 Bulk Email Campaign Management System

## 📝 Problem Description

A Django project for manage and send bulk email campaigns to its registered users with CSV upload support, tracking campaign triggered status, and automatic pairing generation campaign status to admin.

-- Create campaigns

-- Schedule campaigns

-- Track sending progress

-- Efficiently handle large recipient lists

---

## 🧰 Virtual Environment Setup

Before running the project, make sure to set up your Python virtual environment.

### Step 1: Install `virtualenv` (if not already installed)
```bash
pip install virtualenv
```


### Step 2: Create a virtual environment
```bash
python -m virtualenv env
```

### Step 3: Activate the virtual environment
```bash
env\Scripts\activate
```

## Install Project Dependencies

After activating your virtual environment, install all necessary packages:

```bash
pip install -r requirements.txt
```

This installs all dependencies used in the project including Django, pandas, etc.


## 🛠️ Database Setup

Before running the application, make sure your database is set up and update the (EMAIL_HOST_USER, CELERY_BROKER_URL) credentials are configured in settings.py.

### Step 1: Create the database
Create a database (e.g., PostgreSQL, SQLite, etc.) and update the database settings in your Django settings.py.

### Step 2: Create migrations
```bash
python manage.py makemigrations
```

### Step 3: Apply migrations to create tables
```bash
python manage.py migrate
```

## 🚀 Run the Project

Start the development server:

```bash
python manage.py runserver
```
Start the Celery Task and Celery Beat Scheduler

```bash
celery -A bulk_email_campaign worker --pool=solo -l info
```
and 
```bash
celery -A bulk_email_campaign beat -l info
```
Then open this URL in your browser to access the landing screen:

```bash
http://127.0.0.1:8000/
```

------------------------------------------------------------------------

# 📂 Project Scenarios

## 📁 Scenario 1: Campaign Creation

Admin can create a new campaign using a simple form. The campaign
includes:

-   **Campaign Name**
-   **Subject Line**
-   **Email Content** (Plain text or HTML)
-   **Scheduled Time for Sending**
-   **Status Control** (Draft, Scheduled, In Progress, Completed)

This module ensures clean validation and proper storage of campaign
metadata.

------------------------------------------------------------------------

## 📁 Scenario 2: Recipient Management

Manage recipients efficiently through:

-   Recipient model with:

    -   **Name**
    -   **Email Address**
    -   **Subscription Status** (Subscribed / Unsubscribed)

-   **Bulk Upload Support**
    Upload a CSV/Excel file containing recipients.

-   **Validation Rules**

    -   Valid email format
    -   Duplicate email detection

This module ensures your mailing list is clean and optimized before
campaign execution.

------------------------------------------------------------------------

## 📁 Scenario 3: Campaign Execution

Once a campaign is scheduled, the system will:

-   Automatically start sending emails at the scheduled time
-   Process large recipient lists efficiently
-   Maintain a **Delivery Log** for each email:
    -   Recipient Email
    -   Sent / Failed
    -   Failure Reason (if any)

The campaign status dynamically updates based on progress: - Draft →
Scheduled → In Progress → Completed

------------------------------------------------------------------------

## 📊 Scenario 4: Campaign Dashboard

The dashboard provides campaign-level insights:

-   Total Recipients
-   Sent Count
-   Failed Count
-   Status Summary (e.g., *470/500 sent*)
-   Click a campaign to view detailed email delivery logs

This helps admins track real-time campaign performance.

------------------------------------------------------------------------

## 📄 Scenario 5: Reporting

Once the campaign completes:

-   Generate a summary report (Text/CSV)
-   Automatically send the report to the configured **Admin Email**

This ensures proper audit tracking and post-campaign visibility.
