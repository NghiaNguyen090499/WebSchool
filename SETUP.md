# Quick Setup Guide

## Initial Setup Steps

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin username, email, and password.

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the website**
   - Homepage: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Adding Initial Content

After logging into the admin panel, add some sample content:

### 1. Core Values
- Go to **Core → Core Values**
- Add 4 core values with icons (e.g., `fas fa-graduation-cap`, `fas fa-users`, `fas fa-lightbulb`, `fas fa-heart`)

### 2. Statistics
- Go to **Core → Statistics**
- Add 4 statistics (e.g., Students, Teachers, Years of Excellence, Programs)

### 3. News Categories
- Go to **News → Categories**
- Add categories like "Announcements", "Events", "Academic"

### 4. Sample News
- Go to **News → News**
- Add a few news articles with thumbnails
- Mark one as "Featured" for the homepage

### 5. Events
- Go to **Events → Events**
- Add upcoming events (with future dates)
- Add some past events (with past dates)

### 6. Gallery Albums
- Go to **Gallery → Albums**
- Create albums and add photos to each album

### 7. About Pages
- Go to **About → About Pages**
- Add content for Mission, Vision, and Principal's Message

## Testing the Contact Form

The contact form will save messages to the database. To receive email notifications:

1. Update email settings in `school_website/settings.py`
2. Configure your SMTP server credentials
3. Test by submitting the contact form

## Multilingual Support

The site supports English and Vietnamese. To add translations:

1. Create translation files:
   ```bash
   python manage.py makemessages -l vi
   python manage.py makemessages -l en
   ```

2. Edit the `.po` files in `locale/` directory

3. Compile translations:
   ```bash
   python manage.py compilemessages
   ```

## Production Deployment

1. Set `DEBUG = False` in `settings.py`
2. Update `ALLOWED_HOSTS` with your domain
3. Configure PostgreSQL database
4. Set up static file serving (use WhiteNoise or a web server)
5. Configure media file serving
6. Set up proper email backend
7. Use environment variables for sensitive settings

## Notes

- All images should be uploaded through the admin panel
- The site uses Tailwind CSS via CDN (for production, consider using Tailwind CLI)
- Dark mode preference is saved in browser localStorage
- The site is fully responsive and mobile-friendly



