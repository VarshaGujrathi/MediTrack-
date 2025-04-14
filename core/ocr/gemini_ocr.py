import google.generativeai as genai
import os

# ✅ Configure Gemini API Key
genai.configure(api_key="AIzaSyDuK6VF2MBYu2lUPXrJVqpVWUKO658jIPk")  # Replace with your actual API key

# ✅ Upload image to Gemini
def upload_file(path, mime_type="image/jpeg"):
    file = genai.upload_file(path, mime_type=mime_type)
    return file

# ✅ Extract medicine names with dosages
def extract_medicines_from_image(image_path):
    uploaded_file = upload_file(image_path)

    prompt = """
    Extract only the list of medicines along with their strength or dosage units (e.g., mg, IU, ml, or just numeric values) from this prescription image.
    Each medicine should be listed in the format:

    * Medicine Name Dosage

    Example:
    * UROMAX 0.4
    * CAVINTON 5 mg
    """

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    response = model.generate_content([uploaded_file, prompt])
    return response.text
