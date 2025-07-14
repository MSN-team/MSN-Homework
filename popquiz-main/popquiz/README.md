# PopQuiz API

This is a basic Python project using FastAPI and MongoDB for the PopQuiz application.

## Requirements
- Python 3.10+
- MongoDB

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd popquiz
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pymongo
   ```

3. Start MongoDB:
   Make sure MongoDB is running locally on `mongodb://localhost:27017/`.

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the API:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## API Endpoints
- `GET /`: Returns a welcome message.