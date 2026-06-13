# Biometric Face Verification Security Protocol

A high-fidelity biometric identity verification system built with **Python 3.11**, **Streamlit**, **DeepFace**, and **OpenCV**. The application performs facial comparison, identifies face shapes, and executes liveness eye-blink checks locally.

---

## 🚀 Key Features

*   **Credential Verification**: Upload a reference ID/credential photo and compare it in real-time with a live camera capture.
*   **Facial Geometry Diagnostics**: Calculates and identifies face shapes (Oval, Oblong, Square, Round) geometrically using facial bounding boxes.
*   **Liveness Verification (Blink Test)**: Actively tracks eye status using Haar Cascade Classifiers to verify active users and prevent spoofing with static photos.
*   **Biometric Diagnostics Dashboard**: Real-time side-by-side feed display featuring green/red neon biometric scanning overlays.
*   **Deep Learning Matching**: Employs the **VGG-Face** model via the **DeepFace** engine for high-accuracy feature distance comparisons.
*   **Premium Soft Pink / Coral UI**: Styled interface inspired by high-end mobile biometric design mockups.

---

## 🛠️ Tech Stack

*   **Frontend UI**: [Streamlit](https://streamlit.io/)
*   **Verification Engine**: [DeepFace](https://github.com/serengil/deepface) (VGG-Face, Cosine Distance)
*   **Computer Vision Diagnostics**: [OpenCV](https://opencv.org/) (Haar Cascade Classifiers)
*   **Language & Environment**: Python 3.11, Virtual Environment (`venv`)

---

## 📦 Local Installation & Setup

```powershell
# 1. Clone the repository and enter directory
git clone https://github.com/haiyvradynamics/face-verification-model.git
cd face-verification-model

# 2. Set up and activate Python 3.11 virtual environment
py -3.11 -m venv .venv
& .venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install --upgrade pip
pip install streamlit deepface tf-keras opencv-python tensorflow
```

---

## 🖥️ How to Run the App

1. Ensure your virtual environment is active.
2. Launch the Streamlit server:
   ```bash
   streamlit run face_verification_app.py
   ```
3. Open your browser and navigate to `http://localhost:8501`.

---

## 📂 Project Directory Structure

```text
├── .venv/                      # Python virtual environment (ignored by Git)
├── .gitignore                  # Git exclude configurations
├── README.md                   # Project documentation (this file)
└── face_verification_app.py    # Main Streamlit web application source code
```

---

## ⚙️ Biometric Verification Flow

1. **Upload Reference Photo**: The user uploads a clear, front-facing profile photo. The system runs OpenCV diagnostics to verify face visibility and output reference face shapes.
2. **Capture Live Authorization**: The user captures a live snapshot using their webcam. The system runs real-time liveness checks (Blink test) and identifies the captured face shape.
3. **Biometric Report**: DeepFace matches the face vectors. If the cosine distance falls within the VGG-Face threshold, verification is successful, displaying similarity percentages and detailed diagnostic metrics.
