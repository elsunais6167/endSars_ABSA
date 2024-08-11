from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout

from django.contrib import messages

from .forms import RegisterForm

# Create your views here.

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
                    return redirect('admin-dash')
                elif user_role == 'COP Desk Officer':
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