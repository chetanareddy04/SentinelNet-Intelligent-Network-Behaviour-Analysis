
import streamlit as st
import pandas as pd
import pickle
import html
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SentinelNet",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent

CLASSIFICATION_FILE = BASE_DIR / "sentinelnet_classification_model.pkl"
CLUSTERING_FILE = BASE_DIR / "SentinelNet_clustering_pipeline.pkl"

# Find the banner image saved in the project folder
IMAGE_CANDIDATES = [
    "banner.png", "banner.jpg",
    "sentinelnet_banner.png", "sentinelnet_banner.jpg",
    "home_banner.png", "home_banner.jpg",
    "cybersecurity.png", "cybersecurity.jpg",
    "banner.jpeg", "sentinelnet.png"
]

BANNER_IMAGE = None

for image_name in IMAGE_CANDIDATES:
    image_path = BASE_DIR / image_name
    if image_path.exists():
        BANNER_IMAGE = image_path
        break

if BANNER_IMAGE is None:
    for extension in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
        images = list(BASE_DIR.glob(extension))
        if images:
            BANNER_IMAGE = images[0]
            break


# =========================================================
# CLUSTER INTERPRETATIONS
# =========================================================

CLUSTER_INTERPRETATION = {
    0: {
        "name": "UDP-Based Short-Burst Traffic",
        "description": (
            "Very short-duration connections with high transmission "
            "rates and low packet counts. UDP and INT state are dominant."
        )
    },
    1: {
        "name": "TCP-Based Moderate-Volume Traffic",
        "description": (
            "TCP connections with moderate packet counts and packet "
            "sizes. Most connections have the FIN state."
        )
    },
    2: {
        "name": "DNS-Dominated High-Rate Traffic",
        "description": (
            "Short-duration, high-rate connections with low packet "
            "counts and high endpoint, port and service activity. "
            "UDP and DNS are dominant."
        )
    },
    3: {
        "name": "TCP-Based Irregular-Timing Traffic",
        "description": (
            "TCP connections with unusually high inter-packet times "
            "and jitter, indicating irregular communication timing."
        )
    },
    4: {
        "name": "High-Volume SMTP-Associated Traffic",
        "description": (
            "Long-duration connections with very high packet volume, "
            "packet size and packet loss. TCP is dominant, with SMTP "
            "as the leading service."
        )
    },
    5: {
        "name": "ARP-Based Short-Packet Traffic",
        "description": (
            "ARP-based connections with very low packet counts and "
            "the same source-destination IP/port condition."
        )
    },
    6: {
        "name": "FTP-Based Communication Traffic",
        "description": (
            "TCP connections associated with FTP service and FTP "
            "command activity, with moderate packet volume and packet loss."
        )
    },
    7: {
        "name": "TCP-Based High-Volume Data Transfer",
        "description": (
            "TCP connections with comparatively high packet counts, "
            "larger packet sizes and higher destination-side data load."
        )
    }
}


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fc;
    color: #172b4d;
}

header[data-testid="stHeader"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stAppViewBlockContainer {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1250px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #102a43;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 9px 12px;
    margin-bottom: 7px;
}

/* Headings */

h1, h2, h3 {
    color: #102a43 !important;
}

/* Dashboard cards */

.dashboard-card {
    background: white;
    border: 1px solid #e1e9f0;
    border-radius: 15px;
    padding: 24px;
    min-height: 210px;
    box-shadow: 0 4px 15px rgba(16,42,67,0.05);
}

.dashboard-card h3 {
    color: #102a43;
    font-size: 21px;
    margin-top: 10px;
    margin-bottom: 8px;
}

.dashboard-card p {
    color: #627d98;
    font-size: 14px;
    line-height: 1.6;
}

.card-icon {
    font-size: 32px;
}

/* Page introduction */

.page-intro {
    background: white;
    border-left: 5px solid #2878b5;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(16,42,67,0.04);
}

.page-intro p {
    color: #627d98;
    font-size: 14px;
    margin-bottom: 0;
    line-height: 1.6;
}

/* Result cards */

.result-card {
    background: white;
    border: 1px solid #dce6ef;
    border-radius: 14px;
    padding: 25px;
    margin-top: 18px;
    box-shadow: 0 4px 15px rgba(16,42,67,0.04);
}

.result-normal {
    border-left: 6px solid #16a36a;
}

.result-attack {
    border-left: 6px solid #e05252;
}

.result-cluster {
    border-left: 6px solid #2878b5;
}

.result-label {
    color: #627d98;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.result-heading {
    font-size: 25px;
    font-weight: 800;
    color: #102a43;
    margin-top: 8px;
}

.cluster-name {
    color: #174a72;
    font-size: 19px;
    font-weight: 700;
    margin-top: 12px;
}

.result-description {
    color: #627d98;
    font-size: 14px;
    line-height: 1.7;
    margin-top: 12px;
}

/* Buttons */

.stButton > button,
.stFormSubmitButton > button {
    background-color: #174a72;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #102a43;
    color: white;
    border: none;
}

/* Input fields */

div[data-testid="stNumberInput"] input {
    border-radius: 8px;
}

div[data-testid="stSelectbox"] {
    border-radius: 8px;
}

/* Footer */

.footer {
    text-align: center;
    color: #829ab1;
    font-size: 12px;
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODELS
# =========================================================

@st.cache_resource
def load_models():

    classification_model = None
    clustering_artifacts = None
    errors = []

    if CLASSIFICATION_FILE.exists():

        try:
            with open(CLASSIFICATION_FILE, "rb") as file:
                classification_model = pickle.load(file)

        except Exception as e:
            errors.append(f"Classification model error: {e}")

    else:
        errors.append(
            f"Missing file: {CLASSIFICATION_FILE.name}"
        )

    if CLUSTERING_FILE.exists():

        try:
            with open(CLUSTERING_FILE, "rb") as file:
                clustering_artifacts = pickle.load(file)

            if not isinstance(clustering_artifacts, dict):
                raise ValueError(
                    "Clustering pickle must contain a dictionary."
                )

            for key in ["preprocessing", "pca", "kmeans"]:

                if key not in clustering_artifacts:
                    raise ValueError(
                        f"Missing '{key}' in clustering pickle."
                    )

        except Exception as e:
            errors.append(f"Clustering model error: {e}")

    else:
        errors.append(
            f"Missing file: {CLUSTERING_FILE.name}"
        )

    return classification_model, clustering_artifacts, errors


classification_model, clustering_artifacts, model_errors = load_models()


# =========================================================
# FEATURE ENGINEERING
# =========================================================

DERIVED_FEATURES = {
    "total_packets": ["spkts", "dpkts"],
    "total_packet_size": ["sbytes", "dbytes"],
    "total_packet_loss": ["sloss", "dloss"],
    "total_endpoint_activity": ["ct_src_ltm", "ct_dst_ltm"],
    "total_port_activity": [
        "ct_src_dport_ltm", "ct_dst_sport_ltm"
    ],
    "total_service_activity": [
        "ct_srv_src", "ct_srv_dst"
    ],
    "total_application_activity": [
        "ct_ftp_cmd", "ct_flw_http_mthd"
    ]
}


def engineer_features(df):

    df = df.copy()

    for new_feature, source_features in DERIVED_FEATURES.items():

        if all(col in df.columns for col in source_features):

            df[new_feature] = (
                df[source_features[0]] +
                df[source_features[1]]
            )

    return df


# =========================================================
# MODEL FEATURE DETECTION
# =========================================================

def get_feature_names(model):

    if model is None:
        return []

    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)

    if hasattr(model, "named_steps"):

        for _, step in reversed(
            list(model.named_steps.items())
        ):

            if hasattr(step, "feature_names_in_"):
                return list(step.feature_names_in_)

    return []


def get_clustering_features(artifacts):

    if not artifacts:
        return []

    preprocessing = artifacts["preprocessing"]

    if hasattr(preprocessing, "feature_names_in_"):
        return list(preprocessing.feature_names_in_)

    return []


classification_features = get_feature_names(
    classification_model
)

clustering_features = get_clustering_features(
    clustering_artifacts
)


# =========================================================
# INPUT FEATURE GROUPS
# =========================================================

FEATURE_GROUPS = {

    "Connection Details": [
        "dur", "proto", "service", "state"
    ],

    "Packet & Traffic Statistics": [
        "spkts", "dpkts", "sbytes", "dbytes",
        "rate", "sloss", "dloss", "smean", "dmean"
    ],

    "Network Timing & TCP": [
        "sttl", "dttl", "sload", "dload",
        "sinpkt", "dinpkt", "sjit", "djit",
        "swin", "stcpb", "dtcpb", "dwin",
        "tcprtt", "synack", "ackdat"
    ],

    "Connection Activity": [
        "ct_srv_src", "ct_state_ttl", "ct_dst_ltm",
        "ct_src_dport_ltm", "ct_dst_sport_ltm",
        "ct_dst_src_ltm", "ct_src_ltm", "ct_srv_dst"
    ],

    "Application Behaviour": [
        "trans_depth", "response_body_len",
        "is_ftp_login", "ct_ftp_cmd",
        "ct_flw_http_mthd", "is_sm_ips_ports"
    ]
}


CATEGORICAL_OPTIONS = {

    "proto": [
        "tcp", "udp", "arp", "ospf", "icmp",
        "igmp", "sctp", "gre", "ip", "unas",
        "ipv6", "rtp", "ddp", "esp", "pim"
    ],

    "service": [
        "-", "http", "ftp", "ftp-data",
        "smtp", "ssh", "dns", "pop3",
        "dhcp", "snmp", "ssl"
    ],

    "state": [
        "FIN", "INT", "CON", "REQ",
        "RST", "ACC", "CLO", "ECO",
        "URH", "PAR", "no"
    ]
}


# Friendly input labels

FEATURE_LABELS = {
    "dur": "Connection Duration",
    "proto": "Network Protocol",
    "service": "Network Service",
    "state": "Connection State",
    "spkts": "Source Packets",
    "dpkts": "Destination Packets",
    "sbytes": "Source Bytes",
    "dbytes": "Destination Bytes",
    "rate": "Traffic Rate",
    "sloss": "Source Packet Loss",
    "dloss": "Destination Packet Loss",
    "smean": "Average Source Packet Size",
    "dmean": "Average Destination Packet Size",
    "sttl": "Source TTL",
    "dttl": "Destination TTL",
    "sload": "Source Data Load",
    "dload": "Destination Data Load",
    "sinpkt": "Source Inter-Packet Time",
    "dinpkt": "Destination Inter-Packet Time",
    "sjit": "Source Jitter",
    "djit": "Destination Jitter",
    "swin": "Source TCP Window",
    "stcpb": "Source TCP Base",
    "dtcpb": "Destination TCP Base",
    "dwin": "Destination TCP Window",
    "tcprtt": "TCP Round Trip Time",
    "synack": "SYN-ACK Time",
    "ackdat": "ACK Data Time",
    "ct_srv_src": "Service Source Count",
    "ct_state_ttl": "State TTL Count",
    "ct_dst_ltm": "Destination Connection Count",
    "ct_src_dport_ltm": "Source Destination-Port Count",
    "ct_dst_sport_ltm": "Destination Source-Port Count",
    "ct_dst_src_ltm": "Destination-Source Count",
    "ct_src_ltm": "Source Connection Count",
    "ct_srv_dst": "Service Destination Count",
    "trans_depth": "Transaction Depth",
    "response_body_len": "Response Body Length",
    "is_ftp_login": "FTP Login",
    "ct_ftp_cmd": "FTP Command Count",
    "ct_flw_http_mthd": "HTTP Method Count",
    "is_sm_ips_ports": "Same IP and Port"
}

BINARY_FEATURES = [
    "is_ftp_login",
    "is_sm_ips_ports"
]


# =========================================================
# REQUIRED INPUT FEATURES
# =========================================================

def get_required_input_features(model_features):

    if not model_features:
        return []

    required = set(model_features)

    for feature in list(required):

        if feature in DERIVED_FEATURES:

            required.remove(feature)

            required.update(
                DERIVED_FEATURES[feature]
            )

    return [
        feature
        for group in FEATURE_GROUPS.values()
        for feature in group
        if feature in required
    ]


# =========================================================
# INPUT FORM
# =========================================================

def render_input_form(
    required_features,
    form_key,
    submit_label="Run Analysis"
):

    if not required_features:

        st.error(
            "Unable to identify model input features. "
            "Check the feature names in the saved model."
        )

        return None

    feature_values = {}

    with st.form(form_key):

        st.caption(
            "Enter the network traffic details below."
        )

        for group_name, group_features in FEATURE_GROUPS.items():

            selected_features = [
                feature
                for feature in group_features
                if feature in required_features
            ]

            if not selected_features:
                continue

            with st.expander(
                group_name,
                expanded=(group_name == "Connection Details")
            ):

                columns = st.columns(3)

                for index, feature in enumerate(
                    selected_features
                ):

                    with columns[index % 3]:

                        display_name = FEATURE_LABELS.get(
                            feature,
                            feature.replace("_", " ").title()
                        )

                        if feature in CATEGORICAL_OPTIONS:

                            feature_values[feature] = st.selectbox(
                                display_name,
                                CATEGORICAL_OPTIONS[feature],
                                key=f"{form_key}_{feature}"
                            )

                        elif feature in BINARY_FEATURES:

                            binary_value = st.selectbox(
                                display_name,
                                ["No", "Yes"],
                                key=f"{form_key}_{feature}"
                            )

                            feature_values[feature] = (
                                1 if binary_value == "Yes" else 0
                            )

                        else:

                            feature_values[feature] = st.number_input(
                                display_name,
                                min_value=0.0,
                                value=0.0,
                                step=0.1,
                                format="%.4f",
                                key=f"{form_key}_{feature}"
                            )

        submitted = st.form_submit_button(
            submit_label,
            use_container_width=True
        )

    if submitted:
        return feature_values

    return None


# =========================================================
# PREPARE MODEL INPUT
# =========================================================

def prepare_model_input(input_values, model_features):

    input_df = pd.DataFrame([input_values])

    input_df = engineer_features(input_df)

    X = input_df.reindex(
        columns=model_features
    )

    if X.isnull().any().any():

        missing = X.columns[
            X.isnull().any()
        ].tolist()

        raise ValueError(
            f"Required model features are missing: {missing}"
        )

    return X


# =========================================================
# SIDEBAR
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"


with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:15px 5px 25px;">
        <div style="font-size:45px;">🛡️</div>
        <h2 style="color:white !important; margin-bottom:0;">
            SentinelNet
        </h2>
        <p style="color:#bcccdc; font-size:12px;">
            Intelligent Network Security
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.radio(
        "Navigation",
        [
            "Home",
            "Intrusion Detection",
            "Behaviour Analysis"
        ],
        key="page"
    )

    st.markdown("---")

    st.caption("Network Security Analytics")


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    # Show only the existing banner image
    if BANNER_IMAGE is not None:
        st.image(
            str(BANNER_IMAGE),
            use_container_width=True
        )

    st.markdown("### Security Analytics")

    st.write(
        "Select an analysis module to examine network traffic."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.html("""
        <div class="dashboard-card">
            <div class="card-icon">🔍</div>
            <h3>Intrusion Detection</h3>
            <p>
                Examine network traffic and identify whether
                the activity is normal or potentially malicious.
            </p>
            <p><b>Output:</b> Normal / Attack</p>
        </div>
        """)

        if st.button(
            "Open Intrusion Detection →",
            use_container_width=True
        ):
            st.session_state.page = "Intrusion Detection"
            st.rerun()

    with col2:

        st.html("""
        <div class="dashboard-card">
            <div class="card-icon">📊</div>
            <h3>Behaviour Analysis</h3>
            <p>
                Explore network traffic patterns and group
                connections according to their behaviour.
            </p>
            <p><b>Output:</b> Behavioural Cluster</p>
        </div>
        """)

        if st.button(
            "Open Behaviour Analysis →",
            use_container_width=True
        ):
            st.session_state.page = "Behaviour Analysis"
            st.rerun()

    st.html("""
    <div class="footer">
        SentinelNet | Network Security Analytics
    </div>
    """)


# =========================================================
# INTRUSION DETECTION PAGE
# =========================================================

elif st.session_state.page == "Intrusion Detection":

    st.title("🔍 Intrusion Detection")

    st.html("""
    <div class="page-intro">
        <p>
            Examine the network connection details below to determine
            whether the traffic represents normal activity or an attack.
            Provide the available traffic characteristics and run the analysis.
        </p>
    </div>
    """)

    if classification_model is None:

        st.error(
            "Classification model could not be loaded."
        )

    else:

        required_features = get_required_input_features(
            classification_features
        )

        input_values = render_input_form(
            required_features,
            "classification_form",
            submit_label="🔍 Detect Intrusion"
        )

        if input_values is not None:

            try:

                X = prepare_model_input(
                    input_values,
                    classification_features
                )

                prediction = classification_model.predict(X)[0]

                prediction_text = str(
                    prediction
                ).strip().lower()

                if prediction_text in [
                    "1", "1.0", "attack"
                ]:

                    result = "Attack"
                    result_class = "result-attack"
                    result_icon = "🚨"

                elif prediction_text in [
                    "0", "0.0", "normal"
                ]:

                    result = "Normal"
                    result_class = "result-normal"
                    result_icon = "✅"

                else:

                    raise ValueError(
                        f"Unexpected classification output: {prediction}"
                    )

                st.html(f"""
                <div class="result-card {result_class}">
                    <div class="result-label">
                        Classification Result
                    </div>
                    <div class="result-heading">
                        {result_icon} {html.escape(result)}
                    </div>
                </div>
                """)

            except Exception as e:

                st.error(
                    f"Prediction error: {str(e)}"
                )


# =========================================================
# BEHAVIOUR ANALYSIS PAGE
# =========================================================

elif st.session_state.page == "Behaviour Analysis":

    st.title("📊 Network Behaviour Analysis")

    st.html("""
    <div class="page-intro">
        <p>
            Explore the behavioural pattern of a network connection.
            Enter the traffic characteristics below to identify the
            behavioural group that best represents this connection.
        </p>
    </div>
    """)

    if clustering_artifacts is None:

        st.error(
            "Clustering pipeline could not be loaded."
        )

    else:

        preprocessing = clustering_artifacts["preprocessing"]
        pca = clustering_artifacts["pca"]
        kmeans = clustering_artifacts["kmeans"]

        required_features = get_required_input_features(
            clustering_features
        )

        if int(kmeans.n_clusters) != len(CLUSTER_INTERPRETATION):

            st.warning(
                f"The saved clustering model has {kmeans.n_clusters} "
                f"clusters, while the interpretation table has "
                f"{len(CLUSTER_INTERPRETATION)} clusters. "
                "Please verify the saved model."
            )

        input_values = render_input_form(
            required_features,
            "clustering_form",
            submit_label="📊 Analyze Behaviour"
        )

        if input_values is not None:

            try:

                X = prepare_model_input(
                    input_values,
                    clustering_features
                )

                X_processed = preprocessing.transform(X)

                X_pca = pca.transform(X_processed)

                cluster_prediction = int(
                    kmeans.predict(X_pca)[0]
                )

                if cluster_prediction not in CLUSTER_INTERPRETATION:

                    raise ValueError(
                        f"No interpretation available for "
                        f"Cluster {cluster_prediction}."
                    )

                cluster_info = CLUSTER_INTERPRETATION[
                    cluster_prediction
                ]

                cluster_name = cluster_info["name"]
                cluster_description = cluster_info["description"]

                st.html(f"""
                <div class="result-card result-cluster">

                    <div class="result-label">
                        Assigned Behavioural Cluster
                    </div>

                    <div class="result-heading">
                        Cluster {cluster_prediction}
                    </div>

                    <div class="cluster-name">
                        {html.escape(cluster_name)}
                    </div>

                    <div class="result-description">
                        {html.escape(cluster_description)}
                    </div>

                </div>
                """)

            except Exception as e:

                st.error(
                    f"Clustering error: {str(e)}"
                )


# =========================================================
# MODEL LOADING DETAILS
# =========================================================

if model_errors:

    with st.sidebar:

        with st.expander("Model Loading Details"):

            for error in model_errors:
                st.error(error)
