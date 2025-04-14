# Soccer Rankings Application

A Flask-based web application for tracking and displaying soccer team rankings.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- Google Cloud account (for Cloud SQL and Cloud Run deployment)
- Docker (for containerization)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd soccer_ranking
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Setup

### Local Development

1. Create a `.env.local` file in the project root:
```bash
touch .env.local
```

2. Add the following environment variables to `.env.local`:
```env
# Flask configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database configuration
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
USE_CLOUD_SQL=false

# Cloud SQL configuration (if using Cloud SQL locally)
CLOUD_SQL_CONNECTION_NAME=your-project:region:instance
```

3. For local development with Cloud SQL, install and configure Cloud SQL Proxy:
```bash
# Download Cloud SQL Proxy
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
chmod +x cloud_sql_proxy

# Start Cloud SQL Proxy
./cloud_sql_proxy -instances=your-project:region:instance=tcp:5432
```

### Cloud Run Deployment

1. Create a `.env.cloud` file for production settings:
```bash
touch .env.cloud
```

2. Add the following environment variables to `.env.cloud`:
```env
# Flask configuration
SECRET_KEY=your-production-secret-key

# Database configuration
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
USE_CLOUD_SQL=true
CLOUD_SQL_CONNECTION_NAME=your-project:region:instance
```

## Running the Application

### Local Development

1. Switch to local environment:
```bash
./switch_env.sh local
```

2. Start the application:
```bash
python3 -m flask run
```

### Cloud Run Deployment

1. Switch to cloud environment:
```bash
./switch_env.sh cloud
```

2. Build and deploy using the deployment script:
```bash
./deploy.sh soccer-rankings-with-registration
```

3. The script will:
   - Set up necessary secrets in Cloud Secret Manager
   - Build and push the Docker image
   - Deploy to Cloud Run with proper configuration

## Database Setup

1. Create the database:
```bash
createdb -U your_db_user your_db_name
```

2. The application will automatically create the necessary tables when it starts up for the first time.

## Features

- User registration and authentication
- Team rankings display
- Game results tracking
- Historical data analysis
- State and gender-based filtering

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 