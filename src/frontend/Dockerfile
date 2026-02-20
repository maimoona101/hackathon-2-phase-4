# Use Node image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install
COPY package*.json ./
RUN npm install

# Copy rest of the app
COPY . .

# Build Next.js
RUN npm run build

# Start server
EXPOSE 3000
CMD ["npm", "start"]