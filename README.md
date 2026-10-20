\# CRM Lead Management System



A web-based Customer Relationship Management (CRM) application built with Python and Django to manage leads, track customer interactions, schedule follow-ups, and visualize business activity.



\## Features



\* \*\*Lead Management:\*\* Create, view, update, and delete leads.

\* \*\*Search \& Filtering:\*\* Find leads using search and status filters.

\* \*\*Lead Scoring:\*\* Assign scores to leads.

\* \*\*Activity Tracking:\*\* Maintain records of customer interactions.

\* \*\*Follow-up Management:\*\* Track upcoming follow-up activities.

\* \*\*Customer Conversion:\*\* Convert qualified leads into customers.

\* \*\*Interactive Dashboard:\*\* Visualize CRM data using charts.

\* \*\*REST API:\*\* Access CRM functionality through Django REST Framework.

\* \*\*API Permissions:\*\* Authentication and permission controls.

\* \*\*CSV Import \& Export:\*\* Import and export records through Django Admin.



\## Tech Stack



\* \*\*Backend:\*\* Python, Django

\* \*\*Database:\*\* MySQL

\* \*\*API:\*\* Django REST Framework

\* \*\*Filtering:\*\* django-filter

\* \*\*Data Import/Export:\*\* django-import-export

\* \*\*Frontend:\*\* HTML, CSS, JavaScript, Chart.js

\* \*\*Version Control:\*\* Git and GitHub



\## Project Repository



GitHub: https://github.com/chinmaya-hub/CRM-Lead-Management-System



\## Local Installation



\### 1. Clone the repository



```bash

git clone https://github.com/chinmaya-hub/CRM-Lead-Management-System.git

cd CRM-Lead-Management-System

```



\### 2. Create and activate a virtual environment



Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



If PowerShell activation is blocked, use the virtual environment's Python executable directly.



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file in the project root. Add your own local configuration:



```env

DJANGO\_SECRET\_KEY=replace\_with\_your\_own\_secret\_key

DB\_NAME=crm\_db

DB\_USER=crm\_user

DB\_PASSWORD=replace\_with\_your\_database\_password

DB\_HOST=localhost

DB\_PORT=3306

```



Never commit your real `.env` file or secrets to GitHub.



\### 5. Prepare the database



Create the MySQL database and configure a database user with the required permissions.



Run migrations:



```bash

python manage.py migrate

```



\### 6. Create an administrator account



```bash

python manage.py createsuperuser

```



\### 7. Start the development server



```bash

python manage.py runserver

```



Open `http://127.0.0.1:8000/` in your browser.



\## Security Notes



\* Keep secret keys and database credentials in environment variables.

\* Do not upload `.env` files.

\* Use `DEBUG=False` and configure `ALLOWED\_HOSTS` before production deployment.

\* Configure production database credentials separately from local development.



\## Author



Developed as a Python and Django full-stack project.



GitHub: https://github.com/chinmaya-hub



