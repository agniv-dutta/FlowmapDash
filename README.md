# FlowmapDash

A modern user analytics dashboard for tracking and visualizing user sessions, events, and behavioral patterns in real-time.

## 🚀 Features

### Frontend (React + TypeScript)
- **Real-time Dashboard**: Live overview of user sessions and events
- **Interactive Charts**: Powered by Recharts for beautiful data visualization
- **Advanced Data Tables**: TanStack Table v8 with sorting, filtering, pagination, and CSV export
- **Responsive Design**: Mobile-friendly interface built with TailwindCSS
- **React Router v6**: Seamless navigation between Dashboard, Sessions, Heatmap, and Settings
- **State Management**: Zustand for global state management
- **Data Fetching**: React Query for efficient server state management

### Backend (Flask + MongoDB)
- **RESTful API**: Well-structured API endpoints for sessions, events, and analytics
- **MongoDB Integration**: Scalable NoSQL database for storing user data
- **Rate Limiting**: Built-in rate limiting to prevent API abuse
- **CORS Support**: Configurable cross-origin resource sharing
- **Environment Configuration**: Flexible configuration for development, testing, and production
- **Docker Support**: Containerized deployment with Docker Compose

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (v4.4 or higher) - or MongoDB Atlas account
- **npm** or **yarn**

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FlowmapDash
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
# Set MONGO_URI to your MongoDB connection string
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file (if needed)
echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env
```

## 🏃 Running the Application

### Development Mode

**Backend:**
```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
flask run
```
Backend will run on `http://localhost:5000`

**Frontend:**
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:5173` (or next available port)

### Production Mode

**Using Docker Compose:**
```bash
docker-compose up -d
```

**Manual Deployment:**

Backend:
```bash
cd backend
gunicorn -c gunicorn.conf.py wsgi:app
```

Frontend:
```bash
cd frontend
npm run build
npm run preview
```

## 📁 Project Structure

```
FlowmapDash/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utilities and helpers
│   │   ├── models.py        # Database models
│   │   └── exceptions.py    # Custom exceptions
│   ├── config.py            # Configuration management
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── docker-compose.yml   # Docker Compose setup
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── api/             # API client and endpoints
│   │   ├── store/           # Zustand store
│   │   ├── types/           # TypeScript types
│   │   └── lib/             # Utility functions
│   ├── package.json         # Node dependencies
│   ├── vite.config.ts       # Vite configuration
│   └── tailwind.config.js   # TailwindCSS configuration
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required
SECRET_KEY=change-me-in-production
MONGO_URI=mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/flowmapdash?retryWrites=true&w=majority

# Environment
FLASK_ENV=development
LOG_LEVEL=INFO
APP_VERSION=1.0.0

# MongoDB
MONGO_DB_NAME=flowmapdash
MONGO_POOL_SIZE=50

# CORS
CORS_ORIGINS=http://localhost:3000

# Rate Limiting
RATELIMIT_CAPACITY=200
RATELIMIT_REFILL_RATE=20.0

# Flask (dev only)
FLASK_DEBUG=1
```

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

## 📊 API Endpoints

### Sessions
- `GET /api/v1/sessions` - List all sessions
- `GET /api/v1/sessions/:id` - Get session details
- `GET /api/v1/sessions/:id/events` - Get events for a session

### Events
- `GET /api/v1/events` - List all events
- `POST /api/v1/events` - Create a new event

### Analytics
- `GET /api/v1/analytics/summary` - Get analytics summary

### Heatmap
- `GET /api/v1/heatmap` - Get heatmap data

## 🎨 Frontend Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router v6** - Routing
- **TanStack React Query** - Data fetching and caching
- **TanStack React Table v8** - Data tables
- **Recharts** - Charting library
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 🔙 Backend Technologies

- **Flask** - Web framework
- **MongoDB** - Database
- **MongoEngine** - ODM for MongoDB
- **Gunicorn** - WSGI HTTP Server
- **Flask-CORS** - CORS support
- **Pydantic** - Data validation
- **Python-dotenv** - Environment variable management

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Deployment

### Render (Backend)
The backend includes a `render.yaml` configuration for easy deployment on Render.

### Vercel/Netlify (Frontend)
The frontend can be deployed to Vercel or Netlify with a simple build command.

### Docker
```bash
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with modern web technologies
- Inspired by the need for better user analytics tools
- Thanks to the open-source community for the amazing libraries

## 📞 Support

For support, please open an issue in the repository or contact the development team.

---

**Note**: This is a work-in-progress project. Some features are still under development.
