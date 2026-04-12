# Assiign (Find Nearby Shops)

**Assignment As Demo Submission for "CSTE.International"**

## Problem Statement + Solution
What problem were I trying to solve?
Users in urban areas (e.g., Delhi) often face urgent needs for specific materials/items (notebooks, lab equipment, medicines, hardware, etc.) right before exams, events, or emergencies. Online orders take 2–3+ days with delivery delays and minimum-order issues. Local kirana/stationery/medical shops have the item right now, but there is no single place to instantly know:

Which nearby shops have it
Current price range
Exact distance from your current GPS location
How many options are available within walking/driving distance

Additionally, users want to contact shops directly from home to bargain without visiting each on

For example, a user like Mohit needs a USB drive, but:
He does not know which nearby shops have it
He cannot compare prices across shops
He wastes time visiting multiple stores
There is no centralized system showing distance + availability + price


Core Problems
Lack of real-time product availability
No price comparison between nearby shops
Time-consuming manual search
Inefficient decision-making
No distance-based smart filtering

# Approach
How did you break down the problem?

Data Layer → Stores (shops) + Items + Live Inventory (price + last-updated).
Location Layer → User GPS → calculate real distance to every shop.
Search & Ranking Layer → Natural-language item search + sort by (price + distance) score.
Real-time & Bargain Layer → Shop owners update prices via simple dashboard; users contact via WhatsApp in one tap.
Agentic Automation → Background autonomous workflow (Celery + scheduler) that can later scrape public sources or use ML to predict price/availability when data is stale.

# why
This is a high-frequency, high-pain real-world problem in India (especially tier-1/2 cities). It directly impacts students, small businesses, and households. Solving it supports local shops (vs. only big e-commerce), reduces traffic/carbon from unnecessary travel, and creates a hyper-local marketplace.


## Tech Stack
 Agent
- **Backend**: Python + Flask (REST API), FastAPIs, ml model, Algorithm
- **Frontend**: React.js + Tailwind CSS, 
- **Database**: SQLite, SQLAlchemy, ... 
- **Additional **: Hypersine to calculate accurate distance

## Features
This software is not just a search tool, it acts as an intelligent agent because:

 Key Features

Smart product search
Location-based shop discovery
Price comparison across shops
Fast and optimized results
Accurate distance calculation
ML-based filtering (optional enhancement)


## Architecture & Structure

User (Frontend - React)
API Request (FastAPI Backend)
Database / Shop Data
Distance Calculation (Haversine)
Filtered Results (Price + Distance + Multiples Shops Nearby)
Response to Frontend


## How to Run the Application

### 1. Backend

                            
cd Desktop/Found_your_Required_near/Backend   # Activate Virtual Environment 
source startup_idea_venv/bin/activate

pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv scipy scikit-learn celery redis
uvicorn app.main:app --reload


pip freeze > requirements.txt
pip install -r requirements.txt
python app.py

## Frontend name as 
cd frnt

npm create vite@latest smpl_p
cd smpl_p
npm install
npm install tailwindcss @tailwindcss/vite

## Setup Tailwind CSS
location vite.config.js
plugins tailwindcss()
index.css @import "tailwindcss";


npm run dev



## Future Enhancements (Optional - Advanced Features)
**Note**:
Potential future enhancements using Machine Learning and AI:
The current submission prioritizes simplicity, reliability, and timely delivery using SQLite and basic full-stack or small Agent

1- **Expense Prediction**: Forecast future monthly expenses and income trends based on historical data using time-series models.

2- **Smart Recommendations**: Provide personalized spending recommendations and budget alerts.

3- **Budget Planning Assistant**: Generate monthly budget plans and savings goals with predictive insights.

4- **Task Automation**: Set up recurring transactions and automated reminders for bills.

