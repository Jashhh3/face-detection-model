import streamlit as st
from PIL import Image
import numpy as np
import tempfile
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Face Verification Prototype Demo",
    page_icon="🔍",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* ---- Root palette ---- */
:root {
    --bg:          #0D0F14;
    --surface:     #161A22;
    --border:      #242830;
    --accent:      #4F8EF7;
    --accent-dim:  #1C2D4A;
    --success:     #22C97A;
    --success-dim: #0D2E1E;
    --danger:      #F25C5C;
    --danger-dim:  #2E1212;
    --text:        #E8ECF4;
    --muted:       #6B7280;
}

/* ---- Base overrides ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text);
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
footer { visibility: hidden; }

/* ---- Hero banner ---- */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 1.8rem;
}
.hero-badge {
    display: inline-block;
    background: var(--accent-dim);
    color: var(--accent);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-radius: 4px;
    padding: 4px 12px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(1.7rem, 4vw, 2.6rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
    margin: 0 0 0.6rem;
    line-height: 1.15;
}
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ---- Step cards ---- */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.5rem 1rem;
    margin-bottom: 1.2rem;
}
.step-label {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.9rem;
}
.step-num {
    width: 26px; height: 26px;
    background: var(--accent-dim);
    color: var(--accent);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step-title {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text);
    letter-spacing: 0.01em;
}

/* ---- Result boxes ---- */
.result-box {
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
}
.result-box.success {
    background: var(--success-dim);
    border: 1px solid var(--success);
}
.result-box.danger {
    background: var(--danger-dim);
    border: 1px solid var(--danger);
}
.result-box.warn {
    background: #1E1C0D;
    border: 1px solid #C9A227;
}
.result-icon { font-size: 1.4rem; line-height: 1; padding-top: 2px; }
.result-body h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
}
.result-body.success h3 { color: var(--success); }
.result-body.danger  h3 { color: var(--danger); }
.result-body.warn    h3 { color: #C9A227; }
.result-body p {
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.5;
}

/* ---- Score pill ---- */
.score-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-top: 0.6rem;
}
.score-label { font-size: 0.78rem; color: var(--muted); }
.score-pill {
    background: var(--accent);
    color: #fff;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 0.82rem;
    padding: 2px 10px;
    border-radius: 99px;
}

/* ---- Divider ---- */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.8rem 0;
}

/* ---- Streamlit widget tweaks ---- */
[data-testid="stFileUploadDropzone"],
[data-testid="stCameraInputButton"] {
    background: var(--bg) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stImage"] img {
    border-radius: 8px;
    border: 1px solid var(--border);
}
.stButton button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔐 Identity Verification</div>
    <h1>Face Verification<br>Prototype Demo</h1>
    <p>Upload a reference photo and capture a live photo to verify if they belong to the same person.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── Helper: save PIL image to a temp file ─────────────────────────────────────
def pil_to_tempfile(img: Image.Image, suffix=".jpg") -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    img.save(tmp.name)
    return tmp.name


# ── Step 1 & 2 – Side by side ─────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-label">
            <div class="step-num">1</div>
            <span class="step-title">Upload Reference Profile Photo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload a clear, front-facing photo (JPEG or PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    ref_image = None
    if uploaded_file:
        ref_image = Image.open(uploaded_file).convert("RGB")
        st.image(ref_image, caption="Reference photo", width=None)
        st.markdown(
            '<div class="result-box warn"><div class="result-icon">💡</div>'
            '<div class="result-body warn"><p>Use a well-lit, front-facing photo for the best accuracy.</p></div></div>',
            unsafe_allow_html=True,
        )

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-label">
            <div class="step-num">2</div>
            <span class="step-title">Capture Live Photo for Verification</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    camera_photo = st.camera_input(
        "Look directly at the camera, then click the shutter",
        label_visibility="collapsed",
    )

    live_image = None
    if camera_photo:
        live_image = Image.open(camera_photo).convert("RGB")
        st.image(live_image, caption="Live capture", width=None)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── Step 3 – Verification ─────────────────────────────────────────────────────
if ref_image and live_image:
    st.markdown("""
    <div class="step-card">
        <div class="step-label">
            <div class="step-num">3</div>
            <span class="step-title">Running Verification…</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analysing facial features with DeepFace · VGG-Face…"):
        try:
            from deepface import DeepFace  # lazy import – avoids cold-start cost

            ref_path  = pil_to_tempfile(ref_image)
            live_path = pil_to_tempfile(live_image)

            result = DeepFace.verify(
                img1_path   = ref_path,
                img2_path   = live_path,
                model_name  = "VGG-Face",
                detector_backend = "opencv",
                enforce_detection = True,
            )

            # Clean up temp files
            os.unlink(ref_path)
            os.unlink(live_path)

            verified  = result.get("verified", False)
            distance  = result.get("distance", None)
            threshold = result.get("threshold", None)

            # Convert cosine / euclidean distance → a 0-100 similarity score
            if distance is not None and threshold is not None:
                # Normalise: distance=0 → 100 %, distance=threshold → ~50 %
                similarity_pct = max(0, round((1 - distance / (threshold * 2)) * 100, 1))
            else:
                similarity_pct = None

            if verified:
                score_html = ""
                if similarity_pct is not None:
                    score_html = (
                        f'<div class="score-row">'
                        f'<span class="score-label">Similarity score</span>'
                        f'<span class="score-pill">{similarity_pct}%</span>'
                        f'</div>'
                    )
                st.markdown(
                    f'<div class="result-box success">'
                    f'  <div class="result-icon">✅</div>'
                    f'  <div class="result-body success">'
                    f'    <h3>Verification Successful! Match Confirmed.</h3>'
                    f'    <p>The two photos appear to depict the same person.</p>'
                    f'    {score_html}'
                    f'  </div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="result-box danger">'
                    '  <div class="result-icon">❌</div>'
                    '  <div class="result-body danger">'
                    '    <h3>Verification Failed! Faces do not match.</h3>'
                    '    <p>The reference photo and the live capture do not belong to the same person.</p>'
                    '  </div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

        except ValueError as e:
            st.markdown(
                f'<div class="result-box warn">'
                f'  <div class="result-icon">⚠️</div>'
                f'  <div class="result-body warn">'
                f'    <h3>Face Not Detected</h3>'
                f'    <p>Could not locate a face in one or both images. Make sure the face is clearly visible, well-lit, and centred. Detail: <code>{e}</code></p>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.markdown(
                f'<div class="result-box danger">'
                f'  <div class="result-icon">🔴</div>'
                f'  <div class="result-body danger">'
                f'    <h3>Unexpected Error</h3>'
                f'    <p><code>{e}</code></p>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )

elif not ref_image and not live_image:
    st.markdown(
        '<div class="result-box warn"><div class="result-icon">👆</div>'
        '<div class="result-body warn"><p>Complete both steps above to start verification.</p></div></div>',
        unsafe_allow_html=True,
    )
elif not live_image:
    st.markdown(
        '<div class="result-box warn"><div class="result-icon">📷</div>'
        '<div class="result-body warn"><p>Capture a live photo in Step 2 to continue.</p></div></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="result-box warn"><div class="result-icon">🖼️</div>'
        '<div class="result-body warn"><p>Upload a reference photo in Step 1 to continue.</p></div></div>',
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;font-size:0.75rem;color:#6B7280;">'
    'Powered by <strong>DeepFace · VGG-Face</strong> &nbsp;|&nbsp; For demonstration purposes only'
    '</p>',
    unsafe_allow_html=True,
)
