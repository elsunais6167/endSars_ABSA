from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout

from django.contrib import messages


import joblib
import logging

#forms
from .forms import RegisterForm
from .forms import AdminForm
from .forms import IncidenceForm

#database models
from .models import CustomUser
from .models import Incidence
from .models import KnowledgeCategory
from .models import KnowledgeComment
from .models import ExpertKnowledge


# Load the saved CountVectorizer
cVec = joblib.load('count_vectorizer.joblib')

# Load the saved TfidfVectorizer
tVec = joblib.load('tfidf_vectorizer.joblib')
# Create your views here.

# Set up logging
logger = logging.getLogger(__name__)

def load_model(path):
    try:
        return joblib.load(path)
    except Exception as e:
        logger.error(f"Failed to load model {path}: {str(e)}")
        return None
    
def index(request):
    '''
    stations_map = Station.objects.all()
    markers = []

    for station in stations_map:
        patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
        positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

        lat, lon = map(float, station.gis_location.split(','))
        station_url = f"/sta-public/{station.id}/"
        popup_content = f"""
        <a href="{station_url}"> <strong>{station.name}</strong> </a>  <br>
        Total Malaria Test: {patients_count} <br>
        Positive Cases: {positive_cases} <br>
        """  
        markers.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    
    campaign_map = Campaign.objects.all()
    
    markers2 = []
    for campaign in campaign_map:
        s1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_female=Sum('screened_female'))['total_screened_female']
        t1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_female=Sum('treated_female'))['total_treated_female']
        r1= CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_female=Sum('referral_female'))['total_referral_female']

        s2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_male=Sum('screened_male'))['total_screened_male']
        t2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_male=Sum('treated_male'))['total_treated_male']
        r2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_male=Sum('referral_male'))['total_referral_male']
        
        screened_count = s1 + s2
        treated_cases = t1 + t2
        refer_cases = r1 + r2
        
        lat, lon = map(float, campaign.gis_location.split(','))

        campaign_url = f"/camp-public/{campaign.id}/"
        popup_content = f"""
        <a href="{campaign_url}"> <strong>{campaign.name}</strong> </a>  <br>
        Total Screened: {screened_count} <br>
        Total Treated: {treated_cases} <br>
        Total Referral: {refer_cases} <br>
        """  
        markers2.append({
            'location': [lat, lon],
            'popup': popup_content
        })
        '''
    context = {
        #'markers_json': json.dumps(markers),
        #'markers_json2': json.dumps(markers2),
    }
    
    return render(request, 'index.html', context)

def hub(request):
    '''
    stations_map = Station.objects.all()
    markers = []

    for station in stations_map:
        patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
        positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

        lat, lon = map(float, station.gis_location.split(','))
        station_url = f"/sta-public/{station.id}/"
        popup_content = f"""
        <a href="{station_url}"> <strong>{station.name}</strong> </a>  <br>
        Total Malaria Test: {patients_count} <br>
        Positive Cases: {positive_cases} <br>
        """  
        markers.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    
    campaign_map = Campaign.objects.all()
    
    markers2 = []
    for campaign in campaign_map:
        s1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_female=Sum('screened_female'))['total_screened_female']
        t1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_female=Sum('treated_female'))['total_treated_female']
        r1= CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_female=Sum('referral_female'))['total_referral_female']

        s2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_male=Sum('screened_male'))['total_screened_male']
        t2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_male=Sum('treated_male'))['total_treated_male']
        r2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_male=Sum('referral_male'))['total_referral_male']
        
        screened_count = s1 + s2
        treated_cases = t1 + t2
        refer_cases = r1 + r2
        
        lat, lon = map(float, campaign.gis_location.split(','))

        campaign_url = f"/camp-public/{campaign.id}/"
        popup_content = f"""
        <a href="{campaign_url}"> <strong>{campaign.name}</strong> </a>  <br>
        Total Screened: {screened_count} <br>
        Total Treated: {treated_cases} <br>
        Total Referral: {refer_cases} <br>
        """  
        markers2.append({
            'location': [lat, lon],
            'popup': popup_content
        })
        '''
    context = {
        #'markers_json': json.dumps(markers),
        #'markers_json2': json.dumps(markers2),
    }
    
    return render(request, 'hub.html', context)

def reports_list(request):
    '''
    stations_map = Station.objects.all()
    markers = []

    for station in stations_map:
        patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
        positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

        lat, lon = map(float, station.gis_location.split(','))
        station_url = f"/sta-public/{station.id}/"
        popup_content = f"""
        <a href="{station_url}"> <strong>{station.name}</strong> </a>  <br>
        Total Malaria Test: {patients_count} <br>
        Positive Cases: {positive_cases} <br>
        """  
        markers.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    
    campaign_map = Campaign.objects.all()
    
    markers2 = []
    for campaign in campaign_map:
        s1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_female=Sum('screened_female'))['total_screened_female']
        t1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_female=Sum('treated_female'))['total_treated_female']
        r1= CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_female=Sum('referral_female'))['total_referral_female']

        s2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_male=Sum('screened_male'))['total_screened_male']
        t2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_male=Sum('treated_male'))['total_treated_male']
        r2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_male=Sum('referral_male'))['total_referral_male']
        
        screened_count = s1 + s2
        treated_cases = t1 + t2
        refer_cases = r1 + r2
        
        lat, lon = map(float, campaign.gis_location.split(','))

        campaign_url = f"/camp-public/{campaign.id}/"
        popup_content = f"""
        <a href="{campaign_url}"> <strong>{campaign.name}</strong> </a>  <br>
        Total Screened: {screened_count} <br>
        Total Treated: {treated_cases} <br>
        Total Referral: {refer_cases} <br>
        """  
        markers2.append({
            'location': [lat, lon],
            'popup': popup_content
        })
        '''
    context = {
        #'markers_json': json.dumps(markers),
        #'markers_json2': json.dumps(markers2),
    }
    
    return render(request, 'reports.html', context)

def signin(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                user_role = user.role 
                if user_role == 'Admin':
                    return redirect('admin-dashboard')
                elif user_role == 'Reporter':
                    return redirect('admin-cop')
                else:
                    context['error_message'] = 'Contact the administrator for a designated role.'
            except: 
                context['error_message'] = 'Dashboard Error'
        else:
            context['login_error'] = 'Invalid credentials.'

    return render(request, 'login.html', context)

def loggingout(request):
    auth_logout(request)
    return redirect('login')

def Register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.role = 'Reporter'
            form.save()
            return redirect('login')
    
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)

def admin_dasboard(request):
    '''
    stations_map = Station.objects.all()
    markers = []

    for station in stations_map:
        patients_count = Diagnosis.objects.filter(patient_id__care_centre=station).count()
        positive_cases = Diagnosis.objects.filter(patient_id__care_centre=station, results='Positive').count()

        lat, lon = map(float, station.gis_location.split(','))
        station_url = f"/sta-public/{station.id}/"
        popup_content = f"""
        <a href="{station_url}"> <strong>{station.name}</strong> </a>  <br>
        Total Malaria Test: {patients_count} <br>
        Positive Cases: {positive_cases} <br>
        """  
        markers.append({
            'location': [lat, lon],
            'popup': popup_content
        })

    
    campaign_map = Campaign.objects.all()
    
    markers2 = []
    for campaign in campaign_map:
        s1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_female=Sum('screened_female'))['total_screened_female']
        t1 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_female=Sum('treated_female'))['total_treated_female']
        r1= CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_female=Sum('referral_female'))['total_referral_female']

        s2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_screened_male=Sum('screened_male'))['total_screened_male']
        t2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_treated_male=Sum('treated_male'))['total_treated_male']
        r2 = CampReport.objects.filter(campaign_id=campaign).aggregate(total_referral_male=Sum('referral_male'))['total_referral_male']
        
        screened_count = s1 + s2
        treated_cases = t1 + t2
        refer_cases = r1 + r2
        
        lat, lon = map(float, campaign.gis_location.split(','))

        campaign_url = f"/camp-public/{campaign.id}/"
        popup_content = f"""
        <a href="{campaign_url}"> <strong>{campaign.name}</strong> </a>  <br>
        Total Screened: {screened_count} <br>
        Total Treated: {treated_cases} <br>
        Total Referral: {refer_cases} <br>
        """  
        markers2.append({
            'location': [lat, lon],
            'popup': popup_content
        })
        '''
    context = {
        #'markers_json': json.dumps(markers),
        #'markers_json2': json.dumps(markers2),
    }
    
    return render(request, 'admin-dash.html', context)

def admin_reports(request):
    reports = Incidence.objects.all()
    total_reports = Incidence.objects.count()
    user = request.user

    form = IncidenceForm()
    if request.method == "POST":
        form = IncidenceForm(request.POST)
        if form.is_valid():
            incidence = form.save(commit=False)
            incidence.user = user
            content = form.cleaned_data['content']

            

            # Apply vectorizers to the content
            cVec_content = cVec.transform([content])  # Use list to transform a single document
            tVec_content = tVec.transform([content])

            # Paths to the models
            model_paths = {
                'Decision Tree with Count Vectorizer': 'D3CV.joblib',
                'Decision Tree with TFIDF': 'D3TFIDF.joblib',
                'Random Forest with Count Vectorizer': 'RFCV.joblib',
                'Random Forest with TFIDF': 'RFTFIDF.joblib',
                'Logistic Regression with Count Vectorizer': 'LRCV.joblib',
                'Logistic Regression with TFIDF': 'LRTFIDF.joblib',
                'Naive Bayes with Count Vectorizer': 'NBCV.joblib',
                'Naive Bayes with TFIDF': 'NBTFIDF.joblib',
                'Support Vector Machine with Count Vectorizer': 'SVMCV.joblib',
                'Support Vector Machine with TFIDF': 'SVMTFIDF.joblib',
            }

            predictions = {}
            prediction_scores = {}

            for model_name, model_path in model_paths.items():
                model = load_model(model_path)
                if model:
                    try:
                        if 'Count Vectorizer' in model_name:
                            transformed_content = cVec_content
                        else:
                            transformed_content = tVec_content

                        predictions[model_name] = model.predict(transformed_content)[0]
                        prediction_scores[model_name] = max(model.predict_proba(transformed_content)[0])
                    except AttributeError as e:
                        logger.error(f"Error with model {model_name}: {str(e)}")
                    except Exception as e:
                        logger.error(f"General error with model {model_name}: {str(e)}")

            # Find the best model and its corresponding score
            if prediction_scores:
                best_model = max(prediction_scores, key=prediction_scores.get)
                best_score = prediction_scores[best_model]
                best_sentiment = predictions[best_model]

                # Save to the Incidence instance
                incidence.model = best_model
                incidence.percentage = f"{best_score * 100:.2f}%"  # Convert to percentage
                incidence.status = best_sentiment

                # Save the incidence record
                incidence.save()

            return redirect('admin-reports')

    else:
        form = IncidenceForm()

    context = {
        'form': form,
    }
    
    return render(request, 'admin-reports.html', context)

def admin_hub(request):
    
    context = {
        
    }
    
    return render(request, 'admin-dash.html', context)

def admin_users(request):
    user_list = CustomUser.objects.all()
    total_users = CustomUser.objects.count()
    total_reporters = CustomUser.objects.filter(role = 'Reporter').count()
    total_admins = CustomUser.objects.filter(role = 'Admin').count()

    form = AdminForm()
    if request.method == "POST":
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-users')
    
    else:
        form = AdminForm()

    context = {
        'user_list': user_list,
        'total_users': total_users,
        'total_reporters': total_reporters,
        'total_admins': total_admins,
        'form': form,
    }
    
    return render(request, 'admin-users.html', context)