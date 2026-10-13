# GharSure 🏠
### A PLACE FORWARD Innovation Project | Seva Innovation Challenge 2026

**Team Name:** PLACE FORWARD

GharSure is a prototype designed to help monitor living conditions in affordable housing and redevelopment communities. It focuses on a key challenge: providing housing is only the first step; residents also need reliable basic services, timely complaint resolution, and affordable access to everyday necessities.

Our goal is to make housing quality and service accountability more transparent through a simple, centralized digital platform.

## 🎯 Problem Statement

Residents in affordable housing and redeveloped communities may face issues such as:

- Irregular water supply
- Faulty lifts and infrastructure problems
- Poor waste collection and sanitation
- Delays in complaint resolution
- Limited visibility into service status
- Additional expenses and longer commutes after relocation

When these issues are tracked across disconnected channels, residents may struggle to understand the status of their complaints or assess the overall livability of their housing.

## 💡 Our Solution

GharSure brings essential housing-service monitoring and resident support features together in one platform.

### Key Features

**1. Building Basic-Service Dashboard**
- Displays the status of essential services.
- Highlights operational services and reported issues.
- Allows service statuses to be updated.

**2. Complaint Reporting**
- Allows users to submit housing-related complaints.
- Records complaint categories, descriptions, and priorities.
- Stores reports for subsequent tracking.

**3. Complaint Management**
- Displays submitted complaints.
- Supports status updates and assignment to responsible teams.
- Helps track complaints through to resolution.

**4. Housing Affordability Calculator**
- Compares housing-related expenses before and after relocation.
- Helps users understand changes in monthly expenditure.

**5. Relocation Impact Calculator**
- Compares commute time and travel costs before and after relocation.
- Helps assess how relocation may affect daily life.

## 🛠️ Technology Stack

- **Python** — application logic
- **Streamlit** — interactive web interface
- **SQLite** — local database for storing complaints and service statuses
- **Pandas** — data handling and calculations
- **Git and GitHub** — version control and project collaboration

## 🚀 Getting Started

Follow these steps to run the prototype on your computer.

### Prerequisites

- Python 3 installed
- Git installed
- Visual Studio Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/synadshah2213/Place-Forward---GharSure.git
cd Place-Forward---GharSure
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually:

`http://localhost:8501`

## 📁 Project Structure

```text
Place-Forward---GharSure/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database is generated locally when the application runs and is not intended to be committed to the repository.

## 🧪 Current Prototype Scope

The current MVP demonstrates the core workflow using sample housing-service data:

- Viewing service statuses
- Reporting and managing complaints
- Updating complaint and service statuses
- Comparing housing expenses
- Comparing relocation-related commute time and costs

**Important:** The current prototype uses sample data. It is not connected to live municipal systems, housing authorities, or real-time utility infrastructure. Service statuses and complaint resolution should be independently verified before being treated as confirmed real-world outcomes.

## 🔮 Future Scope

Potential future improvements include:

- Resident and administrator login with role-based permissions
- Photo and location-based complaint reporting
- Automated complaint categorization and prioritization
- Notifications for status changes and overdue complaints
- Analytics on complaint frequency and resolution time
- Integration with verified housing authority and public-service data
- Multilingual and mobile-friendly access
- Deployment to a cloud hosting platform for public demonstrations

## 🌍 Expected Impact

GharSure aims to support:

- Greater visibility into essential housing services
- More structured complaint tracking
- Improved accountability in maintenance workflows
- Better understanding of post-relocation affordability
- More informed decisions about housing livability

These are intended outcomes of the proposed platform; real-world impact would need to be evaluated through pilot testing with residents and relevant authorities.

## 👥 Team

**PLACE FORWARD**

Project: **GharSure — Affordable Housing Livability and Basic-Service Assurance**

Developed for the **Seva Innovation Challenge 2026**.

## 📄 License

No open-source license has been selected yet. Until a license is added, the repository should not be assumed to grant permission to reuse, modify, or redistribute the code.