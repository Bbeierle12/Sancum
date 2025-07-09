# Sanctum

This is a monorepo for the Sanctum project, containing the Next.js frontend and the FastAPI backend.

## Project Structure

- `frontend/`: The Next.js application.
- `backend/`: The Python FastAPI services for AI and data processing.
- `docs/`: Project documentation and plans.
- `data/`: Local SQLite database files (auto-generated at the root).

## Getting Started

### Prerequisites

- Node.js and npm
- Python 3.9+ and pip
- Docker and Docker Compose
- `ngrok` for exposing local services

### Installation

1.  **Install all dependencies:**
    ```bash
    npm install
    ```
    This will install both frontend (`npm`) and backend (`pip`) dependencies.

2.  **Environment Variables:**
    - Create a `.env` file in the root of the project.
    - Fill in the required API keys for Firebase, Google AI, and other services.
    - The `SANCTUM_API_KEY` is a secret key you create to protect your local backend services.

### Running the Application

1.  **Start the Backend Services:**
    In one terminal, run the backend services using ngrok for secure tunneling:
    ```bash
    npm run dev:backend
    ```
    Take note of the `ngrok` URLs printed in the logs. You will need these for the GPT actions configuration.

2.  **Start the Frontend Development Server:**
    In another terminal, start the Next.js app:
    ```bash
    npm run dev:frontend
    ```
    The application will be available at `http://localhost:9002`.

### Testing

To run the Python backend tests:
```bash
npm run test:backend
```
