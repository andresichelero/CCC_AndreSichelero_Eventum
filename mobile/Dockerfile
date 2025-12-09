FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# Install dependencies
RUN npm install

COPY . .

# Expose the port the app runs on
EXPOSE 8100

# Start the app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "8100"]
