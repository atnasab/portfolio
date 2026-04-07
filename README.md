# Basanta Singh — Portfolio Website

Django 5 portfolio with blog, teaching portfolio, and projects. Deployed on DigitalOcean Basic Droplet (no Docker).

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | Django 5, Python 3.11+              |
| Database    | PostgreSQL (production), SQLite (local) |
| Web server  | Nginx + Gunicorn                    |
| Static      | WhiteNoise                          |
| Auth/sec    | Django Axes, CSP, rate limiting     |
| Editor      | Django Summernote (WYSIWYG)         |
| Tags        | django-taggit                       |
| RSS         | Django syndication                  |
| Sitemap   | Django sitemaps                     |

## Project Structure

```
portfolio/
├── config/
│   ├── settings/
│   │   ├── base.py          # shared settings
│   │   ├── local.py         # dev
│   │   └── production.py    # DigitalOcean
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/                # home, about, contact, SiteProfile
│   ├── blog/                # posts, categories, tags, RSS feed
│   ├── teaching/            # subjects, syllabi, links
│   └── projects/            # research & project portfolio
├── templates/
│   ├── base.html
│   ├── core/
│   ├── blog/
│   ├── teaching/
│   ├── projects/
│   ├── components/
│   └── errors/
├── static/
│   ├── css/main.css
│   └── js/main.js
├── scripts/
│   ├── deploy.sh            # full DO deployment script
│   ├── nginx.conf
│   ├── portfolio.service    # systemd
│   └── portfolio.socket
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── gunicorn.conf.py
├── manage.py
└── .env.example
```

## Local Development

```bash
# 1. Clone & create virtualenv
git clone <repo-url> portfolio && cd portfolio
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements/local.txt

# 3. Create .env
cp .env.example .env
# Edit .env: set DJANGO_SECRET_KEY (any random string is fine for local)

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start dev server
python manage.py runserver
```

Visit http://localhost:8000 — go to /admin to add your profile, subjects, and projects.

## DigitalOcean Deployment

### Prerequisites
- DigitalOcean Basic Droplet: Ubuntu 22.04 LTS, 1 vCPU / 1 GB RAM ($6/mo minimum)
- A domain name pointed to the droplet IP (A records for `@` and `www`)

### One-command deploy

```bash
# SSH into your droplet as root, then:
git clone <your-repo-url> /tmp/portfolio
chmod +x /tmp/portfolio/scripts/deploy.sh
/tmp/portfolio/scripts/deploy.sh yourdomain.com your@email.com
```

The script will:
1. Install all system packages (Python, PostgreSQL, Nginx, Certbot, fail2ban)
2. Create a `portfolio` system user
3. Set up PostgreSQL database
4. Clone your repo, create virtualenv, install dependencies
5. Generate a `.env` file with a random `SECRET_KEY` and database password
6. Run migrations and collect static files
7. Install systemd socket + service
8. Configure Nginx with security headers
9. Obtain and auto-renew Let's Encrypt SSL certificate
10. Configure UFW firewall and fail2ban

### After deployment

```bash
# Create Django superuser
sudo -u portfolio /home/portfolio/venv/bin/python \
  /home/portfolio/app/manage.py createsuperuser \
  --settings=config.settings.production

# Update code
sudo /home/portfolio/app/scripts/deploy.sh --update

# View logs
tail -f /var/log/portfolio/gunicorn-error.log
tail -f /var/log/nginx/portfolio-error.log

# Restart app
sudo systemctl restart portfolio

# Check status
sudo systemctl status portfolio
```

### Admin setup (via /admin after login)

1. **Site Profile** → Add your name, bio, avatar, CV, and social links
2. **Teaching > Subjects** → Add each course with description, syllabus, links
3. **Projects** → Add your research projects with GitHub/paper links
4. **Blog > Categories** → Create categories (e.g. NLP, Computer Vision, Education)
5. **Blog > Posts** → Write articles with Summernote rich text editor

## Security Features

| Feature | Implementation |
|---------|---------------|
| HTTPS | Let's Encrypt via Certbot |
| HSTS | 1 year, subdomains, preload |
| CSP | `django-csp` with strict policy |
| Brute-force protection | `django-axes` (5 attempts → 1hr lockout) |
| Rate limiting | `django-ratelimit` on contact form |
| Input sanitisation | `bleach` on all user inputs |
| Bot honeypot | Hidden field in contact form |
| Admin URL obfuscation | Configurable via `ADMIN_URL` env var |
| SQL injection | Django ORM (parameterised queries) |
| XSS | Django template escaping + CSP |
| CSRF | Django CSRF middleware |
| Clickjacking | `X-Frame-Options: DENY` |
| Sec headers | Nginx adds HSTS, X-Content-Type, Referrer-Policy |
| fail2ban | SSH + Nginx brute-force protection |
| UFW firewall | Only ports 22, 80, 443 open |

## Updating Content

All content is managed via Django Admin. No code changes needed to:
- Publish blog posts
- Add/edit subjects taught
- Add/edit projects
- Update profile, bio, social links, CV

## RSS Feed

Available at `/blog/feed/` — subscribers get new posts automatically.
