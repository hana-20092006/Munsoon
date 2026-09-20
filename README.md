# MUNSOON

### AI-Powered Energy Resilience for Monsoon-Prone Solar Homes

MUNSOON is an AI-powered prototype that helps rooftop-solar households prepare for energy shortages during prolonged monsoon weather and grid disruptions.

It combines solar-generation estimation, household energy simulation, agentic reasoning, and RAG-based guidance to answer one simple question:

> **"Will my house make it through tonight?"**

Built as part of the **1M1B AI for Sustainability Virtual Internship**.

<!-- Add a dashboard screenshot or demo GIF here, e.g. ![MUNSOON Dashboard](docs/dashboard.png) -->

---

## 🌧️ Problem

In monsoon-prone regions such as Kerala, heavy cloud cover and rainfall can sharply reduce solar generation, while severe weather also raises the chance of grid outages.

Without proactive energy management, households can drain their battery before grid power returns. MUNSOON turns this uncertainty into a clear, actionable energy plan.

---

## 💡 Solution

MUNSOON classifies a household's energy-shortage risk as **LOW**, **MEDIUM**, or **HIGH**, then recommends actions such as:

- Prioritizing essential loads
- Preserving battery reserve
- Shifting flexible usage to periods of higher solar generation
- Charging the battery before an expected low-generation period, when possible

### Workflow

```text
Weather & Solar Data
        ↓
Solar Generation Estimation
        ↓
Household Energy Simulation
        ↓
Energy Risk Assessment
        ↓
Agentic Reasoning + RAG
        ↓
Actionable Recommendations
        ↓
Energy Resilience Dashboard
```

---

## 🤖 AI Components

| Component | Description |
|---|---|
| **Solar Generation Model** | A Random Forest regression model estimates solar power output from solar and weather features. |
| **Agentic AI Workflow** | The MUNSOON agent interprets the risk assessment, decides on a response, retrieves relevant knowledge, and produces actionable recommendations. |
| **RAG** | A lightweight knowledge base covering battery reserve management, load shifting, energy-risk interpretation, and responsible AI considerations. |
| **Energy Simulation** | An energy engine that models solar generation, household demand, battery state of charge, grid availability, energy shortage, and energy coverage. |

---

## 📊 Prototype Results

A controlled monsoon scenario was used to compare a reactive strategy against the MUNSOON strategy.

| Metric | Reactive | MUNSOON | Change |
|---|---|---|---|
| Energy shortage | 6.59 kWh | 4.59 kWh | **2.0 kWh reduction** |
| Energy coverage | 40.09% | 58.27% | **+18.18 percentage points** |

> **Note:** These are controlled prototype simulation results, not field validation results.

---

## 🌱 SDG Alignment

**SDG 7: Affordable and Clean Energy.** MUNSOON supports energy resilience by helping solar-powered households make better-informed decisions about limited energy during adverse weather.

---

## 🛡️ Responsible AI

- **Transparency:** energy inputs, risk levels, and recommendations are all visible to the user.
- **Privacy:** no sensitive personal household information is required.
- **Safety:** provides energy-management guidance only, with no electrical installation instructions.
- **Human control:** recommendations support household decisions rather than replace them.
- **Limitations:** predictions and simulations are clearly communicated as estimates.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite, Tailwind CSS, Recharts |
| **Backend** | Python, FastAPI, Pandas, NumPy, Scikit-learn |
| **AI** | Random Forest, agentic workflow, RAG, prompt-based reasoning |
| **Data** | Open-Meteo weather data, public solar-generation data, prototype household energy profiles |

---

## 📁 Project Structure

```text
Munsoon/
├── backend/
│   ├── agent/        # Agentic reasoning workflow
│   ├── app/          # FastAPI application
│   ├── data/         # Datasets and household profiles
│   ├── ml/           # Solar generation model
│   ├── rag/          # Knowledge base and retrieval
│   └── services/     # Energy simulation and risk logic
│
├── frontend/
│   └── src/          # React dashboard
│
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher

### 1. Backend

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. FastAPI's interactive docs are available at `http://127.0.0.1:8000/docs`.

### 2. Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at `http://localhost:5173`.

---

## ⚠️ Current Limitations

- The solar model is a prototype and has not been validated on Kerala rooftop-solar data.
- The public PV dataset used represents a larger solar plant, not a household rooftop system.
- Household demand profiles are simplified.
- Comparisons are simulations, not real-world field trials.

---

## 🔮 Future Work

- Kerala-specific rooftop solar datasets
- More accurate day-ahead solar forecasting
- Real-time weather integration
- Personalized household demand prediction
- Battery-aware optimization
- Mobile alerts for upcoming energy risks
- Integration with smart meters and home energy-management systems

---

## 🎯 Impact

MUNSOON turns weather uncertainty into proactive household energy decisions, helping solar homes prepare before the power goes out.