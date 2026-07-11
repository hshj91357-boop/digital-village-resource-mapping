# Contributing to Digital Village Resource Mapping

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/digital-village-resource-mapping.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature-name`
7. Open a Pull Request

## Code Style

### Python
- Follow PEP 8
- Use Black for formatting: `black .`
- Use isort for imports: `isort .`
- Type hints required for functions
- Docstrings required for all functions/classes

### TypeScript/React
- Use Prettier for formatting
- ESLint configuration enforced
- Functional components with hooks
- Props should be typed
- Avoid prop drilling, use context when needed

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Commit Messages

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for test changes

Example: `feat: add flood risk map generation`

## Development Process

1. **Phase 1**: UI Foundation ✅
2. **Phase 2**: GIS Integration 🔄
3. **Phase 3**: Remote Sensing
4. **Phase 4**: AI Detection
5. **Phase 5**: Analytics
6. **Phase 6**: Validation & Deployment

Always work on features aligned with the current phase.

## Reporting Issues

When reporting issues, include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots/logs if applicable

## Pull Request Process

1. Update README.md with any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Request review from maintainers
5. Address review comments
6. Merge only after approval

## Questions?

Open an issue or discussion on GitHub!
