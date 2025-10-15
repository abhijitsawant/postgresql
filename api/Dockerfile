# Use official Node.js LTS Alpine image
FROM node:20-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy app source
COPY index.js ./

# Expose port 3000
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
