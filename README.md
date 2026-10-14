# Eng Abdelnaser — Programming Academy

A Django-based Arabic-first programming learning platform. Includes a public landing page, phone-number login, approval workflow, course/lesson management, code library, developer resources, CV page, and a staff panel.

## What's included
- Django backend and SQLite database stored in the project folder (`db.sqlite3`).
- Django admin at `/django-admin/` to manage courses, lessons, code snippets, and resources.
- User registration with phone number and password; new accounts stay pending until approved.
- Staff panel for reviewing members and assigning roles.
- Responsive dark developer-themed design, animated cards, copy-code buttons, and mobile navigation.
- Editable CV template and social/contact links.

## Run locally
Use Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Create the two requested admin accounts
After migrations, run:

```bash
python manage.py create_platform_admins
```

The command asks you to set and confirm passwords in the terminal; it never prints or hardcodes them. The first account uses the phone number supplied by the owner (`01098227150`) and display name `Eng Abdelnaser`. For Fatima, enter her own phone number when prompted. Choose unique, strong passwords of at least 10 characters and store them securely. Do not share one password between accounts.

Because the admin creation command marks these accounts as Django superusers, they can access `/django-admin/`. Protect these credentials carefully.

## Add content
Visit `/django-admin/` and create:
1. Courses — title, slug, summary, category, level, published status.
2. Lessons inside each course.
3. Code snippets — title, language, description, code.
4. Resources — tools, extensions, definitions, games, and articles.

## Profile photo
The requested photo named `Snapchat-19917905` was not attached to this project-generation message, so the CV currently uses a designed code-avatar placeholder. When you have the actual image file, upload it into `media/` and we can wire it into the profile/CV and landing page.

## Database and file storage
- Local development uses SQLite (`db.sqlite3`) in this project folder, not Firebase.
- Uploaded course covers are stored in the project's `media/` directory.
- For a public production site, move to a managed VPS/server, configure PostgreSQL, HTTPS, backups, `DEBUG=False`, a strong `DJANGO_SECRET_KEY`, and restricted `ALLOWED_HOSTS`. Media files and database backups should be included in your backup plan.
- The database is physically stored on your server, not inside the browser or a static website. Do not expose database credentials or Django secret keys in frontend JavaScript.

## Important deployment checklist
- Set `DJANGO_DEBUG=False`.
- Set a random `DJANGO_SECRET_KEY`.
- Set `DJANGO_ALLOWED_HOSTS` to the actual domain.
- Configure HTTPS and secure cookies at the reverse proxy/production settings.
- Back up the database and uploaded media.
- Test signup, approval, login, role changes, deletion, and admin access before inviting real members.

## Notes
This is a starter project that can run locally after installing dependencies and running migrations. Hosting it publicly requires server setup and security review. SMS/WhatsApp automatic password delivery is not enabled: this starter deliberately does not send passwords over chat. Users choose their own password during signup; the administrator approves the account afterward.
