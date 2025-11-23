# Quick Deployment Guide

## Option 1: Streamlit Cloud (Recommended - Free & Easy)

1. **Prepare Repository:**
   - Create a GitHub repository
   - Upload all files from this project

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select your repository and `app.py`
   
3. **Configure Secrets:**
   - In Streamlit Cloud dashboard, go to app settings
   - Add to "Secrets":
     ```toml
     ANTHROPIC_API_KEY = "your-api-key-here"
     ```
   
4. **Launch:**
   - Click "Deploy"
   - Your app will be live at `https://[your-app-name].streamlit.app`

**Time to deploy: ~5 minutes**

## Option 2: Local Development

```bash
# Clone/download the project
cd document-classification-portal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up secrets
mkdir -p .streamlit
cp secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your API key

# Run the app
streamlit run app.py
```

**Access at:** http://localhost:8501

## Option 3: Other Hosting Platforms

### Hugging Face Spaces
1. Create a new Space with Streamlit SDK
2. Upload files
3. Add `ANTHROPIC_API_KEY` to Space secrets

### Railway / Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.port $PORT`
4. Add environment variable: `ANTHROPIC_API_KEY`

## Getting an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new key
5. Copy and save it securely

## Testing the Application

1. Upload a sample PDF (any document)
2. Click "Classify Document"
3. View results with confidence score
4. Test with different document types

**Note:** The application processes documents in real-time and doesn't store any data.
