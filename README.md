# proxy-free-attendance-system
Proxy-Free Attendance System using JWT authentication and CIDR-based IP validation to prevent proxy attendance. Professors manage time-bound sessions, while students can mark attendance only within authorized classroom networks, ensuring secure, real-time and tamper-resistant tracking.
# Proxy-Free Attendance System

## 🚀 Features
- JWT Authentication
- Professor-controlled attendance sessions
- IP-based classroom validation
- 10-minute attendance window
- Student self-mark attendance
- Session analytics and export

## 🛠 Tech Stack
- Backend: Node.js, Express, PostgreSQL
- Frontend: React (Vite), TailwindCSS
- Authentication: JWT

## 📂 Project Structure
- proxy-attendance-backend
- proxy-attendance-frontend

## ⚙️ Setup

### Backend
cd proxy-attendance-backend
npm install
npm start

### Frontend
cd proxy-attendance-frontend
npm install
npm run dev

## 🔐 Environment Variables

Create `.env` in backend:

JWT_SECRET=your_secret
DB_HOST=localhost
DB_USER=your_user
DB_PASS=your_pass
DB_NAME=your_db

## 📌 API Endpoints
- POST /api/auth/login
- POST /api/attendance/start
- POST /api/attendance/mark
- POST /api/attendance/close
- GET /api/attendance/session/:id/status
