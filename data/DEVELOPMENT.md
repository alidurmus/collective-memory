# 🐍 Context7 ERP - Python Development Guide

This guide follows the [Cursor Python Development Guide](https://docs.cursor.com/guides/languages/python) best practices and modern Python development standards.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (Recommended: 3.11+)
- Git
- VS Code or Cursor
- Node.js (for pre-commit hooks)

### Installation

```bash
# Clone the repository
git clone https://github.com/alidurmus/python-dashboard.git
cd python-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Setup Django
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

## 🛠️ Development Tools

### Code Quality Tools

We use the following tools for code quality, following modern Python standards:

#### **Ruff** - Ultra-fast Python linter and formatter
```bash
# Check code
ruff check .

# Fix issues automatically
ruff check --fix .

# Format code
ruff format .
```

#### **Black** - Code formatter
```bash
# Format all Python files
black .

# Check formatting without changing files
black --check .
```

#### **isort** - Import organizer
```bash
# Sort imports
isort .

# Check import sorting
isort --check-only .
```

#### **MyPy** - Type checker
```bash
# Run type checking
mypy .

# Generate type stubs
mypy . --ignore-missing-imports
```

#### **Bandit** - Security linter
```bash
# Run security checks
bandit -r .

# Generate detailed report
bandit -r . -f json -o bandit-report.json
```

### Makefile Commands

We provide a comprehensive Makefile for common development tasks:

```bash
# Show all available commands
make help

# Development setup
make setup                 # Initial setup
make install-dev          # Install development dependencies
make pre-commit-install   # Install git hooks

# Code quality
make format               # Format code (black, isort, ruff)
make lint                 # Run all linters
make type-check          # Run type checking
make security            # Run security checks
make qa                  # Run all quality checks

# Testing
make test                # Run tests
make test-coverage       # Run tests with coverage
make django-check        # Run Django system checks

# Django
make runserver           # Start development server
make django-migrate      # Run migrations
make django-shell        # Open Django shell
make collectstatic       # Collect static files

# CI/CD
make ci                  # Run full CI pipeline locally
make clean              # Clean generated files
```

## 📁 Project Structure

```
python-dashboard/
├── .github/                 # GitHub Actions workflows
├── .vscode/                 # VS Code configuration
├── dashboard_project/       # Django project settings
├── core/                    # Core application
├── erp/                     # ERP modules
├── api/                     # REST API
├── tests/                   # Test files
├── docs/                    # Documentation
├── static/                  # Static files
├── templates/               # Django templates
├── requirements.txt         # Dependencies
├── pyproject.toml          # Modern Python configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── Makefile                # Development commands
└── README.md               # Project documentation
```

## 🔧 VS Code Configuration

### Recommended Extensions

The following extensions are automatically recommended when you open the project:

- **Python** (ms-python.python) - Core Python support
- **Pylance** (ms-python.vscode-pylance) - Advanced language server
- **Black Formatter** (ms-python.black-formatter) - Code formatting
- **Ruff** (charliermarsh.ruff) - Fast linting and formatting
- **isort** (ms-python.isort) - Import organization
- **MyPy** (ms-python.mypy-type-checker) - Type checking

### Settings

The project includes optimized VS Code settings in `.vscode/settings.json`:

- **Auto-formatting** on save
- **Import organization** on save
- **Type checking** enabled
- **Testing** with pytest
- **Linting** with multiple tools
- **Python path** configured for virtual environment

## 🧪 Testing

### Running Tests

```bash
# Run Django tests
python manage.py test

# Run pytest
pytest

# Run with coverage
coverage run --source='.' manage.py test
coverage report -m
coverage html

# Run specific test file
pytest tests/test_specific.py

# Run with verbose output
pytest -v
```

### Test Configuration

Tests are configured in `pytest.ini` and `pyproject.toml`:

- **Django settings** for testing
- **Coverage reporting** enabled
- **Test discovery** patterns
- **Minimum coverage** requirements

## 🔒 Security

### Security Checks

We implement multiple layers of security checking:

```bash
# Run security audit
bandit -r .

# Check for known vulnerabilities
safety check

# Run all security checks
make security
```

### Security Configuration

- **Bandit** configuration in `pyproject.toml`
- **Safety** checks in CI/CD pipeline
- **Django security** settings
- **Pre-commit hooks** for security

## 🚀 CI/CD Pipeline

### GitHub Actions

Our CI/CD pipeline includes:

1. **Code Quality Checks**
   - Black formatting
   - Ruff linting
   - MyPy type checking
   - Import sorting

2. **Security Scanning**
   - Bandit security audit
   - Safety vulnerability check

3. **Testing**
   - Unit tests
   - Integration tests
   - Coverage reporting

4. **Build & Deploy**
   - Static file collection
   - Documentation build
   - Deployment packaging

### Running CI Locally

```bash
# Run full CI pipeline
make ci

# Run individual checks
make qa
make test-coverage
make django-check
```

## 📊 Code Quality Metrics

### Quality Targets

- **Test Coverage**: 80%+
- **Type Coverage**: 90%+
- **Security Score**: A
- **Code Quality**: 9.0/10
- **Performance**: <2s response time

### Monitoring

- **Pre-commit hooks** prevent low-quality commits
- **GitHub Actions** ensure quality in CI/CD
- **Coverage reports** track test coverage
- **Security reports** monitor vulnerabilities

## 🎯 Best Practices

### Code Style

1. **Follow PEP 8** - Python style guide
2. **Use type hints** - Improve code clarity
3. **Write docstrings** - Document functions and classes
4. **Keep functions small** - Single responsibility principle
5. **Use descriptive names** - Clear variable and function names

### Django Best Practices

1. **Class-based views** - Use CBVs over FBVs
2. **Model validation** - Validate data at model level
3. **URL namespacing** - Organize URLs properly
4. **Template inheritance** - Use template blocks
5. **Static files** - Proper static file handling

### Git Workflow

1. **Feature branches** - Use descriptive branch names
2. **Commit messages** - Follow conventional commits
3. **Pull requests** - Code review process
4. **Pre-commit hooks** - Automated quality checks
5. **CI/CD pipeline** - Automated testing and deployment

## 🛡️ Security Guidelines

### Django Security

1. **CSRF protection** - Always enabled
2. **XSS protection** - Escape user input
3. **SQL injection** - Use ORM properly
4. **Authentication** - Secure user management
5. **HTTPS** - Use in production

### Code Security

1. **Input validation** - Validate all inputs
2. **Error handling** - Don't expose sensitive info
3. **Dependencies** - Keep dependencies updated
4. **Secrets management** - Use environment variables
5. **Security headers** - Implement proper headers

## 📈 Performance Optimization

### Database

1. **Query optimization** - Use select_related/prefetch_related
2. **Indexing** - Add indexes for frequently queried fields
3. **Caching** - Implement caching strategy
4. **Connection pooling** - Use connection pooling
5. **Monitoring** - Monitor database performance

### Frontend

1. **Static files** - Optimize CSS/JS delivery
2. **Image optimization** - Compress images
3. **Caching** - Browser and server caching
4. **CDN** - Use CDN for static assets
5. **Minification** - Minify CSS/JS files

## 📚 Learning Resources

### Python & Django

- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)
- [Real Python](https://realpython.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### Code Quality

- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Effective Python](https://effectivepython.com/)
- [Python Testing 101](https://python-testing-101.readthedocs.io/)

### Tools Documentation

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)

## 🆘 Troubleshooting

### Common Issues

1. **Virtual environment issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

2. **Import errors**
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **Database errors**
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Pre-commit issues**
   ```bash
   # Reinstall pre-commit hooks
   pre-commit uninstall
   pre-commit install
   pre-commit run --all-files
   ```

### Getting Help

1. **Check documentation** - Start with project docs
2. **Search issues** - Check GitHub issues
3. **Ask questions** - Create GitHub issue
4. **Code review** - Request code review
5. **Pair programming** - Work with team members

---

**🎯 Goal**: Maintain high code quality, security, and performance while following modern Python development practices.

**📝 Note**: This guide is continuously updated as the project evolves and new best practices emerge. 