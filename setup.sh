#!/bin/bash

echo "🚀 Setting up SocialTab..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your MongoDB Atlas connection string!"
    echo "   1. Go to https://www.mongodb.com/cloud/atlas"
    echo "   2. Create a free cluster"
    echo "   3. Get your connection string"
    echo "   4. Update MONGODB_URL in .env file"
    echo "   5. Generate a strong SECRET_KEY"
    echo ""
else
    echo "✓ .env file found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your MongoDB Atlas credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: uvicorn main:app --reload"
echo "4. Open: http://localhost:8000"
echo ""
echo "Happy coding! 💚"
