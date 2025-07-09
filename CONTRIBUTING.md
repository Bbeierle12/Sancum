# Contributing

Thank you for considering contributing to Sanctum!

## Setup

1. Install Node.js dependencies for the frontend (from the root directory):
   ```bash
   npm install
   ```
2. Install Python dependencies for the backend:
   ```bash
   npm run install:backend
   ```
3. Install pre-commit hooks to ensure code quality and consistent formatting:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Running Tests

Run Python tests for the backend from the root directory:

```bash
npm run test:backend
```

## Formatting

Before committing your changes, please run the formatter to ensure your code matches the project's style guidelines.

```bash
npm run format
```

This will run both Black (for Python) and Prettier (for frontend files) as defined in the `.pre-commit-config.yaml`.
