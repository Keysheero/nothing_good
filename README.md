# Telegram Message Distribution Bot

Welcome to the Telegram Message Distribution Bot project! This bot is designed to facilitate efficient message dissemination across various channels on the Telegram platform.

## Getting Started

Follow these steps to deploy the bot using Docker Compose:

1. **Create Environment File (.env)**:
   - In the /src/ of your project, create a file named `.env`.
   - Define the required environment variables in the `.env` file. Example:
     ```dotenv
     

     # PostgreSQL Database Configuration
     DB_NAME=your_db_name
     DB_PORT=5432
     DB_HOST=your_db_host
     DB_PASSWORD=your_db_password
     DB_USER=your_db_user
     
     # Telegram Bot Configuration
     BOT_TOKEN=your_bot_token
     BOT_NAME=your_bot_name
     
     # Redis Configuration
     REDIS_DATABASE=your_redis_database
     REDIS_HOST=your_redis_host
     REDIS_PORT=your_redis_port
     REDIS_TTL_STATE=your_redis_ttl_state
     REDIS_TTL_DATA=your_redis_ttl_data
     ```

2. **Configure Docker Compose**:
   - Open the `docker-compose.yaml` file in the root of your project.
   - Ensure that the file includes necessary configurations for your services.

3. **Build and Run the Docker Containers**:
   ```bash
   docker-compose --env-file .\src\.env  -f docker-compose.yaml up --build
