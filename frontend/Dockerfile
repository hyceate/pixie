FROM oven/bun:1 AS base

# Set the working directory in the container
WORKDIR /app

# Copy the package files and install dependencies
COPY . .

# Expose the application port
EXPOSE 5173

# Define the command to run the application
CMD ["bun", "dev"]