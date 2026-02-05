📊 Sentiment Analyzer (Groq + Streamlit)

    This project is a simple web-based sentiment analysis application developed using "Streamlit" and the "Groq" large language model. 
    The application allows users to upload text data in multiple formats such as JSON, TXT, CSV, and PDF, and automatically classifies each input into positive, negative, or neutral sentiment categories.
    The system processes inputs in batches and uses Groq’s LLM to generate structured sentiment outputs. Results are grouped and displayed in a clean Streamlit interface, making it easy to understand overall sentiment distribution.

📁 Project Files

    * app.py – Main application file containing Streamlit UI and Groq sentiment logic.
    * requirements.txt – Lists all Python libraries required for the project.
    * .gitignore – Prevents sensitive files like ".env" and cache folders from being uploaded to GitHub.

✨ Key Features

    * Supports JSON, TXT, CSV, and PDF uploads
    * Batch-based sentiment processing
    * Uses Groq LLM for classification
    * Displays grouped sentiment results
    * Simple and beginner-friendly Streamlit interface
    * Secure API handling using environment variables

🔐 Security
    
     The Groq API key is stored in a `.env` file and excluded from GitHub using `.gitignore`, ensuring sensitive credentials remain private.

🎯 Purpose
     
      This project demonstrates how modern LLM APIs can be integrated with Streamlit to build practical NLP applications such as sentiment analysis, making it suitable for learning, mini-projects, and academic demonstrations.




