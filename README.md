## Backend Setup (Django)

Follow these steps to set up the backend server with Django.

### 0. Environment Variables

Create a new file at:
```
/backend/apis/modules/.env
```
Then add the following keys

```
OPENAI_API_KEY=your_openai_api_key
OCR_API_URL=your_naver_ocr_api_url
OCR_SECRET=your_naver_ocr_sk
```

### 1. Create and Activate Virtual Environment

```bash
# Move to backend/
cd ./backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

```

### 2. Install Dependencies

Make sure you have a `requirements.txt` file in the project root. Then install all dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run Django Server

Once dependencies are installed, run database migrations and start the Django development server:

```bash
python manage.py migrate
python manage.py runserver
```


The backend will be available at:  
👉 http://127.0.0.1:8000/

---

## 4. Test API Script (`test_api.py`)

You can use the provided **test_api.py** script to verify all backend APIs — from user registration to OCR and TTS processing.

### 4.1 Run the Test Script

After the Django server is running (`python manage.py runserver`), open a new terminal and run:

```bash
python test_api.py
```

This script will automatically perform the following sequence:

1. **Register a new user** (`/user/register`)
2. **Start a new session** (`/session/start`)
3. **Upload an image for OCR + TTS processing** (`/process/upload/`)
4. **Fetch OCR result** (`/page/get_ocr/`)
5. **Fetch TTS result and save audio files** (`/page/get_tts/` → saved in `./out_audio/`)

---

- To avoid a **409 Conflict** error (when re-registering an already registered device),  
  modify the `DEVICE_INFO` in `test_api.py` before running the test again:

```python
DEVICE_INFO = "test-device-002"  # Change this each run to avoid conflict
```

- Make sure the test image (`sample_page.jpeg`) exists in the same directory as `test_api.py`.

- After running, you can check:
  - OCR results printed in the terminal.
  - TTS audio files saved under `./out_audio/`.

---

