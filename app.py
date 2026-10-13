import html
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

PILL_CLASS = {
    # service statuses
    "Operational": "green",
    "Intermittent": "amber",
    "Reported Fault": "red",
    "Under Repair": "blue",
    # complaint statuses
    "Open": "blue",
    "In Progress": "amber",
    "Resolved": "green",
    # priorities
    "Low": "grey",
    "Medium": "blue",
    "High": "amber",
    "Urgent": "red",
}


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ==================================================
# 1. DATABASE  (unchanged)
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
# 2. STYLING
# ==================================================

NAVY = "#14213D"
BLUE = "#1A3FA0"
GREEN = "#2E9E5B"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.stApp { background: #F4F6FA; }

/* hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1200px; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] { background: #16347F; }
[data-testid="stSidebar"] * { color: #E8EEFF; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.18); }
.brand { display:flex; align-items:center; gap:10px; margin: 4px 0 18px 0; }
.brand-mark {
    width:38px; height:38px; border-radius:10px; background:#fff;
    display:flex; align-items:center; justify-content:center; font-size:20px;
}
.brand-name { font-size:1.35rem; font-weight:700; color:#fff !important; line-height:1.1; }
.brand-sub { font-size:0.7rem; letter-spacing:.08em; text-transform:uppercase; color:#AFC0F5 !important; }

[data-testid="stSidebar"] div[role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 14px; border-radius: 10px; width: 100%; cursor: pointer;
}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(255,255,255,0.10); }
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #FFFFFF;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) * {
    color: #16347F !important; font-weight: 600;
}

/* ---------- page header ---------- */
.page-head { margin-bottom: 18px; }
.page-title { font-size: 1.6rem; font-weight: 700; color: #14213D; margin: 0; }
.page-sub { color: #5B6785; font-size: 0.95rem; margin-top: 2px; }

.notice {
    background: #FFF8E6; border: 1px solid #F3DFA2; color: #7A5B00;
    padding: 9px 14px; border-radius: 10px; font-size: 0.82rem; margin-bottom: 18px;
}

/* ---------- cards ---------- */
.card {
    background: #fff; border: 1px solid #E3E8F2; border-radius: 14px;
    padding: 18px 20px; box-shadow: 0 1px 2px rgba(20,33,61,0.04);
    margin-bottom: 16px;
}
.card-title { font-size: 1.02rem; font-weight: 600; color: #14213D; margin-bottom: 12px; }
.kpi { border-top: 4px solid #1A3FA0; }
.kpi-label { color: #5B6785; font-size: 0.82rem; font-weight: 500; }
.kpi-value { color: #14213D; font-size: 2rem; font-weight: 700; line-height: 1.2; margin-top: 4px; }
.kpi-sub { color: #8390AB; font-size: 0.76rem; margin-top: 2px; }

/* ---------- pills ---------- */
.pill {
    display: inline-block; padding: 3px 11px; border-radius: 999px;
    font-size: 0.74rem; font-weight: 600; border: 1px solid transparent; white-space: nowrap;
}
.pill.green { background:#E6F6EC; color:#1E7A43; border-color:#BFE6CF; }
.pill.amber { background:#FFF4DE; color:#9A6A00; border-color:#F5DDA3; }
.pill.red   { background:#FDE9E9; color:#B42323; border-color:#F5BDBD; }
.pill.blue  { background:#E8EFFE; color:#1A3FA0; border-color:#C3D3F8; }
.pill.grey  { background:#EEF1F6; color:#5B6785; border-color:#DCE2EC; }

/* ---------- tables ---------- */
.tbl-wrap { overflow-x: auto; }
table.gs { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
table.gs th {
    text-align: left; color: #5B6785; font-weight: 600; font-size: 0.78rem;
    padding: 10px 10px; border-bottom: 1px solid #E3E8F2; white-space: nowrap;
}
table.gs td { padding: 12px 10px; border-bottom: 1px solid #EEF1F6; color: #14213D; vertical-align: middle; }
table.gs tr:last-child td { border-bottom: none; }
table.gs td.num, table.gs th.num { text-align: right; }
table.gs tr.total td { font-weight: 700; background: #F8FAFD; }
.up { color: #B42323; font-weight: 600; }
.down { color: #1E7A43; font-weight: 600; }

/* ---------- bars ---------- */
.bar-row { margin-bottom: 12px; }
.bar-top { display:flex; justify-content:space-between; font-size:0.85rem; color:#14213D; margin-bottom:4px; }
.bar-track { background:#EEF1F6; border-radius:999px; height:8px; }
.bar-fill { height:8px; border-radius:999px; background:#1A3FA0; }

/* ---------- callouts ---------- */
.callout { border-radius: 10px; padding: 11px 14px; font-size: 0.88rem; margin: 6px 0 14px 0; border: 1px solid; }
.callout.info { background:#E8EFFE; border-color:#C3D3F8; color:#1A3FA0; }
.callout.warn { background:#FFF4DE; border-color:#F5DDA3; color:#8A5E00; }
.callout.ok   { background:#E6F6EC; border-color:#BFE6CF; color:#1E7A43; }
.callout.bad  { background:#FDE9E9; border-color:#F5BDBD; color:#B42323; }

/* ---------- streamlit forms & inputs ---------- */
[data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"] .section-marker) {
    background: #fff; border: 1px solid #E3E8F2; border-radius: 14px; padding: 18px 20px;
}
div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] {
    border-radius: 8px !important;
}
.stButton > button, [data-testid="stFormSubmitButton"] > button {
    background: #1A3FA0; color: #fff; border: none; border-radius: 8px;
    padding: 0.5rem 1.2rem; font-weight: 600;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: #14307F; color: #fff;
}
.section-label { font-size: 1.02rem; font-weight: 600; color: #14213D; margin: 4px 0 8px 0; }
.foot { color: #8390AB; font-size: 0.76rem; text-align: center; margin-top: 28px; line-height: 1.6; }

/* ---------- hero banner ---------- */
.hero {
    position: relative; overflow: hidden; border-radius: 18px;
    background: linear-gradient(100deg, #FFFFFF 0%, #F1F5FD 45%, #DCE7FA 100%);
    border: 1px solid #E3E8F2; margin-bottom: 16px; min-height: 230px;
}
.hero-text { position: relative; z-index: 2; padding: 28px 32px; max-width: 56%; }
.hero-title { font-size: 2rem; font-weight: 800; line-height: 1.15; color: #14213D; }
.hero-sub { font-size: 1.02rem; color: #5B6785; margin-top: 8px; }
.hero-art { position: absolute; right: 0; bottom: 0; width: 62%; height: 100%; z-index: 1; }
.hero-art svg { width: 100%; height: 100%; display: block; }
.hero-photo {
    position: absolute; right: 0; top: 0; bottom: 0; width: 60%; z-index: 1;
    background-size: cover; background-position: center;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, #000 38%);
    mask-image: linear-gradient(to right, transparent 0%, #000 38%);
}
.feat-row { display: flex; gap: 22px; margin-top: 18px; }
.feat { text-align: center; font-size: 0.74rem; color: #14213D; width: 110px; line-height: 1.3; }
.feat-ic {
    width: 46px; height: 46px; border-radius: 50%; margin: 0 auto 6px auto;
    border: 2px solid #1A3FA0; background: #fff; display:flex; align-items:center;
    justify-content:center; font-size: 20px;
}
@media (max-width: 800px) {
    .hero-text { max-width: 100%; }
    .hero-photo { width: 100%; opacity: .25; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ---------- small HTML helpers ----------

def esc(value):
    return html.escape(str(value))


def pill(label):
    return f'<span class="pill {PILL_CLASS.get(label, "grey")}">{esc(label)}</span>'


def kpi(label, value, sub="", color=BLUE):
    return (
        f'<div class="card kpi" style="border-top-color:{color}">'
        f'<div class="kpi-label">{esc(label)}</div>'
        f'<div class="kpi-value">{esc(value)}</div>'
        f'<div class="kpi-sub">{esc(sub)}</div></div>'
    )


def callout(kind, text):
    st.markdown(
        f'<div class="callout {kind}">{esc(text)}</div>',
        unsafe_allow_html=True
    )


PAGE_IMAGES = {
    "Building Dashboard": "dashboard",
    "Report a Complaint": "report",
    "Manage Complaints": "complaints",
    "Housing Affordability": "affordability",
    "Relocation Impact": "relocation",
}


@st.cache_data(show_spinner=False)
def load_photo(key):
    """Looks (case-insensitively) in assets/ and the app folder for <key>.jpg/jpeg/png/webp, then hero.*.
    Returns a base64 JPEG string (resized so the page stays light), or None."""
    import base64, io, os
    from PIL import Image

    exts = {".jpg", ".jpeg", ".png", ".webp"}
    for name in (key, "hero"):
        for folder in ("assets", "."):
            if not os.path.isdir(folder):
                continue
            for fname in sorted(os.listdir(folder)):
                stem, ext = os.path.splitext(fname)
                if stem.lower() == name and ext.lower() in exts:
                    img = Image.open(os.path.join(folder, fname)).convert("RGB")
                    img.thumbnail((1400, 1400))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=82)
                    return base64.b64encode(buf.getvalue()).decode()
    return None


def hero(title, subtitle, features=None):
    b64 = load_photo(PAGE_IMAGES.get(page, "hero"))
    photo = ""
    if b64:
        photo = (f'<div class="hero-photo" '
                 f'style="background-image:url(data:image/jpeg;base64,{b64})"></div>')
    feats = ""
    if features:
        feats = '<div class="feat-row">' + "".join(
            f'<div class="feat"><div class="feat-ic">{icon}</div>{esc(text)}</div>'
            for icon, text in features
        ) + "</div>"
    st.markdown(
        f'<div class="hero">{photo}'
        f'<div class="hero-text"><div class="hero-title">{esc(title)}</div>'
        f'<div class="hero-sub">{esc(subtitle)}</div>{feats}</div></div>'
        '<div class="notice"><b>Demo data.</b> This student prototype uses '
        'simulated building information and is not connected to live '
        'government systems.</div>',
        unsafe_allow_html=True
    )


def page_header(title, subtitle, features=None):
    hero(title, subtitle, features)


def table(headers, rows, num_cols=(), total_last=False):
    """headers: list of str. rows: list of lists of ready-made HTML strings."""
    head = "".join(
        f'<th class="{"num" if i in num_cols else ""}">{esc(h)}</th>'
        for i, h in enumerate(headers)
    )
    body = ""
    for r_i, row in enumerate(rows):
        cls = "total" if total_last and r_i == len(rows) - 1 else ""
        cells = "".join(
            f'<td class="{"num" if i in num_cols else ""}">{cell}</td>'
            for i, cell in enumerate(row)
        )
        body += f'<tr class="{cls}">{cells}</tr>'
    st.markdown(
        f'<div class="card"><div class="tbl-wrap"><table class="gs">'
        f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div></div>',
        unsafe_allow_html=True
    )


def complaint_rows(df, with_description=False):
    rows = []
    for _, c in df.iterrows():
        row = [
            f'<b>GS-{int(c["id"]):04d}</b>',
            esc(c["service"]),
        ]
        if with_description:
            row.append(esc(c["description"]))
        row += [
            pill(c["priority"]),
            esc(c["assigned_team"]),
            pill(c["status"]),
            esc(c["created_at"]),
        ]
        rows.append(row)
    return rows


def money(x):
    return f"₹{x:,.0f}"


def change_html(diff, suffix=""):
    if diff > 0:
        return f'<span class="up">▲ +{diff:,.0f}{suffix}</span>'
    if diff < 0:
        return f'<span class="down">▼ {diff:,.0f}{suffix}</span>'
    return "—"


# ==================================================
# 3. SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">🏠</div>'
        '<div><div class="brand-name">GharSure</div>'
        '<div class="brand-sub">PLACE FORWARD</div></div></div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Building Dashboard",
            "Report a Complaint",
            "Manage Complaints",
            "Housing Affordability",
            "Relocation Impact"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("Post-Occupancy Livability and Basic-Service Assurance")
    st.caption("Demo location: Mumbai, Maharashtra")
    st.caption("Student MVP • Seva Innovation Challenge 2026")


# ==================================================
# 4. BUILDING DASHBOARD
# ==================================================

if page == "Building Dashboard":

    page_header(
        "Is your building working for you?",
        "Check essential services. Report problems. Track every fix.",
        [("🏢", "Essential services tracked"),
         ("🛠️", "Complaints followed to resolution"),
         ("🔑", "Safer homes. Stronger communities.")]
    )

    services = get_services()
    complaints = get_complaints()

    open_count = int((complaints["status"] != "Resolved").sum())
    operational = int((services["status"] == "Operational").sum())
    attention = int((services["status"] != "Operational").sum())
    total_services = max(len(services), 1)
    level = operational / total_services * 100

    # ---- KPI row + service-level ring ----
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Services Tracked", len(services), "Essential services"), unsafe_allow_html=True)
    k2.markdown(kpi("Need Attention", attention, "Not fully operational", "#D9822B"), unsafe_allow_html=True)
    k3.markdown(kpi("Unresolved Complaints", open_count, "Open + in progress", "#C0392B"), unsafe_allow_html=True)

    circ = 2 * 3.14159 * 46
    dash = circ * level / 100
    k4.markdown(
        f'<div class="card kpi" style="border-top-color:{GREEN}; text-align:center">'
        f'<div class="kpi-label">Service Level</div>'
        f'<svg width="96" height="96" viewBox="0 0 120 120">'
        f'<circle cx="60" cy="60" r="46" fill="none" stroke="#E6EBF3" stroke-width="10"/>'
        f'<circle cx="60" cy="60" r="46" fill="none" stroke="{GREEN}" stroke-width="10" '
        f'stroke-linecap="round" stroke-dasharray="{dash:.1f} {circ:.1f}" '
        f'transform="rotate(-90 60 60)"/>'
        f'<text x="60" y="66" text-anchor="middle" font-size="22" font-weight="700" '
        f'fill="{NAVY}">{level:.0f}%</text></svg>'
        f'<div class="kpi-sub">{operational} of {len(services)} operational</div></div>',
        unsafe_allow_html=True
    )

    # ---- service status table + category bars ----
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="section-label">Essential-Service Status</div>', unsafe_allow_html=True)
        table(
            ["Service", "Status", "Last updated"],
            [
                [f"<b>{esc(s['service_name'])}</b>", pill(s["status"]), esc(s["updated_at"])]
                for _, s in services.iterrows()
            ]
        )
        st.caption("These are recorded statuses, not sensor-verified service uptime.")

    with right:
        st.markdown('<div class="section-label">Unresolved Complaints by Service</div>', unsafe_allow_html=True)
        unresolved = complaints[complaints["status"] != "Resolved"]
        counts = unresolved["service"].value_counts()
        if counts.empty:
            bars = '<div class="kpi-sub">No unresolved complaints.</div>'
        else:
            top = counts.max()
            bars = "".join(
                f'<div class="bar-row"><div class="bar-top"><span>{esc(name)}</span>'
                f'<span><b>{n}</b></span></div><div class="bar-track">'
                f'<div class="bar-fill" style="width:{n / top * 100:.0f}%"></div></div></div>'
                for name, n in counts.items()
            )
        st.markdown(f'<div class="card">{bars}</div>', unsafe_allow_html=True)

    # ---- update service status ----
    st.markdown('<div class="section-label">Update Service Status</div>', unsafe_allow_html=True)

    with st.form("service_form"):
        f1, f2 = st.columns(2)

        chosen_service = f1.selectbox("Select service", SERVICES)

        service_df = services[services["service_name"] == chosen_service]
        old_status = service_df.iloc[0]["status"]

        chosen_status = f2.selectbox(
            "New recorded status",
            SERVICE_STATUSES,
            index=SERVICE_STATUSES.index(old_status)
        )

        save_service = st.form_submit_button("Save Service Update")

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

    # ---- recent complaints ----
    st.markdown('<div class="section-label">Recent Complaints</div>', unsafe_allow_html=True)

    if complaints.empty:
        callout("info", "No complaints have been recorded.")
    else:
        table(
            ["Ref", "Service", "Priority", "Team", "Status", "Reported"],
            complaint_rows(complaints.head(8))
        )


# ==================================================
# 5. REPORT A COMPLAINT
# ==================================================

elif page == "Report a Complaint":

    page_header(
        "Report a problem in your building",
        "Water, lift, drainage or power. Tell us what is not working.",
        [("💧", "Water & drainage"), ("🛗", "Lifts & power"), ("🧹", "Sanitation & waste")]
    )

    with st.form("new_complaint_form"):

        resident = st.text_input(
            "Resident name or demo identifier",
            placeholder="e.g. Resident C"
        )

        a, b = st.columns(2)

        service = a.selectbox("Affected service", SERVICES)
        priority = b.selectbox("Priority", PRIORITIES)

        assigned_team = st.selectbox("Responsible team", TEAMS)

        description = st.text_area(
            "Describe the issue",
            placeholder="What happened, where and when?"
        )

        submit = st.form_submit_button("Submit Complaint")

    if submit:

        if not resident.strip() or not description.strip():

            st.error("Enter a resident identifier and describe the issue.")

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

            st.success(f"Complaint recorded! Reference: GS-{complaint_id:04d}")

            callout(
                "info",
                "This reference works inside the demo application. "
                "The complaint has not been sent to a real authority."
            )


# ==================================================
# 6. MANAGE COMPLAINTS
# ==================================================

elif page == "Manage Complaints":

    page_header(
        "Track every complaint",
        "Search, filter and resolve resident complaints in one place."
    )

    complaints = get_complaints()

    if complaints.empty:

        callout("info", "There are no complaints to display.")

    else:

        s1, s2, s3 = st.columns([2, 1, 1])

        query = s1.text_input(
            "Search",
            placeholder="Search by reference, service or description"
        )
        status_filter = s2.selectbox("Status", ["All"] + COMPLAINT_STATUSES)
        priority_filter = s3.selectbox("Priority", ["All"] + PRIORITIES)

        view = complaints.copy()

        if status_filter != "All":
            view = view[view["status"] == status_filter]

        if priority_filter != "All":
            view = view[view["priority"] == priority_filter]

        if query.strip():
            q = query.strip().lower()
            ref = view["id"].apply(lambda n: f"gs-{n:04d}")
            mask = (
                ref.str.contains(q, regex=False)
                | view["service"].str.lower().str.contains(q, regex=False)
                | view["description"].str.lower().str.contains(q, regex=False)
            )
            view = view[mask]

        st.caption(f"Showing {len(view)} of {len(complaints)} complaints")

        if view.empty:
            callout("warn", "No complaints match these filters.")
        else:
            table(
                ["Ref", "Service", "Description", "Priority",
                 "Team", "Status", "Reported"],
                complaint_rows(view, with_description=True)
            )

        st.markdown('<div class="section-label">Update a Complaint</div>', unsafe_allow_html=True)

        selected_id = st.selectbox(
            "Complaint reference",
            complaints["id"].tolist(),
            format_func=lambda number: f"GS-{number:04d}"
        )

        selected = complaints[complaints["id"] == selected_id].iloc[0]

        st.markdown(
            f'<div class="card"><div class="card-title">GS-{int(selected["id"]):04d} '
            f'&nbsp;{pill(selected["priority"])}</div>'
            f'<div style="color:#5B6785;font-size:0.85rem">Service: '
            f'<b style="color:#14213D">{esc(selected["service"])}</b></div>'
            f'<div style="margin-top:6px">{esc(selected["description"])}</div></div>',
            unsafe_allow_html=True
        )

        with st.form("update_complaint_form"):

            f1, f2 = st.columns(2)

            new_status = f1.selectbox(
                "Complaint status",
                COMPLAINT_STATUSES,
                index=COMPLAINT_STATUSES.index(selected["status"])
            )

            new_team = f2.selectbox(
                "Assigned team",
                TEAMS,
                index=TEAMS.index(selected["assigned_team"])
            )

            save_complaint = st.form_submit_button("Save Complaint Update")

        if save_complaint:

            resolved_at = now() if new_status == "Resolved" else None

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
# 7. HOUSING AFFORDABILITY CALCULATOR
# ==================================================

elif page == "Housing Affordability":

    page_header(
        "Can families afford the move?",
        "Compare monthly expenses before and after relocation.",
        [("🏠", "Housing payment"), ("💡", "Utilities & upkeep"), ("🚌", "Commuting costs")]
    )

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-label">Before Relocation</div>', unsafe_allow_html=True)
        with st.container(border=True):
            old_housing = st.number_input(
                "Rent or housing payment (₹/month)",
                min_value=0, value=2000, step=500, key="old_housing"
            )
            old_utilities = st.number_input(
                "Utilities (₹/month)",
                min_value=0, value=800, step=100, key="old_utilities"
            )
            old_maintenance = st.number_input(
                "Maintenance (₹/month)",
                min_value=0, value=200, step=100, key="old_maintenance"
            )
            old_transport = st.number_input(
                "Commuting (₹/month)",
                min_value=0, value=1000, step=100, key="old_transport"
            )

    with right:
        st.markdown('<div class="section-label">After Relocation</div>', unsafe_allow_html=True)
        with st.container(border=True):
            new_housing = st.number_input(
                "Rent, EMI or housing payment (₹/month)",
                min_value=0, value=0, step=500, key="new_housing"
            )
            new_utilities = st.number_input(
                "Utilities (₹/month)",
                min_value=0, value=1500, step=100, key="new_utilities"
            )
            new_maintenance = st.number_input(
                "Maintenance (₹/month)",
                min_value=0, value=1500, step=100, key="new_maintenance"
            )
            new_transport = st.number_input(
                "Commuting (₹/month)",
                min_value=0, value=2500, step=100, key="new_transport"
            )

    old_total = old_housing + old_utilities + old_maintenance + old_transport
    new_total = new_housing + new_utilities + new_maintenance + new_transport
    difference = new_total - old_total

    st.markdown('<div class="section-label">Cost Comparison</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi("Before", f"{money(old_total)}/mo"), unsafe_allow_html=True)
    c2.markdown(kpi("After", f"{money(new_total)}/mo", color="#6B7FB8"), unsafe_allow_html=True)

    diff_color = "#C0392B" if difference > 0 else GREEN
    pct = f"{difference / old_total * 100:+.1f}% vs before" if old_total > 0 else ""
    c3.markdown(
        kpi("Monthly Difference", f"{'+' if difference > 0 else ''}{money(difference)}", pct, diff_color),
        unsafe_allow_html=True
    )

    items = [
        ("Housing payment", old_housing, new_housing),
        ("Utilities", old_utilities, new_utilities),
        ("Maintenance", old_maintenance, new_maintenance),
        ("Commuting", old_transport, new_transport),
        ("Total", old_total, new_total),
    ]
    table(
        ["Expense", "Before", "After", "Change"],
        [
            [esc(n), money(o), money(nw), change_html(nw - o)]
            for n, o, nw in items
        ],
        num_cols=(1, 2, 3),
        total_last=True
    )

    if difference > 0:
        callout("warn", "The entered expenses increase after relocation.")
    elif difference < 0:
        callout("ok", "The entered expenses decrease after relocation.")
    else:
        callout("info", "The entered expenses are unchanged.")

    st.caption(
        "This calculation covers only the expenses entered. "
        "It excludes income, food, healthcare and other costs, "
        "so it is not a complete household affordability assessment."
    )


# ==================================================
# 8. RELOCATION IMPACT CHECKER
# ==================================================

elif page == "Relocation Impact":

    page_header(
        "What does relocation cost in time and fare?",
        "Compare journeys to work, school and healthcare before and after.",
        [("⏱️", "Travel time"), ("💰", "Monthly fare"), ("📍", "Distance from work")]
    )

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-label">Before Relocation</div>', unsafe_allow_html=True)
        with st.container(border=True):
            old_destination = st.text_input(
                "Destination", value="Workplace", key="old_destination"
            )
            old_minutes = st.number_input(
                "One-way journey (minutes)",
                min_value=0, value=30, step=5, key="old_minutes"
            )
            old_fare = st.number_input(
                "One-way travel cost (₹)",
                min_value=0, value=20, step=5, key="old_fare"
            )

    with right:
        st.markdown('<div class="section-label">After Relocation</div>', unsafe_allow_html=True)
        with st.container(border=True):
            new_destination = st.text_input(
                "Destination", value="Workplace", key="new_destination"
            )
            new_minutes = st.number_input(
                "One-way journey (minutes)",
                min_value=0, value=55, step=5, key="new_minutes"
            )
            new_fare = st.number_input(
                "One-way travel cost (₹)",
                min_value=0, value=45, step=5, key="new_fare"
            )

    journeys = st.number_input(
        "Return journeys per month",
        min_value=0, value=26, step=1
    )

    old_monthly_cost = old_fare * 2 * journeys
    new_monthly_cost = new_fare * 2 * journeys
    old_monthly_time = old_minutes * 2 * journeys
    new_monthly_time = new_minutes * 2 * journeys

    cost_diff = new_monthly_cost - old_monthly_cost
    time_diff = (new_monthly_time - old_monthly_time) / 60

    st.markdown('<div class="section-label">Comparison Results</div>', unsafe_allow_html=True)

    a, b, c, d = st.columns(4)
    a.markdown(kpi("Travel cost before", money(old_monthly_cost), "per month"), unsafe_allow_html=True)
    b.markdown(
        kpi("Travel cost after", money(new_monthly_cost),
            f"{cost_diff:+,.0f} ₹ vs before", "#C0392B" if cost_diff > 0 else GREEN),
        unsafe_allow_html=True
    )
    c.markdown(kpi("Travel time before", f"{old_monthly_time / 60:.1f} h", "per month"), unsafe_allow_html=True)
    d.markdown(
        kpi("Travel time after", f"{new_monthly_time / 60:.1f} h",
            f"{time_diff:+.1f} h vs before", "#C0392B" if time_diff > 0 else GREEN),
        unsafe_allow_html=True
    )

    table(
        ["Measure", "Before", "After"],
        [
            ["Destination", esc(old_destination), esc(new_destination)],
            ["One-way travel time (minutes)", f"{old_minutes}", f"{new_minutes}"],
            ["One-way fare (₹)", f"{old_fare}", f"{new_fare}"],
            ["Monthly travel cost (₹)", f"{old_monthly_cost:,.0f}", f"{new_monthly_cost:,.0f}"],
            ["Monthly travel time (hours)",
             f"{old_monthly_time / 60:.1f}", f"{new_monthly_time / 60:.1f}"],
        ],
        num_cols=(1, 2)
    )

    callout(
        "info",
        "Repeat this assessment for schools, healthcare facilities and "
        "markets to develop a broader relocation comparison."
    )

    st.caption(
        "All journey times and fares are manually entered estimates, "
        "not live mapping data."
    )


# ==================================================
# 9. FOOTER
# ==================================================

st.markdown(
    '<div class="foot">PLACE FORWARD | GharSure | Seva Innovation Challenge 2026<br>'
    'Student prototype • Simulated data • No live government integration</div>',
    unsafe_allow_html=True
)