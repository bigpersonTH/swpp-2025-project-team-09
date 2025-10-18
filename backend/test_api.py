import requests
import json
import base64
import os
BASE_URL = "http://127.0.0.1:8000"

def print_response(resp):
    print(f"\n[STATUS] {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
    except Exception:
        print(resp.text)


def test_register_user(device_info, language_preference):
    """Test 1: Register User"""
    url = f"{BASE_URL}/user/register"
    data = {
        "device_info": device_info,
        "language_preference": language_preference
    }
    print("\n--- Register User ---")
    resp = requests.post(url, json=data)
    print_response(resp)
    if resp.status_code == 200:
        return resp.json().get("user_id")
    return None


def test_start_session(user_id, page_index=0):
    """Test 2: Start Session"""
    url = f"{BASE_URL}/session/start"
    data = {
        "user_id": user_id,
        "page_index": page_index
    }
    print("\n--- Start Session ---")
    resp = requests.post(url, json=data)
    print_response(resp)
    if resp.status_code == 200:
        return resp.json().get("session_id")
    return None

def test_process_upload(session_id, lang, image_path):
    """Test 3: OCR + TTS Upload"""
    url = f"{BASE_URL}/process/upload/"
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    data = {
        "session_id": session_id,
        "lang": lang,
        "image_base64": image_b64
    }
    print("\n--- Process Upload ---")
    resp = requests.post(url, json=data)
    #print_response(resp)
    return resp
    
# 4️⃣ OCR Result Retrieval
def test_get_ocr_result(session_id, page_index=0):
    """Test 4: Get OCR Result"""
    url = f"{BASE_URL}/page/get_ocr/"
    params = {
        "session_id": session_id,
        "page_index": page_index
    }
    print("\n--- Get OCR Result ---")
    resp = requests.get(url, params=params)
    print_response(resp)
    return resp

# 5️⃣ TTS Result Retrieval
def test_get_tts_result(session_id, page_index=0):
    """Test 5: Get TTS Result"""
    url = f"{BASE_URL}/page/get_tts/"
    params = {
        "session_id": session_id,
        "page_index": page_index
    }
    print("\n--- Get TTS Result ---")
    resp = requests.get(url, params=params)
    
    try:
        data = resp.json()
        os.makedirs("./out_audio", exist_ok=True)

        audio_results = data.get("audio_results", [])
        for bbox in audio_results:
            bbox_index = bbox.get("bbox_index", 0)
            audio_list = bbox.get("audio_base64_list", [])
            for i, audio_b64 in enumerate(audio_list):
                audio_bytes = base64.b64decode(audio_b64)
                filename = f"./out_audio/tts_{page_index}_{bbox_index}_{i}.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving audio: {e}")

    return resp

if __name__ == "__main__":
    DEVICE_INFO = "test-device-000"
    LANG = "en"

    user_id = test_register_user(DEVICE_INFO, LANG)
    if not user_id:
        print("Registration failed")
        exit()

    session_id = test_start_session(user_id)
    if not session_id:
        print("Session start failed")
        exit()

    IMAGE_PATH = "sample_page.jpeg"  
    LANG = "en"
    resp = test_process_upload(session_id, LANG, IMAGE_PATH)
    if resp.status_code != 200:
        print("Process upload failed")

    # Run OCR + TTS result tests
    print("\n===== Starting OCR / TTS Result Tests =====")
    test_get_ocr_result(session_id)
    test_get_tts_result(session_id)
