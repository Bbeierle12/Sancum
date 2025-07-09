# Sanctum

Sanctum is an experimental scripture study toolkit built with **Next.js** for the frontend and **FastAPI** services for backend processing. It explores ideas like spaced repetition, pivot detection in text, and journaling prompts to deepen scriptural engagement.

## Features
- Scripture flashcards powered by the SM-2 spaced repetition algorithm
- Text analysis service that finds chiastic and golden ratio patterns
- Journaling endpoints to record impressions and fulfillment notes
- Firebase Auth based user authentication (planned)

## Getting Started
### 1. Install Dependencies
This project uses `npm` workspaces. Installing from the root will install frontend dependencies. Backend dependencies must be installed separately.
```bash
npm install
npm run install:backend
```

### 2. Environment Variables
Copy `.env.example` to `.env` and adjust as needed:
```bash
cp .env.example .env
```
`SANCTUM_API_KEY` is used to protect the FastAPI endpoints. If not set, the services run in development mode and allow all requests while logging a warning. **Always set a strong key in production.**

### 3. Run the Servers
Start the backend Python API services with ngrok tunneling:
```bash
npm run dev:backend
```
In another terminal, run the Next.js frontend:
```bash
npm run dev
```
The app will be available at `http://localhost:9002`.

## Formatting and Pre-commit Hooks
This repo uses [Black](https://github.com/psf/black) and [Prettier](https://prettier.io/) via [pre-commit](https://pre-commit.com). Install the hooks once with:
```bash
pip install pre-commit
pre-commit install
```
You can manually format the code at any time using:
```bash
npm run format
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute and run tests.

## License
This project is licensed under the [MIT License](LICENSE).
