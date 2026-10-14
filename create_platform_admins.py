from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from getpass import getpass

class Command(BaseCommand):
    help = "Create the two requested platform admin accounts with passwords entered securely in the terminal."

    def handle(self, *args, **options):
        User = get_user_model()
        accounts = [
            ("Eng Abdelnaser", "01098227150"),
            ("Fatima", None),
        ]
        for display_name, suggested_phone in accounts:
            phone = suggested_phone or input("Enter Fatima's phone number: ").strip()
            if User.objects.filter(phone=phone).exists():
                self.stdout.write(self.style.WARNING(f"Account {phone} already exists; updating its role/approval."))
                user = User.objects.get(phone=phone)
            else:
                user = User(phone=phone, username=phone)
            user.display_name = display_name
            user.role = "admin"
            user.is_approved = True
            user.is_staff = True
            user.is_superuser = True
            password = getpass(f"Set a strong password for {display_name} ({phone}): ")
            confirm = getpass("Confirm password: ")
            if not password or password != confirm:
                self.stdout.write(self.style.ERROR("Passwords were empty or did not match; this account was skipped."))
                continue
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created/updated admin: {display_name} / {phone}"))
        self.stdout.write(self.style.SUCCESS("Done. Passwords were not printed or saved in source files."))
