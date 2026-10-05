FROM node:20-bookworm-slim
WORKDIR /app/front
COPY front/package.json front/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY front/ ./
RUN mkdir -p src/assets /app/back/app/dal/images
EXPOSE 4200
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
