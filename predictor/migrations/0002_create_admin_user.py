from django.db import migrations

def create_admin_user(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = "Wilworks"
    password = "admin123"
    email = "wilfredasumboya@gmail.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superuser created successfully.")
    else:
        print("⚠️ Superuser already exists — skipping creation.")

class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
