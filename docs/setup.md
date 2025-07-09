# Setup Guide

## 1. Install Dependencies

This project uses `npm` workspaces. Installing from the root will install frontend dependencies. Backend dependencies must be installed separately.

```bash
npm install
npm run install:backend
```

## 2. Environment Variables

Copy `.env.example` to `.env` and set your `SANCTUM_API_KEY`.

```bash
cp .env.example .env
```

## 3. Run the Servers

Start the backend Python API services with ngrok tunneling:

```bash
npm run dev:backend
```

In another terminal, run the Next.js frontend:

```bash
npm run dev
```

The app will be available at `http://localhost:9002`.
