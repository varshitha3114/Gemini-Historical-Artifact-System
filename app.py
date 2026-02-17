"""
Gemini Historical Artifact Description System

A Streamlit web app that analyzes high-resolution images of historical artifacts
using Google Generative AI (Gemini) to generate professional archeological insights.

Usage:
  python -m streamlit run app.py
"""


import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv(dotenv_path=".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    GEMINI_MODEL = "gemini-2.5-flash"
    AVAILABLE_MODELS = []
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Get actual available models
    AVAILABLE_MODELS = []
    try:
        for model in genai.list_models():
            model_name = model.name.split('/')[-1]
            # Only include models that support generateContent
            if hasattr(model, 'supported_generation_methods'):
                if 'generateContent' in model.supported_generation_methods:
                    AVAILABLE_MODELS.append(model_name)
    except Exception as e:
        # Fallback models if list_models fails
        AVAILABLE_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"]
    
    # Select the best available model (prefer 2.5-flash)
    if "gemini-2.5-flash" in AVAILABLE_MODELS:
        GEMINI_MODEL = "gemini-2.5-flash"
    elif "gemini-2.0-flash" in AVAILABLE_MODELS:
        GEMINI_MODEL = "gemini-2.0-flash"
    elif "gemini-2.5-pro" in AVAILABLE_MODELS:
        GEMINI_MODEL = "gemini-2.5-pro"
    elif AVAILABLE_MODELS:
        GEMINI_MODEL = AVAILABLE_MODELS[0]
    else:
        GEMINI_MODEL = "gemini-2.5-flash"  # Default fallback


# ============================================================
# PROMPTS
# ============================================================

ARTIFACT_ANALYSIS_PROMPT = """
You are an expert archaeologist and historian specializing in artifact analysis.

Analyze the provided image of a historical artifact and generate a comprehensive professional report.

Please include:
1. **Artifact Type & Classification** - What category does this artifact belong to?
2. **Estimated Period/Era** - When was this likely created? (with confidence level)
3. **Materials & Composition** - What materials are visible and their significance?
4. **Dimensions & Scale** - Approximate size and proportions
5. **Craftsmanship & Technique** - How was this made? What skills were required?
6. **Condition Assessment** - Current state of preservation, visible wear, damage
7. **Cultural & Historical Significance** - Why is this important?
8. **Possible Origin & Geographic Location** - Where might this have come from?
9. **Similar Artifacts** - Known comparative examples
10. **Recommendations for Further Study** - What tests or analysis would help?

Format in clear, structured markdown. Add brief disclaimers about visual-only analysis limitations.
"""


# ============================================================
# CORE FUNCTION
# ============================================================

def get_gemini_analysis(user_notes: str, pil_image: Image.Image) -> str:
    """Generate artifact analysis using Gemini AI"""
    
    # Use available models, fallback to defaults if empty
    models_to_try = AVAILABLE_MODELS if AVAILABLE_MODELS else ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"]
    
    last_error = None
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            
            content = [ARTIFACT_ANALYSIS_PROMPT]

            if user_notes.strip():
                content.append(f"\nAdditional Context from User: {user_notes}\n")

            content.append(pil_image)

            response = model.generate_content(content)
            return response.text
            
        except Exception as e:
            last_error = e
            continue
    
    # If all models fail, raise the last error with helpful info
    error_msg = f"Failed to analyze: {str(last_error)}"
    raise Exception(error_msg)


# ============================================================
# STREAMLIT UI CONFIGURATION
# ============================================================

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="Gemini Historical Artifact Description",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for enhanced UI design
    st.markdown("""
        <style>
            /* Theme Colors */
            :root {
                --primary-color: #8B4513;
                --secondary-color: #D2B48C;
                --accent-color: #CD853F;
            }

            /* Header styling */
            .header-container {
                background: linear-gradient(135deg, #8B4513 0%, #CD853F 100%);
                padding: 2.5rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 8px 20px rgba(139, 69, 19, 0.25);
            }

            .header-container h1 {
                color: white;
                margin: 0;
                font-size: 2.8rem;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }

            .header-container p {
                color: #FFF8DC;
                margin: 0;
                font-size: 1.15rem;
            }

            /* Card styling */
            .info-card {
                background: linear-gradient(135deg, #FFF8DC 0%, #FFE4B5 100%);
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 5px solid #CD853F;
                box-shadow: 0 4px 12px rgba(139, 69, 19, 0.15);
                margin-bottom: 1rem;
            }

            /* Button styling */
            .stButton > button {
                background: linear-gradient(135deg, #8B4513 0%, #CD853F 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.8rem 2rem !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3) !important;
            }

            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 8px 20px rgba(139, 69, 19, 0.4) !important;
            }

            /* Text area styling */
            .stTextArea > div > div > textarea {
                border-radius: 8px !important;
                border: 2px solid #D2B48C !important;
            }

            /* Expander styling */
            .streamlit-expanderHeader {
                background-color: #FFF8DC !important;
                border-radius: 8px !important;
                border: 2px solid #D2B48C !important;
            }

            /* Success/Info messages */
            .stSuccess {
                background-color: #E8F5E9 !important;
                border-left: 5px solid #4CAF50 !important;
            }

            .stInfo {
                background-color: #E3F2FD !important;
                border-left: 5px solid #2196F3 !important;
            }

            .stWarning {
                background-color: #FFF3E0 !important;
                border-left: 5px solid #FF9800 !important;
            }

            .stError {
                background-color: #FFEBEE !important;
                border-left: 5px solid #F44336 !important;
            }

            /* Divider */
            hr {
                border: none;
                height: 2px;
                background: linear-gradient(90deg, transparent, #CD853F, transparent);
                margin: 2rem 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown("""
        <div class="header-container">
            <h1>Gemini Historical Artifact Description</h1>
            <p>AI-Powered Archaeological Analysis Using Google Gemini</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("###  Configuration")
        
        if GOOGLE_API_KEY:
            st.success("API Key Configured")
            st.markdown(f"**Selected Model:** `{GEMINI_MODEL}`")
            
            if AVAILABLE_MODELS:
                with st.expander(" Available Models"):
                    for m in AVAILABLE_MODELS:
                        st.write(f"✓ {m}")
            else:
                st.warning(" Could not detect available models")
        else:
            st.error("API Key Missing - Please add GOOGLE_API_KEY to .env")
        
        st.markdown("---")
        st.markdown("###  About")
        st.info("""
        **Gemini Historical Artifact Description** uses advanced AI to analyze artifact images and provide professional archaeological insights.

        Supports analysis of:
        - Pottery & ceramics
        - Sculpture & statues
        - Tools & weapons
        - Jewelry & ornaments
        - Ancient coins
        - Manuscripts & documents
        """)

    # Main content
    col_input, col_preview = st.columns([1, 1], gap="large")

    # Input panel
    with col_input:
        st.markdown("###  Upload & Analyze")
        
        uploaded_file = st.file_uploader(
            "Select Artifact Image",
            type=["jpg", "jpeg", "png"],
            help="Upload JPG, JPEG, or PNG image of your artifact",
        )

        user_notes = st.text_area(
            " Additional Context (Optional)",
            height=120,
            placeholder="Add any known information about the artifact:\n- Provenance (where it was found)\n- Previous analysis\n- Suspected time period\n- Any inscriptions or markings\n- Cultural context",
            help="Providing context helps generate more accurate analysis",
        )

        analyze_button = st.button(
            " Analyze Artifact",
            disabled=uploaded_file is None or not GOOGLE_API_KEY,
            type="primary",
            use_container_width=True,
        )

        # Usage guide
        if uploaded_file is None:
            st.markdown("---")
            st.markdown("####  How It Works")
            st.markdown("""
            1. **Upload Image** - Choose a clear, high-quality image
            2. **Add Context** (Optional) - Any known information
            3. **Click Analyze** - AI generates comprehensive report
            4. **Review Results** - Get professional insights
            """)

    # Preview panel
    with col_preview:
        st.markdown("###  Image Preview")

        if uploaded_file:
            try:
                pil_image = Image.open(uploaded_file).convert("RGB")
                st.image(pil_image, use_column_width=True, caption="Uploaded Artifact")
                
                # Image info
                with st.expander(" Image Details", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Width", f"{pil_image.width}px")
                    with col2:
                        st.metric("Height", f"{pil_image.height}px")
                    with col3:
                        st.metric("Format", pil_image.format or "PNG")
                
            except Exception as e:
                st.error(f" Could not load image: {e}")
                pil_image = None
        else:
            st.info(" Upload an artifact image to get started")
            pil_image = None

    # Results section
    st.markdown("---")
    st.markdown("###  Analysis Results")

    if analyze_button:
        if pil_image is None:
            st.error(" Please upload a valid image.")
        elif not GOOGLE_API_KEY:
            st.error(" GOOGLE_API_KEY not configured. Add it to your .env file.")
        else:
            with st.spinner(" Analyzing artifact with Gemini AI... This may take a moment..."):
                try:
                    result = get_gemini_analysis(user_notes or "", pil_image)
                    
                    st.success(" Analysis Complete!")
                    
                    # Display in expander
                    with st.expander(" Full Artifact Report", expanded=True):
                        st.markdown(result)

                        # Provide a download button for the full markdown report
                        try:
                            st.download_button(
                                label="Download Report",
                                data=result,
                                file_name="artifact_report.md",
                                mime="text/markdown",
                                help="Download the full artifact analysis as a Markdown file",
                            )
                        except Exception:
                            # Fallback: show a note if download button fails for any reason
                            st.info("Download not available in this environment.")
                    
                except Exception as e:
                    error_str = str(e)
                    st.error(f" Analysis failed: {error_str}")
                    st.markdown("#### Troubleshooting:")
                    
                    error_msg = error_str.lower()
                    
                    if "not found" in error_msg or "not supported" in error_msg:
                        st.error("""
                        ** No Compatible Models Available**
                        
                        Your API key doesn't have access to any compatible Gemini models.
                        
                        **Recommended Solutions:**
                        1. **Get a Free API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
                        2. **Use Gemini API**: The free tier includes Gemini models
                        3. **Replace your GOOGLE_API_KEY** in `.env` file with the new key
                        4. **Restart the app** after updating the key
                        
                        **What models are available:**
                        """)
                        if AVAILABLE_MODELS:
                            for m in AVAILABLE_MODELS:
                                st.info(f" {m}")
                        else:
                            st.warning("Could not detect any compatible models with your API key")
                            
                    elif "401" in error_msg or "permission" in error_msg or "unauthorized" in error_msg or "invalid" in error_msg:
                        st.error("""
                        ** Authentication Error**
                        
                        Your API key is invalid, expired, or not authorized.
                        
                        **Solutions:**
                        1. Generate a new API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
                        2. Update `GOOGLE_API_KEY` in your `.env` file
                        3. Remove any extra spaces from the key
                        4. Restart the Streamlit app
                        """)
                    elif "rate limit" in error_msg:
                        st.warning("""
                        ** Rate Limit Exceeded**
                        
                        You've exceeded your API rate limits.
                        
                        **Solutions:**
                        - Wait a few minutes before analyzing another artifact
                        - Upgrade your API plan for higher limits
                        - Check your usage at [Google Cloud Console](https://console.cloud.google.com)
                        """)
                    else:
                        st.markdown(f"""
                        **Error Details:** `{error_str}`
                        
                        **Quick Fixes:**
                        - Verify GOOGLE_API_KEY is correct in `.env`
                        - Check your internet connection
                        - Try with a different image
                        - Ensure the image clearly shows the artifact
                        
                        **Still Not Working?**
                        1. Visit [Google AI Studio](https://aistudio.google.com)
                        2. Get a new API key (free)
                        3. Update it in your `.env` file
                        4. Restart the app
                        """)


# ============================================================
# FOOTER
# ============================================================

def add_footer():
    """Add footer information"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("** Powered By**")
        st.markdown("[Google Gemini AI](https://ai.google.dev/)")
    
    with col2:
        st.markdown("** Built With**")
        st.markdown("[Streamlit](https://streamlit.io/)")
    
    with col3:
        st.markdown("** For**")
        st.markdown("Artifact Research & Analysis")


if __name__ == "__main__":
    main()
    add_footer()
