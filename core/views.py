from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import difflib
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from django.core.files.storage import FileSystemStorage
from .ocr.gemini_ocr import extract_medicines_from_image # type: ignore




from meditrack import settings

# Home Page View
def home(request):
    return render(request, 'home.html')

# Login Page View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventory')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Features Page View
def features(request):
    return render(request, 'feature.html')

# Inventory Page View
def inventory_view(request):
    dataset_path = r'C:\PROJECT\MediTrack\datasets\inventory.csv'  # Corrected path with 'r'
    
    # Check if dataset exists before loading
    if not os.path.exists(dataset_path):
        return render(request, 'inventory.html', {'error': 'Dataset not found.'})

    data = pd.read_csv(dataset_path)
    medicines = data.to_dict(orient='records')

    return render(request, 'inventory.html', {'medicines': medicines})

# Stock Analysis View
def stock_analysis_view(request):
    return render(request, 'stock_analysis.html')

# Alternate Medicine View
def alternate_medicine_view(request):
    return render(request, 'alternate_medicine.html')

# Upload Prescription View
def upload_prescription_view(request):
    return render(request, 'upload_prescription.html')

# Upload Medicine Image View
def upload_medicine_image_view(request):
    return render(request, 'upload_medicine_image.html')

# Side Effects View
def side_effects_view(request):
    return render(request, 'side_effects.html')

# Dashboard View
def dashboard_view(request):
    return render(request, 'dashboard.html')

def alternate_medicine_view(request):
    medicine_name = None
    alternatives = []

    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name').strip().lower()

        # Load the dataset
        dataset_path = r'C:\PROJECT\MediTrack\datasets\alternate.csv'
        try:
            df = pd.read_csv(dataset_path)

            # Ensure column names are properly stripped
            df.columns = df.columns.str.strip().str.lower()

            # Check if required columns exist
            if 'name' in df.columns:
                # Filter for the medicine
                medicine_data = df[df['name'].str.strip().str.lower() == medicine_name]

                if not medicine_data.empty:
                    # Collect all substitute columns
                    alternatives = medicine_data.iloc[0][['substitute1', 'substitute2', 'substitute3']].dropna().tolist()
                else:
                    return render(request, 'alternate_medicine.html', {'error': 'Medicine not found.'})
            else:
                return render(request, 'alternate_medicine.html', {'error': 'Dataset error: Required columns not found.'})

        except FileNotFoundError:
            return render(request, 'alternate_medicine.html', {'error': 'Dataset file not found. Check the path.'})
        except Exception as e:
            return render(request, 'alternate_medicine.html', {'error': f'Error reading dataset: {e}'})

    return render(request, 'alternate_medicine.html', {
        'medicine': medicine_name.capitalize() if medicine_name else None,
        'alternatives': alternatives
    })
    
    # suggest_medicines
    
# Path to dataset
file_path = os.path.join(settings.BASE_DIR, 'datasets', 'alternate.csv')

def alternate_medicine_view(request):
    medicine = None
    alternatives = []
    error = None

    if request.method == 'POST':
        medicine = request.POST.get('medicine_name', '').strip()

        try:
            df = pd.read_csv(file_path)
            df_match = df[df['name'].str.lower() == medicine.lower()]

            if not df_match.empty:
                row = df_match.iloc[0]
                alternatives = [row.get('substitute1'), row.get('substitute2'), row.get('substitute3')]
                alternatives = [alt for alt in alternatives if pd.notna(alt)]
            else:
                error = "Medicine not found in dataset."

        except FileNotFoundError:
            error = "CSV file not found."

    return render(request, 'alternate_medicine.html', {
        'medicine': medicine,
        'alternatives': alternatives,
        'error': error
    })


def suggest_medicines(request):
    query = request.GET.get('q', '').lower()
    suggestions = []

    try:
        df = pd.read_csv(file_path)
        suggestions = df[df['name'].str.lower().str.contains(query, na=False)]['name'].head(10).tolist()
    except:
        pass

    return JsonResponse({'suggestions': suggestions})

# Side Effects Search View
# Load the side_effect.csv once globally (optional optimization)
side_effect_df = pd.read_csv(r'C:\PROJECT\MediTrack\datasets\side_effect.csv')  # ✅ use raw string
@csrf_exempt # type: ignore
def side_effect_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        # Filter medicine names that start with the typed query (case insensitive)
        matches = side_effect_df[side_effect_df['name'].str.contains(query, case=False, na=False)]
        suggestions = matches['name'].unique()[:10]  # Return only top 10 suggestions
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([], safe=False)

# ------------
def side_effects_view(request):
    medicine_name = None
    side_effects = []

    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name').strip().lower()

        # Load and clean dataset
        dataset_path = r'C:\PROJECT\MediTrack\datasets\side_effect.csv'
        df = pd.read_csv(dataset_path)

        # Search for the medicine using the correct column name
        if 'name' in df.columns and 'side_effects' in df.columns:
            medicine_data = df[df['name'].str.strip().str.lower() == medicine_name]

            if not medicine_data.empty:
                side_effects_text = medicine_data['side_effects'].values[0]
                side_effects = side_effects_text.split(',') if ',' in side_effects_text else [side_effects_text]
            else:
                return render(request, 'side_effects.html', {'error': 'Medicine not found.'})
        else:
            return render(request, 'side_effects.html', {'error': 'Dataset error: Required columns not found.'})

    return render(request, 'side_effects.html', {
        'medicine': medicine_name.capitalize() if medicine_name else None,
        'side_effects': side_effects
    })
# ✅ Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\text\tesseract.exe'

# ------------- prescription --------------
def upload_prescription(request):
    medicines = None
    image_url = None
    error = None

    if request.method == "POST" and request.FILES.get("prescription"):
        uploaded_file = request.FILES["prescription"]
        fs = FileSystemStorage(location="media/")
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        image_url = fs.url(filename)

        try:
            raw_output = extract_medicines_from_image(file_path)
            medicines = [line.strip("* ").strip() for line in raw_output.strip().split("\n") if line.strip()]
        except Exception as e:
            error = f"Failed to process image: {str(e)}"

    return render(request, "upload_prescription.html", {
        "medicines": medicines,
        "image_url": image_url,
        "error": error
    })
def nearby_medical_view(request):
    # Your logic to render the nearby medical page
    return render(request, 'core/nearby_medical.html')