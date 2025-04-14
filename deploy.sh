#!/bin/bash

# Exit on error
set -e

# Valid service names
VALID_SERVICES=(
    "soccer-rankings-without-registration"
    "soccer-rankings-with-registration"
)

# Show usage
usage() {
    echo "Usage: $0 <service-name>"
    echo "Available service names:"
    for service in "${VALID_SERVICES[@]}"; do
        echo "  - $service"
    done
    exit 1
}

# Validate service name
if [ $# -ne 1 ]; then
    echo "❌ Error: Service name is required"
    usage
fi

SERVICE_NAME=$1
VALID_SERVICE=0
for valid_service in "${VALID_SERVICES[@]}"; do
    if [ "$SERVICE_NAME" == "$valid_service" ]; then
        VALID_SERVICE=1
        break
    fi
done

if [ $VALID_SERVICE -eq 0 ]; then
    echo "❌ Error: Invalid service name: $SERVICE_NAME"
    usage
fi

# Configuration
PROJECT_ID="scoutmagi-soccer"
REGION="us-central1"
CLOUD_SQL_INSTANCE="soccer-rankings-db"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
DB_PASSWORD="mIt1983@486"

echo "🚀 Starting deployment process for service: ${SERVICE_NAME}..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK (gcloud) is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! gcloud auth print-identity-token &> /dev/null; then
    echo "🔑 Please login to Google Cloud first:"
    gcloud auth login
fi

# Set the project
echo "🎯 Setting Google Cloud project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    secretmanager.googleapis.com \
    sqladmin.googleapis.com

# Create secrets if they don't exist
echo "🔒 Setting up secrets..."
if ! gcloud secrets describe ${SERVICE_NAME}-db-password &> /dev/null; then
    echo "Creating database password secret..."
    echo -n "${DB_PASSWORD}" | gcloud secrets create ${SERVICE_NAME}-db-password --data-file=-
fi

if ! gcloud secrets describe ${SERVICE_NAME}-secret-key &> /dev/null; then
    echo "Creating Flask secret key..."
    FLASK_SECRET_KEY=$(openssl rand -base64 32)
    echo -n "${FLASK_SECRET_KEY}" | gcloud secrets create ${SERVICE_NAME}-secret-key --data-file=-
fi

# Build and push the Docker image
echo "🏗️ Building and pushing Docker image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --add-cloudsql-instances ${PROJECT_ID}:${REGION}:${CLOUD_SQL_INSTANCE} \
    --set-env-vars="USE_CLOUD_SQL=true" \
    --set-env-vars="DB_USER=scoutmagi" \
    --set-env-vars="DB_NAME=users" \
    --set-env-vars="DB_HOST=/cloudsql/${PROJECT_ID}:${REGION}:${CLOUD_SQL_INSTANCE}" \
    --set-env-vars="CLOUD_SQL_CONNECTION_NAME=${PROJECT_ID}:${REGION}:${CLOUD_SQL_INSTANCE}" \
    --set-secrets="DB_PASSWORD=${SERVICE_NAME}-db-password:latest" \
    --set-secrets="SECRET_KEY=${SERVICE_NAME}-secret-key:latest"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)')

echo "✅ Deployment completed successfully!"
echo "🌎 Your application is available at: ${SERVICE_URL}"
echo "
Next steps:
1. Visit ${SERVICE_URL} to verify the deployment
2. Check the logs in Cloud Console if you encounter any issues
3. Monitor the service in Cloud Run dashboard

To view logs:
gcloud logging tail \"resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}\"
" 