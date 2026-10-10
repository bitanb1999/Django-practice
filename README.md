# DevTrack

DevTrack is a learning project: a small Django API for tracking engineering
issues and the reporters who file them. It is being built step by step to
practice Django project setup, apps, URL routing, function-based views, JSON
responses, query parameters, and Python object-oriented programming.

> **Current scope:** the project currently provides GET endpoints backed by
> JSON files. The POST/create endpoints described in the project brief have not
> been implemented yet. There is no Django ORM model for Reporter or Issue;
> `issues/models.py` contains regular Python classes for the OOP exercise.

## Features

- List reporters and look up one reporter by ID.
- List issues, look up one issue by ID, and filter issues by status.
- Store sample data in `reporters.json` and `issues.json`.
- Represent reporters and issues as Python classes with validation and
  `to_dict()` methods.
- Override `describe()` for critical and low-priority issues.

## Technology

- Python (the development environment used for this project is Python 3.12)
- Django 6.1.2
- JSON files for API data storage

## Project layout

```text
Django-practice/
├── devtrack/
│   ├── settings.py       # Django settings and registered apps
│   └── urls.py           # Includes the issues app under /api/
├── issues/
│   ├── models.py         # OOP entities (plain Python classes, not ORM models)
│   ├── urls.py           # API URL patterns
│   └── views.py          # GET endpoint implementations
├── issues.json           # Issue records
├── reporters.json        # Reporter records
├── manage.py
└── README.md
```

## Run locally

Run these commands from the directory containing `manage.py`.

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Install Django:

   ```bash
   python -m pip install "Django==6.1.2"
   ```

3. Apply Django's built-in migrations and check the project:

   ```bash
   python manage.py migrate
   python manage.py check
   ```

   These migrations initialize Django's built-in applications. Reporter and
   Issue records are stored in JSON files, not in the SQLite database.

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/` or send API requests to the endpoints below.
   Stop the server with **Ctrl+C**.

## API

All routes are mounted under `/api/`. The endpoints currently implemented are
GET-only. Unsupported HTTP methods return a `405 Method Not Allowed` response
where the view checks the method.

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/reporters/` | Return all reporters as a JSON array. |
| GET | `/api/reporters/?id=1` | Return the reporter with ID `1`. |
| GET | `/api/reporters/1/` | Path-parameter form of the reporter lookup. |
| GET | `/api/issues/` | Return all issues as a JSON array. |
| GET | `/api/issues/?id=1` | Return the issue with ID `1`. |
| GET | `/api/issues/1/` | Path-parameter form of the issue lookup. |
| GET | `/api/issues/?status=open` | Return issues whose status is `open`. |
| GET | `/api/issues/status/open/` | Path-parameter form of the status filter. |

Query parameter values are read in the view using `request.GET.get(...)`.
For example, `/api/issues/?status=open` uses the same `/api/issues/` route as
the unfiltered list; the view applies the filter.

IDs in JSON records are integers. Status and priority values are lowercase:

- Status: `open`, `in_progress`, `resolved`, `closed`
- Priority: `low`, `medium`, `high`, `critical`

### Example requests

List all issues:

```http
GET http://127.0.0.1:8000/api/issues/
```

Filter issues by status:

```http
GET http://127.0.0.1:8000/api/issues/?status=open
```

Find one reporter:

```http
GET http://127.0.0.1:8000/api/reporters/?id=1
```

### Responses

A successful list request returns a JSON array, for example:

```json
[
  {
    "id": 1,
    "title": "Issue 1",
    "description": "Description for Issue 1",
    "reporter_id": 1,
    "status": "open",
    "priority": "high"
  }
]
```

A successful lookup returns the matching JSON object. If an ID query parameter
is not an integer, the query-based lookup returns `400 Bad Request`. If the ID
is not found, the lookup returns `404 Not Found`, for example:

```json
{"error": "Issue not found"}
```

An empty list (or `[]`) means there are no matching records.

## JSON data files

The files are read from the project root using Django's `BASE_DIR`. Keep each
file valid JSON and use a top-level array, even when there are no records:

```json
[]
```

Reporter record shape:

```json
{
  "id": 1,
  "name": "Alex Example",
  "email": "alex@example.com",
  "team": "backend"
}
```

Issue record shape:

```json
{
  "id": 1,
  "title": "Login button not working on mobile",
  "description": "Users on iOS cannot tap the login button.",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

`reporter_id` stores the ID of the reporter who filed the issue. The JSON-file
approach is deliberately simple for this exercise; it does not provide database
transactions, concurrent-write protection, or automatic referential integrity.
The current GET-only endpoints do not modify either data file.

## OOP design

`issues/models.py` defines `BaseEntity`, an abstract base class with an abstract
`validate()` method and a `to_dict()` helper. `Reporter` and `Issue` inherit
from it and implement validation.

`CriticalIssue` and `LowPriorityIssue` inherit from `Issue` and override
`describe()`. For example, a critical issue describes itself as:

```text
[URGENT] Login button not working on mobile — needs immediate attention
```

These are ordinary Python objects. They are not Django ORM models and do not
create database tables or require app migrations.

## Testing with Postman

1. Start the Django server with `python manage.py runserver`.
2. Create a request with method **GET** and one of the endpoint URLs above.
3. For query parameters, either enter `?id=1` or `?status=open` in the URL, or
   add the key/value in Postman's **Params** tab.
4. Send the request and inspect the HTTP status and JSON response.
5. For a success case, request an existing ID such as
   `GET /api/issues/?id=1`.
6. For a failure case, request a missing ID such as
   `GET /api/issues/?id=999`; it should return `404` and an error object.

### Required Postman screenshots

Add actual screenshots of at least one successful response and one failure
response before submitting. Save the images in a `screenshots/` folder, then
embed them here using relative Markdown links, for example:

```markdown
![Successful Postman request](screenshots/postman-success.png)
![Failure Postman request](screenshots/postman-failure.png)
```

The screenshots are not included yet; capture them from your own Postman session
so they show your real request and response.

## Design decision

For this practice version, records are stored in JSON files instead of Django's
ORM. This follows the exercise brief and keeps attention on Python classes,
validation, URL routing, views, and JSON HTTP responses. The issue stores
`reporter_id` rather than embedding a full reporter object, representing the
one-reporter-to-many-issues relationship in the requested simple format.

## Planned work

- Implement `POST /api/reporters/` to validate and create reporters.
- Implement `POST /api/issues/` to validate and create issues, select the
  appropriate issue subclass by priority, and include `describe()` in the
  response.
- Add tests for successful requests, validation errors, invalid IDs, and
  missing records.
