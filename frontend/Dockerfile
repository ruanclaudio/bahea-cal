FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Install serve to serve the built React application
RUN npm install -g serve

# Command to run the application
CMD ["serve", "-s", "build"]
