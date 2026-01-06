# Contributing to Spiritual G-Code

First off, thank you for considering contributing to Spiritual G-Code! It's people like you that make Spiritual G-Code such a great tool.

## 🌟 The Spiritual G-Code Community

Our community is built on **transdisciplinary collaboration**—we welcome software engineers, spiritual seekers, data scientists, astrologers, designers, and anyone curious about the intersection of technology and consciousness.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
### Description
A clear and concise description of what the bug is.

### To Reproduce
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

### Expected Behavior
A clear and concise description of what you expected to happen.

### Screenshots
If applicable, add screenshots to help explain your problem.

### Environment
- OS: [e.g. Windows 11, macOS 14, Ubuntu 22.04]
- Python Version: [e.g. 3.11.5]
- Django Version: [e.g. 5.0.1]
- Browser: [e.g. Chrome 120]

### Additional Context
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful** to most Spiritual G-Code users
- **List some examples** of how this feature would be used
- **Include mockups or screenshots** if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`.
2. **If you've added code** that should be tested, add tests.
3. **If you've changed APIs**, update the documentation.
4. **Ensure the code passes tests** (`pytest`).
5. **Format your code** with black and isort.
6. **Commit your changes** using conventional commits (see below).
7. **Push to your fork** and submit a pull request.

### Development Setup

1. Fork and clone the repository
```bash
git clone https://github.com/your-username/spiritual-g-code.git
cd spiritual-g-code
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up pre-commit hooks (optional but recommended)
```bash
pip install pre-commit
pre-commit install
```

5. Create a branch for your feature
```bash
git checkout -b feature/your-feature-name
```

6. Make your changes and test
```bash
pytest
black .
isort .
flake8
```

7. Commit your changes
```bash
git add .
git commit -m "feat: add your feature description"
```

## 📝 Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools
- **ci**: Changes to CI configuration files and scripts

**Examples:**
```bash
feat: add daily G-Code calculation endpoint
fix: resolve transit chart timezone bug
docs: update API documentation
test: add unit tests for Gemini client
```

## 🎨 Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **pylint**: Code analysis

Run all formatters and linters:
```bash
black ai_engine/ api/ core/ tests/
isort ai_engine/ api/ core/ tests/
flake8 ai_engine/ api/ core/ tests/
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator.py

# Run with coverage report
pytest --cov=api --cov=ai_engine --cov-report=html

# Run integration tests only
pytest -m integration

# Run unit tests only
pytest -m "not integration"
```

### Writing Tests

We use `pytest` and `pytest-django` for testing:

```python
# tests/test_calculator.py

import pytest
from ai_engine.calculator import GCodeCalculator

class TestGCodeCalculator:
    @pytest.fixture
    def calculator(self):
        return GCodeCalculator()

    def test_calculate_transits(self, calculator):
        result = calculator.calculate_transits(
            birth_date='1990-06-15',
            location='Taipei, Taiwan',
            target_date='2025-01-06'
        )
        assert 'sun' in result
        assert 'moon' in result
        assert result is not None
```

## 📚 Documentation

If you're adding new features or changing existing functionality, please update the documentation:

- **README.md**: Update feature lists, installation instructions, etc.
- **docs/**: Add or update technical documentation
- **API docs**: Update API endpoint documentation
- **Comments**: Add inline comments for complex logic

## 🌍 Localization

If you're interested in translating Spiritual G-Code into other languages:

1. Check `docs/TRANSLATIONS.md` for guidelines
2. Create a new translation file in `locale/`
3. Submit a pull request with your translations

## 🎯 Areas Where We Need Help

We're actively looking for contributors in these areas:

### High Priority
- [ ] **Django/DRF Development**: API endpoints, models, serializers
- [ ] **Frontend Development**: Dashboard UI with Tailwind CSS
- [ ] **Testing**: Unit tests and integration tests
- [ ] **Documentation**: API docs, user guides

### Medium Priority
- [ ] **Mobile App**: React Native or Flutter developers
- [ ] **DevOps**: Docker, Kubernetes, CI/CD
- [ ] **AI/ML**: Improve Gemini prompt engineering
- [ ] **Design**: UI/UX, graphics, branding

### Low Priority
- [ ] **Translations**: Multi-language support
- [ ] **Research**: Astrology, astronomy, consciousness studies
- [ ] **Community Management**: Moderation, events, content

## 🤔 Questions?

Feel free to open an issue with the `question` label, or join our community discussions.

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Our Standards

**Positive behavior includes:**
- Being respectful and inclusive
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, trolling, or derogatory comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Any other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned with this Code of Conduct.

## 🙏 Recognition

Contributors will be recognized in:
- The `CONTRIBUTORS.md` file
- Release notes
- The project website (when launched)

Thank you for contributing to Spiritual G-Code! 🌟
