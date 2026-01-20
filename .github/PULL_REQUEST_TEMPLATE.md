## Description

<!-- Provide a brief description of the changes in this PR -->

## CI/CD Status

> **Note**: Automated checks will run when this PR is submitted:
> - **Tests**: pytest with coverage
> - **Linting**: Black, isort, flake8
> - **Docker**: Build verification
> - **Documentation**: Markdown linting

Please ensure all checks pass before requesting review.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Tests (adding or updating tests)

## Related Issue

<!-- Closes #issue_number or Fixes #issue_number -->

## Changes Made

<!-- List the specific changes made in this PR -->

Example format:
- Added `new_feature.py` module to handle X
- Modified `api/views.py` to add Y endpoint
- Updated `README.md` with new installation steps
- Fixed bug in calculator.py where Z was incorrect

Your changes:
-
-
-

## Django-Specific Changes

<!-- Check if your PR affects any of these -->

- [ ] Database migrations created and tested (`python manage.py makemigrations`, `python manage.py migrate`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Settings changes documented in `core/settings/`
- [ ] New dependencies added to `requirements.txt`

## Screenshots (if applicable)

<!-- Add screenshots to help explain the changes (especially for UI changes) -->

## Testing

<!-- Describe the tests you ran and how to reproduce them -->

Example:
```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_api.py

# Run with coverage
pytest --cov=api --cov=ai_engine --cov-report=html
```

Tests performed:

Example:
- [x] Ran `pytest` - all tests passed
- [x] Tested locally with Docker Compose
- [x] Manually tested the API endpoint in browser
- [ ] Added new test cases for this feature

Your tests:
-
-
-

## Code Quality Checklist

- [ ] Code formatted with `black .`
- [ ] Imports sorted with `isort .`
- [ ] No flake8 errors (`flake8 .`)
- [ ] All pytest tests pass locally
- [ ] Code follows project style guidelines (see [CONTRIBUTING.md](../CONTRIBUTING.md))
- [ ] Self-reviewed code and added comments for complex logic
- [ ] Updated relevant documentation (README, docs/, API docs)
- [ ] No new warnings introduced

## Commit Message Convention

> **Tip**: Use [Conventional Commits](../CONTRIBUTING.md#commit-convention) format:
> - `feat:` for new features
> - `fix:` for bug fixes
> - `docs:` for documentation
> - `refactor:` for refactoring
> - `test:` for tests
> - `chore:` for maintenance

## Co-authors

<!-- If you worked with someone, add them as co-authors -->

```
Co-authored-by: Name <email@example.com>
```

## Additional Notes

<!-- Any additional information or context, such as: -->
<!-- - Breaking changes documentation -->
<!-- - Migration steps required -->
<!-- - Configuration changes needed -->
<!-- - Known limitations -->
