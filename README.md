# My Enhanced Agent App (Dagger.io + OpenHands AI)

This enhanced version shows seamless frontend-backend-database interaction using containerized services orchestrated with Dagger.io.

## 🚀 Quick Start

### Run with Dagger

```bash
# Install Dagger dependencies
pip install -r agent/requirements.txt

# Run the application with Dagger
python agent/main.py
```

Then visit the React app:
- Frontend: http://localhost:3000
- API Health Check: http://localhost:5000/api/health
- API Quotes: http://localhost:5000/api/quotes

Click the "Load Quotes" button to fetch quotes stored in PostgreSQL via Flask API.

### Alternative: Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🔄 Interaction Flow

- User clicks button in React.
- React frontend makes fetch request to Flask API.
- Flask API queries PostgreSQL database.
- Quotes retrieved from DB and returned to frontend.
- React displays quotes seamlessly.

## 🛠 Technologies Demonstrated

- React frontend containerized separately.
- Flask middleware containerized separately.
- PostgreSQL DB containerized separately.
- Dagger.io orchestration.
- OpenHands AI for automated pipeline and testing.

## 🔎 How it Works Seamlessly

- React (Frontend) sends fetch request (`/api/quotes`).
- Flask API (Middleware) receives, queries PostgreSQL (DB container).
- PostgreSQL returns data → Flask → React.
- Displayed clearly, demonstrating networked, multi-container communication.

## 📌 Why This Matters

This small but meaningful example demonstrates a clear separation of concerns and the value of containerization, orchestration (Dagger.io), and AI-powered automation (OpenHands).

## 📂 Repository Structure

```
my-agent-app/
├── .dagger/           # Dagger cache directory
├── agent/             # Dagger orchestration code
├── frontend/          # React frontend application
├── api/               # Flask API middleware
├── db/                # PostgreSQL database initialization
└── docker-compose.yml # Alternative to Dagger for local development
```

## ✅ Verification

Ensure interaction by clicking the button in the React frontend. You should see quotes loaded from the database.
