# Spotify-last-songs

🎵 **Billboard Tracker**  
A full-stack music web app that fetches the Billboard Hot 100 playlist from Spotify, stores it in a PostgreSQL database, and displays it in a responsive web interface built with Flask and Jinja2.

---

## 🔑 Environment Setup

To use this project locally, you’ll need a Spotify Developer account and an `.env` file.

### 📄 `.env` File Format

client_id=YOUR_SPOTIFY_CLIENT_ID
client_secret=YOUR_SPOTIFY_CLIENT_SECRET
API_KEY=YOUR_OPTIONAL_API_KEY

yaml
Copy
Edit

### ⚙️ `PullSpotifyToken.ps1`

This PowerShell script automatically pulls a fresh Spotify access token using the credentials in your `.env` file.  
It creates a **plug-and-play environment** by streamlining the token generation process for local development.

---

## ✅ Keploy Test Integration

This app uses [Keploy](https://keploy.io) to auto-generate API tests from real traffic.

### 📦 GitHub Actions CI/CD

Keploy runs automatically on every push to `main`.  
See the workflow file: [`.github/workflows/keploy-test.yml`](.github/workflows/keploy-test.yml)

### 🧪 Test Report Screenshot

_Add your screenshot here after your first test run:_

![Keploy Screenshot](./keploy-screenshot.png)