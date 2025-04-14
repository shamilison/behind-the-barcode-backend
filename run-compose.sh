#!/bin/bash

PROJECT_NAME="behindthebarcode"
VOLUME_NAME="btb-postgres-data"
CONTAINER_NAME="btb-postgres"
DB_NAME="behind_the_barcode"  # change this if needed

# 1. Check if volume exists
if docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
  echo "✅ Volume '$VOLUME_NAME' already exists."
else
  echo "📦 Creating volume '$VOLUME_NAME'..."
  docker volume create "$VOLUME_NAME"
fi

# 2. Run Docker Compose
echo "🚀 Starting docker-compose with rebuild and force recreate..."
docker-compose -p "$PROJECT_NAME" up -d --build --force-recreate

# 3. Wait for database to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker exec -it "$CONTAINER_NAME" psql -U postgres -d "$DB_NAME" -c '\q' 2>/dev/null; do
  sleep 2
  echo "🔄 Still waiting for DB '$DB_NAME' inside container '$CONTAINER_NAME'..."
done

echo "✅ Database '$DB_NAME' is ready!"