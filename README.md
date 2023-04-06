# DeepSense App Backend

This is the backend server for the DeepSense app. It uses Flask to serve an API that provides access to machine learning models for emotion detection and for the database files.

## Installation and Setup

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/chamajay/deepsense-backend.git
    ```

2. Download the machine learning models used by the server and put them in the `models/` folder

    emotion-english-distilroberta-base:   
    https://huggingface.co/j-hartmann/emotion-english-distilroberta-base  
    https://drive.google.com/drive/folders/1pcd8XhmnQmAv4uGHfPJ5r12lkk1Rdsng?usp=sharing

    suicidal-text-electra-cj: https://drive.google.com/drive/folders/16ZnDr635ODm2t1QV0L9gUcGqHUX2hDiR?usp=sharing
    
3. Create a virtual environment for the project:

    ```
    python3 -m venv env
    source env/bin/activate
    ``` 
    
4. (Optional) If you're a Linux user you may want to install the pytorch cpu version using following command & comment out the torch, torchaudio and torchvision packages in the requirements.txt before the next step:
    ```
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    ```
    
5. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```
    


5. Start the server

    ```
    python app.py
    ```
