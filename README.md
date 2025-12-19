# SocialTab - The "I'll Pay You Later" Protocol

## 🎯 Problem Statement
SocialTab solves the awkward problem of tracking informal debts between friends. No more forgotten IOUs or uncomfortable money conversations.

## ✨ Features

### Core Functionality
- **Quick Capture**: Log debts in seconds with an intuitive interface
- **Consensus System**: Both parties must accept debts to prevent fraud
- **Group Splitting**: Handle complex group expenses with automatic calculations
- **Smart Notifications**: Gentle reminders using psychology, not pressure
- **Dispute Resolution**: Handle disagreements gracefully

### Security Features
- **Encrypted Storage**: All data encrypted in MongoDB Atlas
- **Biometric Simulation**: PIN-based authentication system
- **Session Management**: Secure token-based sessions
- **Dead Man's Switch**: Auto-archive old debts after 90 days

### UX Enhancements
- **Instant Feedback**: Real-time animations and updates
- **Dashboard Analytics**: Visual debt summaries
- **Payment Tracking**: Mark debts as paid with confirmation
- **Search & Filter**: Find debts quickly

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: Jinja2 Templates with modern CSS/JS
- **Database**: MongoDB Atlas
- **Authentication**: JWT tokens with bcrypt
- **Styling**: Custom CSS with green/white theme
- **Animations**: CSS animations + AOS (Animate On Scroll)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (free tier works)
- pip package manager

### Setup Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd socialtab
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure MongoDB Atlas**
- Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Get your connection string
- Create a `.env` file in the root directory:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/socialtab?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here-change-this-in-production
```

5. **Run the application**
```bash
uvicorn main:app --reload
```

6. **Access the app**
Open your browser and navigate to: `http://localhost:8000`

## 🎨 Design Philosophy

### Color Scheme
- **Primary Green**: #10b981 (Trust, growth, money)
- **Dark Green**: #059669 (Accents, hover states)
- **White**: #ffffff (Clean, minimal)
- **Light Gray**: #f3f4f6 (Backgrounds)
- **Dark Text**: #1f2937 (Readability)

### Animation Strategy
- Smooth transitions (300ms ease)
- Fade-in effects on page load
- Hover animations for interactivity
- Success/error feedback animations
- Skeleton loaders for async operations

## 🚀 Usage Guide

### Creating an Account
1. Click "Sign Up" on the homepage
2. Enter username, email, and create a PIN (4-6 digits)
3. Verify your account

### Logging a Debt
1. Click "New Debt" from dashboard
2. Enter amount, description, and debtor's username
3. Submit - the other party receives a notification
4. They must accept for the debt to be active

### Group Expenses
1. Click "Group Split"
2. Enter total amount and description
3. Add participants
4. Choose split type (equal or custom)
5. All participants receive acceptance requests

### Settling Debts
1. View your debts in the dashboard
2. Click "Mark as Paid"
3. Other party confirms payment
4. Debt moves to history

## 📁 Project Structure

```
socialtab/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── models/
│   ├── user.py            # User data models
│   ├── debt.py            # Debt data models
│   └── notification.py    # Notification models
├── routes/
│   ├── auth.py            # Authentication routes
│   ├── debts.py           # Debt management routes
│   └── users.py           # User profile routes
├── utils/
│   ├── database.py        # MongoDB connection
│   ├── security.py        # Authentication utilities
│   └── helpers.py         # Helper functions
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   ├── js/
│   │   └── app.js         # Frontend JavaScript
│   └── images/            # Static images
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Landing page
    ├── dashboard.html     # User dashboard
    ├── login.html         # Login page
    ├── signup.html        # Registration page
    └── debt_detail.html   # Debt details page
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt rounds
- **JWT Tokens**: Secure session management
- **Input Validation**: Pydantic models for all inputs
- **CORS Protection**: Configured for production
- **Rate Limiting**: Prevent abuse (optional, can be added)

## 🎯 Hackathon Deliverables

✅ Single ZIP file structure
✅ Complete source code
✅ Encrypted storage (MongoDB Atlas with TLS)
✅ Biometric login simulation (PIN-based)
✅ Dead Man's Switch (90-day auto-archive)
✅ Prototype screenshots in `/screenshots` folder
✅ Documentation (this README + inline comments)

## 🐛 Troubleshooting

**MongoDB Connection Issues**
- Verify your connection string in `.env`
- Check IP whitelist in MongoDB Atlas (allow 0.0.0.0/0 for testing)
- Ensure network access is configured

**Port Already in Use**
```bash
uvicorn main:app --reload --port 8001
```

**Dependencies Not Installing**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

## 🚀 Future Enhancements

- Mobile app (React Native/Flutter)
- Push notifications (Firebase)
- Payment gateway integration (Stripe/PayPal)
- AI-powered debt prediction
- Social features (friend suggestions)
- Multi-currency support
- Receipt photo uploads

## 👥 Team

Built for HackForge'25 - WB-3 Challenge

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- MongoDB Atlas for reliable database hosting
- AOS library for scroll animations
- The problem statement sponsors: WEBBED

---

**Made with 💚 for better friendships and clearer finances**
