from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Prediction
from .ml_predictor import get_predictor

def home(request):
    """Landing page view"""
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """Main dashboard for logged-in users"""
    # Get user's recent predictions
    recent_predictions = Prediction.objects.filter(user=request.user)[:5]
    context = {
        'recent_predictions': recent_predictions
    }
    return render(request, 'dashboard.html', context)

@login_required
def predict(request):
    """Prediction form and processing"""
    if request.method == 'POST':
        try:
            # Extract form data
            patient_data = {
                'AGE': float(request.POST.get('AGE')),
                'SEX': int(request.POST.get('SEX')),
                'BMI': float(request.POST.get('BMI')),
                'SP': float(request.POST.get('SP')),
                'BP': float(request.POST.get('BP')),
                'HbA1c': float(request.POST.get('HbA1c')),
                'FPS': float(request.POST.get('FPS')),
                'PPS': float(request.POST.get('PPS')),
                'FAMILY H/O': int(request.POST.get('FAMILY_HO')),
                'ONSET AGE': float(request.POST.get('ONSET_AGE')),
                'DIA LIFE': request.POST.get('DIA_LIFE'),  # String (can be "5" or "6m")
                'SMOKING': int(request.POST.get('SMOKING')),
                'PHY ACT': int(request.POST.get('PHY_ACT')),
                'MED USE': int(request.POST.get('MED_USE')),
                'MED ADH': int(request.POST.get('MED_ADH'))
            }
            
            # Get predictor and make predictions
            predictor = get_predictor()
            predictions = predictor.predict(patient_data)
            
            # Convert DIA LIFE for storage
            dia_life_value = predictor.convert_dia_life(patient_data['DIA LIFE'])
            
            # Save to database
            prediction_record = Prediction.objects.create(
                user=request.user,
                age=patient_data['AGE'],
                sex=patient_data['SEX'],
                bmi=patient_data['BMI'],
                systolic_bp=patient_data['SP'],
                diastolic_bp=patient_data['BP'],
                hba1c=patient_data['HbA1c'],
                fasting_plasma_sugar=patient_data['FPS'],
                postprandial_sugar=patient_data['PPS'],
                family_history=patient_data['FAMILY H/O'],
                onset_age=patient_data['ONSET AGE'],
                diabetes_duration=dia_life_value,
                smoking=patient_data['SMOKING'],
                physical_activity=patient_data['PHY ACT'],
                medication_use=patient_data['MED USE'],
                medication_adherence=patient_data['MED ADH'],
                nephropathy_risk=predictions['NEP'],
                neuropathy_risk=predictions['NEU'],
                retinopathy_risk=predictions['RET']
            )
            
            messages.success(request, 'Prediction completed successfully!')
            return redirect('results', prediction_id=prediction_record.id)
            
        except ValueError as e:
            messages.error(request, f'Invalid input data: {str(e)}')
        except Exception as e:
            messages.error(request, f'An error occurred during prediction: {str(e)}')
            print(f"Prediction error: {e}")
    
    return render(request, 'predict.html')

@login_required
def results(request, prediction_id):
    """Display prediction results"""
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    context = {
        'prediction': prediction,
        'nep_probability': prediction.nephropathy_risk,
        'nep_percentage': round(prediction.nephropathy_risk * 100, 1),
        'neu_probability': prediction.neuropathy_risk,
        'neu_percentage': round(prediction.neuropathy_risk * 100, 1),
        'ret_probability': prediction.retinopathy_risk,
        'ret_percentage': round(prediction.retinopathy_risk * 100, 1),
    }
    
    return render(request, 'results.html', context)