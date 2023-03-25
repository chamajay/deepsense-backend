# DeepSense App Backend

This is the backend server for the DeepSense app. It uses Flask to serve an API that provides access to machine learning models for emotion detection and for the database files.

## Installation and Setup

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/chamajay/deepsense-backend.git
    ```

2. Download the machine learning models used by the server and put them in the `models/` folder

    emotion-english-distilroberta-base: https://huggingface.co/j-hartmann/emotion-english-distilroberta-base

    suicidal-text-electra-cj: https://drive.google.com/drive/folders/16ZnDr635ODm2t1QV0L9gUcGqHUX2hDiR?usp=sharing
    
    
3. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

4. Start the server

    ```
    python app.py
    ```