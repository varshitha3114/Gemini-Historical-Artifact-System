# Gemini Historical Artifact Studio

A local Streamlit app for offline and optional cloud-assisted historical artifact analysis.

Quick start

1. Create and activate the virtual environment (if not already):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Enable Cloud AI: copy `.env.example` to `.env` and add your key:

```text
GOOGLE_API_KEY=your_api_key_here
```

To enable cloud features you should upgrade the SDK to the latest supported package and ensure it exposes a text generation helper. Example:

```powershell
pip install --upgrade google-generativeai
```

4. Run the app:

```powershell
streamlit run app.py --server.port 8503
```

Notes

- The app runs offline by default and provides a basic heuristic-based artifact summary if cloud APIs are unavailable.
- If you add a valid `GOOGLE_API_KEY` and your installed SDK exposes a text-generation function, the app will attempt a cloud analysis.
- If you want help wiring a specific SDK function, run the diagnostic in the app or run the script below and paste the output back to me:

```powershell
python - <<'PY'
import json
try:
    import google.generativeai as genai
    print(json.dumps(sorted(dir(genai)), indent=2))
except Exception as e:
    print("IMPORT_ERROR:", e)
PY
```

Contact me with the diagnostic output and I will adapt the app to call the exact helper available in your environment.
