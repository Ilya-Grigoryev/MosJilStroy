# Construction Company Website

Django-based website for a construction company specializing in house renovations.
All content on the website can be easily managed and updated from the custom (not default from Django) admin panel located at `/admin`.

## Features

The website consists of several sections that can be fully managed and customized:

### 1. **Gratitude and Permissions**
- This section allows admins to upload and view files related to permissions and acknowledgements.
- All files can be added, edited, and deleted through the admin panel.

### 2. **Management Team**
- A list of company leaders, including their photos and details, which can be managed through the admin panel.
- Admins can add, update, or delete the team members' information as needed.

### 3. **Our Projects**
- A section displaying a list of completed renovation projects. Each project has a detailed page that includes:
  - Key project specifications
  - Photos
  - A location map (powered by Google Maps)
- Projects can be added, updated, or removed via the admin panel, including uploading photos for each project.

### 4. **Services**
- A list of services offered by the company, presented as 4 interactive blocks. When hovered over, each block flips to show detailed information about the service.
- The services list can be easily managed via the admin panel.

### 5. **Job Vacancies**
- A section for submitting internship applications, with the ability to download the latest application form.
- The admin panel allows uploading the current version of the application form and viewing all submitted internship applications.
- The vacancies section displays a list of available job opportunities with the ability to upload resumes. Admins can add, update, or delete job listings, and view all applications for the vacancies.

### 6. **Contact Information**
- A contact form that allows users to submit inquiries and specify an email for responses.
- Admins can respond to user questions directly from the admin panel, and the user will receive the response via email.

## Requirements

To run this project, you need to install the following dependencies:

### Python dependencies:
1. Django==3.1.6
2. Pillow==10.4.0

### Setting up the environment

1. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

2. **Install required libraries**:
    To install the required libraries, run:
    ```bash
    pip install Django==3.1.6 Pillow==10.4.0
    ```

3. **Create a superuser**:
    To access the custom admin panel, create a superuser with the following command:
    ```bash
    python manage.py createsuperuser
    ```
    Set the username and password for the superuser.
   (it will be the same for both the admin panel and the superuser login)

4. **Run the development server**:
    Start the development server to view the site locally:
    ```bash
    python manage.py runserver
    ```
    The website will be available at `http://127.0.0.1:8000/`.

## Database

For simplicity, the website uses an SQLite database to store all the content. This includes all template data such as:
- Text content
- Media (photos)
- User-submitted inquiries
- Internship and job applications

## Admin Panel

Access the admin panel at `/admin` on the website after running the server.
The login credentials will be the ones you set during the superuser creation process.
Here, you can manage all sections of the website, including:

- Managing gratitude and permission files
- Updating the management team
- Editing project details (with photo uploads)
- Adding, editing, or removing services
- Managing job vacancies and internship applications
- Responding to user inquiries via the contact form

---
