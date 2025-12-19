# SocialTab - Technical Documentation

## Project Overview

SocialTab is a social credit ledger application designed to track informal debts between friends without the awkwardness. Built for HackForge'25 WB-3 Challenge.

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.8+
- **Database**: MongoDB Atlas (NoSQL)
- **Authentication**: JWT tokens with bcrypt hashing
- **API Style**: RESTful

### Frontend
- **Template Engine**: Jinja2
- **Styling**: Custom CSS with CSS Grid/Flexbox
- **JavaScript**: Vanilla JS (ES6+)
- **Animations**: AOS (Animate On Scroll) + Custom CSS animations

### Database Schema

#### Users Collection
```json
{
  "_id": ObjectId,
  "username": "string (unique, lowercase)",
  "email": "string (unique)",
  "pin_hash": "string (bcrypt hashed)",
  "full_name": "string (optional)",
  "created_at": "datetime",
  "total_owed": "float",
  "total_owing": "float"
}
```

#### Debts Collection
```json
{
  "_id": ObjectId,
  "creditor_username": "string",
  "creditor_id": ObjectId,
  "debtor_username": "string",
  "debtor_id": ObjectId,
  "amount": "float",
  "description": "string",
  "status": "pending|active|disputed|paid|archived",
  "debt_type": "single|group",
  "participants": "array (optional, for group debts)",
  "created_at": "datetime",
  "updated_at": "datetime",
  "paid_at": "datetime (optional)",
  "dispute_reason": "string (optional)"
}
```

#### Notifications Collection
```json
{
  "_id": ObjectId,
  "user_username": "string",
  "notification_type": "debt_request|debt_accepted|debt_disputed|payment_request|payment_confirmed|reminder",
  "title": "string",
  "message": "string",
  "debt_id": "string (optional)",
  "action_url": "string (optional)",
  "read": "boolean",
  "created_at": "datetime"
}
```

## API Endpoints

### Authentication (`/auth`)

#### POST /auth/signup
Create a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "pin": "1234",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "username": "johndoe"
}
```

#### POST /auth/login
Login with username and PIN.

**Request Body:**
```json
{
  "username": "johndoe",
  "pin": "1234"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "username": "johndoe"
}
```

#### POST /auth/logout
Logout current user (clears cookie).

### Debts (`/debts`)

#### POST /debts/create
Create a new debt.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "debtor_username": "janedoe",
  "amount": 25.50,
  "description": "Lunch at cafe",
  "debt_type": "single"
}
```

**Response:**
```json
{
  "message": "Debt created successfully",
  "debt_id": "507f1f77bcf86cd799439011",
  "status": "pending_acceptance"
}
```

#### GET /debts/my-debts
Get all debts for current user.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "owed_to_me": [...],
  "i_owe": [...],
  "total_owed_to_me": 150.00,
  "total_i_owe": 75.00
}
```

#### GET /debts/history
Get debt history (paid/archived).

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "history": [...]
}
```

#### GET /debts/{debt_id}
Get specific debt details.

**Headers:** `Authorization: Bearer <token>`

#### POST /debts/{debt_id}/action
Perform action on debt.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "action": "accept|dispute|mark_paid",
  "reason": "optional dispute reason"
}
```

#### DELETE /debts/{debt_id}
Delete a pending debt (creditor only).

**Headers:** `Authorization: Bearer <token>`

### Users (`/users`)

#### GET /users/me
Get current user profile.

**Headers:** `Authorization: Bearer <token>`

#### GET /users/search/{username}
Search for a user by username.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "username": "janedoe",
  "full_name": "Jane Doe",
  "exists": true
}
```

#### GET /users/notifications
Get user notifications.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "notifications": [...],
  "unread_count": 3
}
```

#### POST /users/notifications/{notification_id}/read
Mark notification as read.

**Headers:** `Authorization: Bearer <token>`

#### GET /users/stats
Get user statistics.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "total_debts_created": 10,
  "total_debts_received": 5,
  "active_debts": 3,
  "paid_debts": 12,
  "total_owed_to_me": 150.00,
  "total_i_owe": 75.00,
  "net_balance": 75.00
}
```

## Security Features

### 1. Encrypted Storage
- All data stored in MongoDB Atlas with TLS encryption
- Connection strings use SSL/TLS
- Database credentials stored in environment variables

### 2. Biometric Login Simulation
- PIN-based authentication (4-6 digits)
- Passwords hashed using bcrypt with salt rounds
- JWT tokens for session management
- Tokens expire after 7 days

### 3. Dead Man's Switch
- Implemented via `is_debt_expired()` helper function
- Automatically archives debts older than 90 days
- Can be triggered via scheduled job (not implemented in MVP)

### 4. Input Validation
- Pydantic models validate all inputs
- SQL injection prevention (NoSQL database)
- XSS prevention via Jinja2 auto-escaping
- CORS configured for production

### 5. Consensus System
- Both parties must accept debts
- Prevents fake IOUs
- Dispute mechanism for disagreements

## Design System

### Color Palette
- **Primary Green**: `#10b981` - Trust, growth, money
- **Dark Green**: `#059669` - Accents, hover states
- **Light Green**: `#d1fae5` - Backgrounds, highlights
- **White**: `#ffffff` - Clean, minimal
- **Light Gray**: `#f3f4f6` - Backgrounds
- **Gray**: `#9ca3af` - Secondary text
- **Dark Gray**: `#4b5563` - Tertiary text
- **Dark Text**: `#1f2937` - Primary text

### Typography
- **Font Family**: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto)
- **Base Size**: 16px
- **Line Height**: 1.6
- **Headings**: Bold, larger sizes

### Animations
1. **Fade In Up**: Hero content, features
2. **Slide Down**: Navbar on load
3. **Float**: Floating cards in hero
4. **Scale In**: Auth cards
5. **Slide In Left**: Debt cards
6. **Slide In Right**: Toast notifications
7. **Rotate**: Feature icons on hover

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## User Flows

### 1. Sign Up Flow
1. User visits landing page
2. Clicks "Sign Up"
3. Fills form (username, email, PIN)
4. Account created, JWT token issued
5. Redirected to dashboard

### 2. Create Debt Flow
1. User clicks "New Debt" on dashboard
2. Modal opens
3. Enters debtor username (validated in real-time)
4. Enters amount and description
5. Submits form
6. Debt created with "pending" status
7. Debtor receives notification

### 3. Accept Debt Flow
1. Debtor sees notification
2. Views debt in "I Owe" tab
3. Clicks "Accept"
4. Debt status changes to "active"
5. Both users' totals updated
6. Creditor receives notification

### 4. Pay Debt Flow
1. Debtor pays creditor (outside app)
2. Debtor clicks "Mark as Paid"
3. Debt status changes to "paid"
4. Both users' totals updated
5. Debt moves to history
6. Creditor receives notification

## Performance Optimizations

1. **Database Indexing**: Username, email fields indexed
2. **Lazy Loading**: Debts loaded on demand
3. **Caching**: LocalStorage for tokens
4. **Async Operations**: All API calls async
5. **Pagination**: History limited to 50 items
6. **Debouncing**: User search debounced (500ms)

## Testing Checklist

### Functional Testing
- [ ] User registration
- [ ] User login
- [ ] Create debt
- [ ] Accept debt
- [ ] Dispute debt
- [ ] Mark as paid
- [ ] Delete pending debt
- [ ] View notifications
- [ ] View history
- [ ] User search
- [ ] Logout

### Security Testing
- [ ] SQL injection attempts
- [ ] XSS attempts
- [ ] CSRF protection
- [ ] Token expiration
- [ ] Unauthorized access
- [ ] PIN validation

### UI/UX Testing
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Animations smooth
- [ ] Forms validate properly
- [ ] Error messages clear
- [ ] Loading states visible
- [ ] Toast notifications work

## Deployment

### Prerequisites
1. Python 3.8+
2. MongoDB Atlas account
3. Domain (optional)

### Steps
1. Clone repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` file with MongoDB URL and secret key
5. Run: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Production Considerations
1. Use HTTPS (SSL/TLS)
2. Set strong SECRET_KEY
3. Configure CORS properly
4. Enable rate limiting
5. Set up monitoring
6. Configure backups
7. Use process manager (PM2, systemd)
8. Set up reverse proxy (Nginx)

## Future Enhancements

1. **Mobile App**: React Native or Flutter
2. **Push Notifications**: Firebase Cloud Messaging
3. **Payment Integration**: Stripe, PayPal, Venmo
4. **AI Features**: Debt prediction, smart reminders
5. **Social Features**: Friend suggestions, activity feed
6. **Multi-Currency**: Support for different currencies
7. **Receipt Upload**: Photo evidence of transactions
8. **Group Optimization**: Simplify complex group debts
9. **Recurring Debts**: Monthly rent, subscriptions
10. **Analytics Dashboard**: Spending insights

## Support

For issues or questions:
- Check documentation
- Review code comments
- Test with sample data
- Check MongoDB Atlas connection

## License

MIT License - Free to use and modify

---

**Built with 💚 for HackForge'25**
