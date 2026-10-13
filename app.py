
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

# ==================================================
# PLACE FORWARD | GHARSURE MVP
# ==================================================

st.set_page_config(
    page_title="GharSure | PLACE FORWARD",
    page_icon="🏠",
    layout="wide"
)

DB = "gharsure.db"

SERVICES = [
    "Water Supply",
    "Lift",
    "Drainage",
    "Sanitation",
    "Waste Collection",
    "Common-Area Electricity"
]

SERVICE_STATUSES = [
    "Operational",
    "Intermittent",
    "Reported Fault",
    "Under Repair"
]

COMPLAINT_STATUSES = [
    "Open",
    "In Progress",
    "Resolved"
]

PRIORITIES = ["Low", "Medium", "High", "Urgent"]

TEAMS = [
    "Building Maintenance",
    "Water Supply Team",
    "Lift Maintenance Team",
    "Sanitation Team",
    "Waste Management Team",
    "Electrical Maintenance Team",
    "Needs Assignment"
]


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ==================================================
# 1. DATABASE
# ==================================================

def connect():
    return sqlite3.connect(DB)


def initialise_database():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_name TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resident TEXT NOT NULL,
                service TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                assigned_team TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                resolved_at TEXT
            )
        """)

        service_count = conn.execute(
            "SELECT COUNT(*) FROM services"
        ).fetchone()[0]

        if service_count == 0:
            demo_services = [
                ("Water Supply", "Intermittent"),
                ("Lift", "Reported Fault"),
                ("Drainage", "Operational"),
                ("Sanitation", "Operational"),
                ("Waste Collection", "Under Repair"),
                ("Common-Area Electricity", "Operational")
            ]

            conn.executemany(
                """
                INSERT INTO services
                (service_name, status, updated_at)
                VALUES (?, ?, ?)
                """,
                [(name, status, now())
                 for name, status in demo_services]
            )

        complaint_count = conn.execute(
            "SELECT COUNT(*) FROM complaints"
        ).fetchone()[0]

        if complaint_count == 0:
            demo_complaints = [
                (
                    "Demo Resident A",
                    "Water Supply",
                    "Water supply has been irregular.",
                    "High",
                    "Water Supply Team",
                    "Open",
                    now(),
                    None
                ),
                (
                    "Demo Resident B",
                    "Lift",
                    "The lift has been reported as faulty.",
                    "Urgent",
                    "Lift Maintenance Team",
                    "In Progress",
                    now(),
                    None
                )
            ]

            conn.executemany(
                """
                INSERT INTO complaints (
                    resident, service, description, priority,
                    assigned_team, status, created_at, resolved_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                demo_complaints
            )


initialise_database()


def get_services():
    with connect() as conn:
        return pd.read_sql_query(
            "SELECT * FROM services ORDER BY service_name",
            conn
        )


def get_complaints():
    with connect() as conn:
        return pd.read_sql_query(
            "SELECT * FROM complaints ORDER BY id DESC",
            conn
        )


# ==================================================
# 2. HEADER AND NAVIGATION
# ==================================================

st.title("🏠 GharSure")
st.subheader("A PLACE FORWARD Innovation Project")

st.write(
    "Post-Occupancy Livability and Basic-Service Assurance"
)

st.caption(
    "Affordable Housing • Slum Redevelopment • Basic Services"
)

st.warning(
    "DEMO DATA: This student prototype uses simulated building "
    "information. It is not connected to live government systems."
)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Building Dashboard",
        "Report a Complaint",
        "Manage Complaints",
        "Housing Affordability",
        "Relocation Impact"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### PLACE FORWARD")
st.sidebar.caption("GharSure | Student MVP")
st.sidebar.caption("Demo location: Mumbai, Maharashtra")


# ==================================================
# 3. BUILDING DASHBOARD
# ==================================================

if page == "Building Dashboard":

    st.header("Building Livability Dashboard")

    services = get_services()
    complaints = get_complaints()

    open_count = int(
        (complaints["status"] != "Resolved").sum()
    )

    operational = int(
        (services["status"] == "Operational").sum()
    )

    attention = int(
        (services["status"] != "Operational").sum()
    )

    a, b, c, d = st.columns(4)

    a.metric("Services Tracked", len(services))
    b.metric("Operational", operational)
    c.metric("Need Attention", attention)
    d.metric("Unresolved Complaints", open_count)

    st.divider()
    st.subheader("Essential-Service Status")

    for _, item in services.iterrows():

        status = item["status"]

        if status == "Operational":
            symbol = "🟢"
        elif status == "Intermittent":
            symbol = "🟡"
        else:
            symbol = "🔴"

        st.write(
            f"{symbol} **{item['service_name']}** — {status}"
        )

    st.caption(
        "These are recorded statuses, not sensor-verified service uptime."
    )

    st.divider()
    st.subheader("Update Service Status")

    with st.form("service_form"):

        chosen_service = st.selectbox(
            "Select service",
            SERVICES
        )

        service_df = services[
            services["service_name"] == chosen_service
        ]

        old_status = service_df.iloc[0]["status"]

        chosen_status = st.selectbox(
            "New recorded status",
            SERVICE_STATUSES,
            index=SERVICE_STATUSES.index(old_status)
        )

        save_service = st.form_submit_button(
            "Save Service Update"
        )

    if save_service:

        with connect() as conn:
            conn.execute(
                """
                UPDATE services
                SET status = ?, updated_at = ?
                WHERE service_name = ?
                """,
                (chosen_status, now(), chosen_service)
            )

        st.success("Service status saved.")
        st.rerun()

    st.divider()
    st.subheader("Recent Complaints")

    if complaints.empty:
        st.info("No complaints have been recorded.")
    else:
        st.dataframe(
            complaints[
                ["id", "service", "priority", "status", "assigned_team"]
            ].head(10),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# 4. REPORT A COMPLAINT
# ==================================================

elif page == "Report a Complaint":

    st.header("Report an Essential-Service Problem")

    st.write(
        "Report an issue affecting your building's basic services."
    )

    with st.form("new_complaint_form"):

        resident = st.text_input(
            "Resident name or demo identifier",
            placeholder="e.g. Resident C"
        )

        service = st.selectbox(
            "Affected service",
            SERVICES
        )

        description = st.text_area(
            "Describe the issue",
            placeholder="What happened, where and when?"
        )

        priority = st.selectbox(
            "Priority",
            PRIORITIES
        )

        assigned_team = st.selectbox(
            "Responsible team",
            TEAMS
        )

        submit = st.form_submit_button("Submit Complaint")

    if submit:

        if not resident.strip() or not description.strip():

            st.error(
                "Enter a resident identifier and describe the issue."
            )

        else:

            with connect() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO complaints (
                        resident, service, description, priority,
                        assigned_team, status, created_at, resolved_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        resident.strip(),
                        service,
                        description.strip(),
                        priority,
                        assigned_team,
                        "Open",
                        now(),
                        None
                    )
                )

                complaint_id = cursor.lastrowid

                # A report flags a service for attention.
                # It does not independently verify the fault.
                conn.execute(
                    """
                    UPDATE services
                    SET status = 'Reported Fault', updated_at = ?
                    WHERE service_name = ?
                    """,
                    (now(), service)
                )

            st.success(
                f"Complaint recorded! Reference: GS-{complaint_id:04d}"
            )

            st.info(
                "This reference works inside the demo application. "
                "The complaint has not been sent to a real authority."
            )


# ==================================================
# 5. MANAGE AND RESOLVE COMPLAINTS
# ==================================================

elif page == "Manage Complaints":

    st.header("Complaint Tracking and Resolution")

    complaints = get_complaints()

    if complaints.empty:

        st.info("There are no complaints to display.")

    else:

        st.dataframe(
            complaints[
                [
                    "id", "service", "description", "priority",
                    "assigned_team", "status", "created_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("Update a Complaint")

        selected_id = st.selectbox(
            "Complaint reference",
            complaints["id"].tolist(),
            format_func=lambda number: f"GS-{number:04d}"
        )

        selected = complaints[
            complaints["id"] == selected_id
        ].iloc[0]

        st.write(f"**Issue:** {selected['description']}")
        st.write(f"**Service:** {selected['service']}")
        st.write(f"**Priority:** {selected['priority']}")

        with st.form("update_complaint_form"):

            new_status = st.selectbox(
                "Complaint status",
                COMPLAINT_STATUSES,
                index=COMPLAINT_STATUSES.index(selected["status"])
            )

            new_team = st.selectbox(
                "Assigned team",
                TEAMS,
                index=TEAMS.index(selected["assigned_team"])
            )

            save_complaint = st.form_submit_button(
                "Save Complaint Update"
            )

        if save_complaint:

            resolved_at = (
                now() if new_status == "Resolved" else None
            )

            with connect() as conn:
                conn.execute(
                    """
                    UPDATE complaints
                    SET status = ?, assigned_team = ?, resolved_at = ?
                    WHERE id = ?
                    """,
                    (new_status, new_team, resolved_at, selected_id)
                )

            st.success(
                "Complaint updated. Service status remains separate "
                "until it is checked and manually updated."
            )
            st.rerun()


# ==================================================
# 6. HOUSING AFFORDABILITY CALCULATOR
# ==================================================

elif page == "Housing Affordability":

    st.header("Housing Affordability Stress Test")

    st.write(
        "Compare estimated monthly expenses before and after relocation."
    )

    st.caption(
        "Enter example values or use anonymised household estimates."
    )

    st.subheader("Before Relocation")

    left, right = st.columns(2)

    with left:
        old_housing = st.number_input(
            "Rent or housing payment (₹/month)",
            min_value=0, value=2000, step=500,
            key="old_housing"
        )

        old_utilities = st.number_input(
            "Utilities (₹/month)",
            min_value=0, value=800, step=100,
            key="old_utilities"
        )

    with right:
        old_maintenance = st.number_input(
            "Maintenance (₹/month)",
            min_value=0, value=200, step=100,
            key="old_maintenance"
        )

        old_transport = st.number_input(
            "Commuting (₹/month)",
            min_value=0, value=1000, step=100,
            key="old_transport"
        )

    st.subheader("After Relocation")

    left, right = st.columns(2)

    with left:
        new_housing = st.number_input(
            "Rent, EMI or housing payment (₹/month)",
            min_value=0, value=0, step=500,
            key="new_housing"
        )

        new_utilities = st.number_input(
            "Utilities (₹/month)",
            min_value=0, value=1500, step=100,
            key="new_utilities"
        )

    with right:
        new_maintenance = st.number_input(
            "Maintenance (₹/month)",
            min_value=0, value=1500, step=100,
            key="new_maintenance"
        )

        new_transport = st.number_input(
            "Commuting (₹/month)",
            min_value=0, value=2500, step=100,
            key="new_transport"
        )

    old_total = (
        old_housing + old_utilities
        + old_maintenance + old_transport
    )

    new_total = (
        new_housing + new_utilities
        + new_maintenance + new_transport
    )

    difference = new_total - old_total

    st.divider()
    st.subheader("Cost Comparison")

    c1, c2, c3 = st.columns(3)

    c1.metric("Before", f"₹{old_total:,.0f}/month")
    c2.metric("After", f"₹{new_total:,.0f}/month")
    c3.metric(
        "Monthly Difference",
        f"₹{difference:+,.0f}",
        delta_color="inverse"
    )

    if old_total > 0:
        percent = difference / old_total * 100
        st.write(f"Estimated monthly cost change: {percent:+.1f}%")

    if difference > 0:
        st.warning(
            "The entered expenses increase after relocation."
        )
    elif difference < 0:
        st.success(
            "The entered expenses decrease after relocation."
        )
    else:
        st.info(
            "The entered expenses are unchanged."
        )

    st.caption(
        "This calculation covers only the expenses entered. "
        "It excludes income, food, healthcare and other costs, "
        "so it is not a complete household affordability assessment."
    )


# ==================================================
# 7. RELOCATION IMPACT CHECKER
# ==================================================

elif page == "Relocation Impact":

    st.header("Relocation Impact Checker")

    st.write(
        "Compare the cost and time required to reach a workplace "
        "or another essential destination."
    )

    st.caption(
        "All journey times and fares are manually entered estimates, "
        "not live mapping data."
    )

    left, right = st.columns(2)

    with left:

        st.subheader("Before Relocation")

        old_destination = st.text_input(
            "Destination",
            value="Workplace",
            key="old_destination"
        )

        old_minutes = st.number_input(
            "One-way journey (minutes)",
            min_value=0, value=30, step=5,
            key="old_minutes"
        )

        old_fare = st.number_input(
            "One-way travel cost (₹)",
            min_value=0, value=20, step=5,
            key="old_fare"
        )

    with right:

        st.subheader("After Relocation")

        new_destination = st.text_input(
            "Destination",
            value="Workplace",
            key="new_destination"
        )

        new_minutes = st.number_input(
            "One-way journey (minutes)",
            min_value=0, value=55, step=5,
            key="new_minutes"
        )

        new_fare = st.number_input(
            "One-way travel cost (₹)",
            min_value=0, value=45, step=5,
            key="new_fare"
        )

    journeys = st.number_input(
        "Return journeys per month",
        min_value=0, value=26, step=1
    )

    old_monthly_cost = old_fare * 2 * journeys
    new_monthly_cost = new_fare * 2 * journeys

    old_monthly_time = old_minutes * 2 * journeys
    new_monthly_time = new_minutes * 2 * journeys

    st.divider()
    st.subheader("Comparison Results")

    a, b = st.columns(2)

    a.metric(
        "Monthly travel cost before",
        f"₹{old_monthly_cost:,.0f}"
    )

    b.metric(
        "Monthly travel cost after",
        f"₹{new_monthly_cost:,.0f}",
        delta=f"₹{new_monthly_cost - old_monthly_cost:+,.0f}",
        delta_color="inverse"
    )

    a, b = st.columns(2)

    a.metric(
        "Travel time before",
        f"{old_monthly_time / 60:.1f} hours/month"
    )

    b.metric(
        "Travel time after",
        f"{new_monthly_time / 60:.1f} hours/month",
        delta=(
            f"{(new_monthly_time - old_monthly_time) / 60:+.1f} hours"
        ),
        delta_color="inverse"
    )

    comparison = pd.DataFrame({
        "Measure": [
            "Destination",
            "One-way travel time (minutes)",
            "One-way fare (₹)",
            "Monthly travel cost (₹)",
            "Monthly travel time (hours)"
        ],
        "Before": [
            old_destination,
            old_minutes,
            old_fare,
            old_monthly_cost,
            round(old_monthly_time / 60, 1)
        ],
        "After": [
            new_destination,
            new_minutes,
            new_fare,
            new_monthly_cost,
            round(new_monthly_time / 60, 1)
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Repeat this assessment for schools, healthcare facilities "
        "and markets to develop a broader relocation comparison."
    )


# ==================================================
# 8. FOOTER
# ==================================================

st.divider()

st.caption(
    "PLACE FORWARD | GharSure | Seva Innovation Challenge 2026"
)

st.caption(
    "Student prototype • Simulated data • "
    "No live government integration"
)
