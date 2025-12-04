# 📝 Django Blog Application - My Tech Blog

A full-featured Django blog application with JWT-based authentication,
CRUD posts, comments, and a clean Bootstrap-styled frontend. Designed
for learning and production-ready concepts like authentication,
templates, and user-specific content management.

## 🌟 Features

### **User Authentication**

-   Sign up, login, and logout functionality.
-   JWT-based authentication with cookies (`access_token`) for session handling.
-   Expired token detection on the frontend and automatic logout.

### **Posts**

-   Users can create, edit, and delete posts.
-   Each post has a title, content, and optional image URL.
-   Only authors can edit or delete their own posts.
-   Posts are listed on the homepage and user-specific pages.

### **Comments**

-   Logged-in users can comment on posts.
-   Display includes author username, comment content, and timestamp.
-   No edit/delete functionality on the post detail page (read-only view).

### **Frontend**

-   Server-side rendered with Django templates.
-   Bootstrap 5 for responsive design.
-   FontAwesome for icons.
-   Consistent button/icon styling across posts and comments.

### **Security**

-   Passwords are hashed using Django's default secure hashing.
-   CSRF protection in all forms.
-   Backend checks for user authorization.

### **Extra Functionalities**

-   Django messages for success/error/warning alerts.
-   Dynamic token expiration detection and redirect.
-   Posts and comments rendered in card-style sections (not tables).

------------------------------------------------------------------------

## 🗂️ Project Structure
Django_Blog
│
├── .gitattributes
├── .gitignore
├── README.md
│
├── backend_django        # Backend (Django project + apps)
│   │
│   ├── account           # User account app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── auth_utils.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── backend_django    # Project folder
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── blog              # Blog app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── db.sqlite3
│   ├── manage.py
│   └── requirements.txt
│
├── frontend_django       # Frontend (templates + static)
│   │
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── auth.js
│   │
│   └── templates
│       ├── base.html
│       ├── edit_post.html
│       ├── home.html
│       ├── post_detail.html
│       ├── userComments.html
│       ├── userPost.html
│       └── write_post.html

------------------------------------------------------------------------

## ⚡ Installation & Setup

### **Clone the repository**

    git clone <repo-url>
    cd backend_django

### **Create a virtual environment**

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate    # Windows

### **Install dependencies**

    pip install -r requirements.txt

### **Set up `.env` file**

    SECRET_KEY=<your-secret-key>
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3

### **Run migrations**

    python manage.py makemigrations
    python manage.py migrate

### **Start the development server**

    python manage.py runserver

### **Access the app**

Open: **http://127.0.0.1:8000/**

------------------------------------------------------------------------

## 🖥️ Usage

-   **Homepage:** Lists all posts.
-   **User Posts:** `/user/posts/`
-   **Post Detail:** `/posts/<post_id>/`
-   **Create Post:** Available on `/user/posts/`
-   **Edit/Delete Actions:** Visible only to the post author.
-   **Commenting:** Only logged-in users can comment.

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   **Backend:** Django, Django REST Framework
-   **Frontend:** Django Templates, Bootstrap 5, FontAwesome
-   **Authentication:** JWT tokens (stored in cookies)
-   **Database:** SQLite (dev), PostgreSQL (prod recommended)

------------------------------------------------------------------------

## 💡 Notes

-   JWT expiration handled on frontend → expired tokens trigger logout.
-   Comments are read-only on post detail page.
-   CSRF included in all forms.
-   User-specific edit/delete policies enforced.

------------------------------------------------------------------------

