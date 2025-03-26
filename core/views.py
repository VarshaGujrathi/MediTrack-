from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import pandas as pd
import os  # For safe file path handling

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
# Side Effects Search View
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
    