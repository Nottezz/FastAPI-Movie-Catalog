# 🎞️ Movie Catalog

A FastAPI-based application for managing and browsing a movie catalog. Designed with scalability and developer experience in mind.

---

## 🚀 Features

- FastAPI-powered backend
- REST API for movies
- Async support
- Integrated testing setup
- Pre-commit hooks for clean code
- Redis support (for caching or other async tasks)

---

## 🧑‍💻 Getting Started

### 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/movie-catalog.git
   cd movie-catalog


2. Mark the `movie-catalog` directory as "Sources Root" in your IDE (for better imports).

---

### 📦 Install Dependencies

Use [`uv`](https://github.com/astral-sh/uv) to install packages:

```bash
uv install
```
---

### ⚙️ Configure Pre-commit Hooks

Install and activate pre-commit:

```bash
pre-commit install
```

This ensures formatting, linting, and other checks before each commit.

---

### 🚀 Run Development Server

1. Ensure you're in the working directory:

   ```bash
   cd movie-catalog
   ```

2. Make sure Redis is running:

   ```bash
   docker run -d -p 6379:6379 redis
   ```

3. Start the FastAPI dev server:

   ```bash
   fastapi dev
   ```

The server will be available at `http://localhost:8000`.

---

### ✅ Running Tests

1. Make sure that the Redis test container is running.:

   ```bash
   docker run -d -p 6380:6380 redis
   ```
2. Set env variables: REDIS_PORT=6380;TESTING=1


3. Run the test suite:

   ```bash
   python -m unittest -v
   ```
   or with coverage
   ```bash
   coverage run -m unittest
   ```

---

### 🧪 Useful Snippets

Generate a random secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

---

## 👨‍🔧 For Developers

* Use a virtual environment (`uv`, `venv`, or `poetry`) to manage dependencies.
* Follow PEP8 style guidelines (auto-enforced via `pre-commit`).
* Use descriptive commit messages (consider [Conventional Commits](https://www.conventionalcommits.org/)).
* Document public endpoints and services clearly with docstrings and OpenAPI schemas.

---
