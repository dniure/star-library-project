# STAR Library

This is a **mini full-stack library system** built with **FastAPI (backend)** and **React (frontend)**.  
The goal is to demonstrate the ability to design and build a complete system with:

- A backend (FastAPI + SQLite database)
- A frontend (React + TailwindCSS)
- Integration of frontend with backend
---

## 📂 Project Structure

```plaintext
star-library-project/
│── backend/
│   ├── app/
│   │   ├── api/          # API routes (to be implemented)
│   │   ├── crud/         # Database CRUD operations
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── main.py       # FastAPI entrypoint
│   │   └── db.py         # Database connection setup
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Backend dependencies
│
│── frontend/
│   ├── public/           # Static assets
│   └── src/
│       ├── components/   # UI components
│       ├── context/      # React context
│       ├── hooks/        # Custom hooks
│       ├── pages/        # Page components
│       ├── services/     # API integration (axios)
│       ├── styles/       # Styling
│       └── utils/        # Utility functions
│
└── README.md

```

## 🚀 How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/star-library-project.git
cd star-library-project
```

## ⚡ Backend Setup (FastAPI + SQLite)

1.  **Navigate to backend folder**
    ```bash
    cd backend
    ```

2.  **Create virtual environment**
    ```bash
    python -m venv venv
    ```
    **Activate it:**
    * **Mac/Linux**
        ```bash
        source venv/bin/activate
        ```
    * **Windows**
        ```bash
        venv\Scripts\activate
        ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the Server**
    ```bash
    uvicorn app.main:app --reload
    ```
    Backend will be available at:
    👉 **http://127.0.0.1:8000**
    
    Interactive API docs (Swagger UI):
    👉 **http://127.0.0.1:8000/docs**

---

## 🎨 Frontend Setup (React + Tailwind)

1.  **Navigate to frontend folder**
    ```bash
    cd frontend
    ```

2.  **Install dependencies**
    ```bash
    npm install
    ```
3.  **Run frontend**
    ```bash
    npm start
    ```
    Frontend will be available at:
    👉 **http://localhost:3000**

---

## 🚀 Running the Project
To run the full-stack application, open two separate terminals.

In Terminal 1, start the backend:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

In Terminal 2, start the frontend:

```bash
cd frontend
npm start
```
Now, open your web browser and navigate to 👉 http://localhost:3000 to view the frontend, which will be fetching data from the backend running at 👉 http://127.0.0.1:8000.