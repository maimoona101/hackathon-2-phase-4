# Quickstart Guide: Phase II Todo Web Application

## Overview
This guide provides the essential steps to set up and run the Phase II Todo web application with full-stack capabilities.

## Prerequisites

### System Requirements
- Node.js 18+ (for Next.js frontend)
- Python 3.9+ (for FastAPI backend)
- Docker and Docker Compose
- Git

### Development Tools
- Package manager: npm or yarn
- Python virtual environment manager: pip or conda
- Code editor with TypeScript/JavaScript and Python support

## Environment Setup

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Backend Environment
```bash
# Navigate to backend directory
cd src/backend

# Create and activate Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend Environment
```bash
# Navigate to frontend directory
cd src/frontend

# Install Node.js dependencies
npm install
# or
yarn install
```

## Database Configuration

### 1. Neon PostgreSQL Setup
1. Create a Neon account at [neon.tech](https://neon.tech)
2. Create a new project and copy the connection string
3. Add the connection string to your environment variables:

```bash
# In src/backend/.env
DATABASE_URL=your_neon_connection_string
```

### 2. Environment Variables
Create `.env` files in both frontend and backend:

**Backend (.env):**
```env
DATABASE_URL=your_neon_connection_string
SECRET_KEY=your_secret_key_for_jwt_signing
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_JWT_SECRET=matching_secret_to_backend
```

## Running the Application

### 1. Start the Backend
```bash
# In src/backend directory
cd src/backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
# In src/frontend directory
cd src/frontend

# Start the Next.js development server
npm run dev
# or
yarn dev
```

### 3. Using Docker Compose (Alternative)
```bash
# From the project root directory
docker-compose up --build
```

## Authentication Setup

### Better Auth Configuration
1. The application uses Better Auth for JWT-based authentication
2. User registration and login endpoints are available at:
   - POST `/api/auth/register`
   - POST `/api/auth/login`
3. Authentication is required for all todo-related endpoints

### Testing Authentication
1. Register a new user via POST `/api/auth/register`
2. Log in via POST `/api/auth/login` to get a JWT token
3. Use the token in the Authorization header for protected endpoints

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Todo Endpoints
- `GET /api/todos` - Get all todos for authenticated user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo

### User Profile Endpoints
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile

## Development Workflow

### 1. Making Changes to Frontend
1. Edit files in `src/frontend/app/`, `src/frontend/components/`, etc.
2. Changes are reflected immediately in development mode
3. All API calls should go through the API client in `src/frontend/lib/api.ts`

### 2. Making Changes to Backend
1. Edit API endpoints in `src/backend/app/api/v1/`
2. Update models in `src/backend/app/models/`
3. Update schemas in `src/backend/app/schemas/`
4. Restart the server to see changes (or use `--reload` flag)

### 3. Database Changes
1. Update models in `src/backend/app/models/`
2. Generate a new migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```
3. Apply the migration:
   ```bash
   alembic upgrade head
   ```

## Testing

### Backend Tests
```bash
# In src/backend directory
cd src/backend
pytest
```

### Frontend Tests
```bash
# In src/frontend directory
cd src/frontend
npm test
# or
yarn test
```

## Project Structure
```
project-root/
├── src/
│   ├── frontend/          # Next.js application
│   │   ├── app/          # App Router pages
│   │   ├── components/   # Reusable components
│   │   ├── lib/          # Utilities and API client
│   │   └── public/       # Static assets
│   └── backend/          # FastAPI application
│       ├── app/          # Application code
│       ├── models/       # SQLModel database models
│       ├── schemas/      # Pydantic schemas
│       ├── api/          # API routes
│       └── tests/        # Backend tests
├── specs/                # Specification files
└── docker-compose.yml    # Container configuration
```

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure Neon PostgreSQL connection string is correct
2. **Authentication**: Verify that JWT secrets match between frontend and backend
3. **Port Conflicts**: Change ports in configuration if 8000 or 3000 are in use
4. **Dependency Issues**: Reinstall dependencies if modules are missing

### Useful Commands
- `npm run dev` or `yarn dev`: Start frontend development server
- `uvicorn app.main:app --reload --port 8000`: Start backend development server
- `alembic upgrade head`: Apply database migrations
- `pytest`: Run backend tests
- `npm test` or `yarn test`: Run frontend tests

## Next Steps
1. Explore the API documentation at `/docs` when the backend is running
2. Customize the UI components in the `src/frontend/components/` directory
3. Add new features by following the established patterns in both frontend and backend
4. Set up your production environment with the same architecture