from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from django.contrib import messages
from collections import Counter

import joblib
import logging

#forms
from .forms import RegisterForm
from .forms import AdminForm
from .forms import IncidenceForm
from .forms import ExpertForm
from .forms import CommentForm
from .forms import CategoryForm

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
    reports = Incidence.objects.all()
    paginator = Paginator(reports, 4)
    total_report = Incidence.objects.count()
    total_reporters = CustomUser.objects.filter(role='Reporter').count()
    total_content = ExpertKnowledge.objects.count()
    total_postive = Incidence.objects.filter(status='1').count()
    total_negative = Incidence.objects.filter(status='0').count()
    total_fc = Incidence.objects.filter(social_media = 'Facebook').count()
    total_tw = Incidence.objects.filter(social_media = 'Twitter').count()
    total_in = Incidence.objects.filter(social_media = 'Instagram').count()
    total_ln = Incidence.objects.filter(social_media = 'LinkedIn').count()
    total_ot = Incidence.objects.filter(social_media = 'Others').count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reports': reports,
        'total_report': total_report,
        'total_content': total_content,
        'total_positive': total_postive,
        'total_negative': total_negative,
        'total_reporters': total_reporters,
        'total_fc': total_fc,
        'total_tw': total_tw,
        'total_in': total_in,
        'total_ln': total_ln,
        'total_ot': total_ot,
        'page_obj': page_obj,
    }
    
    return render(request, 'index.html', context)

def hub(request):
    category = request.GET.get('category')
    
    
    if category:
        content = ExpertKnowledge.objects.filter(categories__name=category)
    else:
        content = ExpertKnowledge.objects.all()
    
    
    categories = KnowledgeCategory.objects.all()
    context = {
        'content': content,
        'categories': categories,
    }
    
    return render(request, 'hub.html', context)



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
                    return redirect('reporter-dashboard')
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
    reports = Incidence.objects.all()
    paginator = Paginator(reports, 4)
    total_report = Incidence.objects.count()
    total_reporters = CustomUser.objects.filter(role='Reporter').count()
    total_content = ExpertKnowledge.objects.count()
    total_postive = Incidence.objects.filter(status='1').count()
    total_negative = Incidence.objects.filter(status='0').count()
    total_fc = Incidence.objects.filter(social_media = 'Facebook').count()
    total_tw = Incidence.objects.filter(social_media = 'Twitter').count()
    total_in = Incidence.objects.filter(social_media = 'Instagram').count()
    total_ln = Incidence.objects.filter(social_media = 'LinkedIn').count()
    total_ot = Incidence.objects.filter(social_media = 'Others').count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reports': reports,
        'total_report': total_report,
        'total_content': total_content,
        'total_positive': total_postive,
        'total_negative': total_negative,
        'total_reporters': total_reporters,
        'total_fc': total_fc,
        'total_tw': total_tw,
        'total_in': total_in,
        'total_ln': total_ln,
        'total_ot': total_ot,
        'page_obj': page_obj,
    }
    
    return render(request, 'admin-dash.html', context)


def admin_reports(request):
    reports = Incidence.objects.all()
    total_reports = Incidence.objects.count()
    user = request.user
    user_reports = Incidence.objects.filter(user_id=user).count()

    form = IncidenceForm()
    if request.method == "POST":
        form = IncidenceForm(request.POST)
        if form.is_valid():
            incidence = form.save(commit=False)
            incidence.user = user
            content = form.cleaned_data['content']

            # Apply vectorizers to the content
            cVec_content = cVec.transform([content])
            tVec_content = tVec.transform([content])

            # Load models
            model_paths = {
                'Decision Tree with Count Vectorizer': 'D3CV.joblib',
                'Decision Tree with TFIDF': 'D3TFIDF.joblib',
                'Random Forest with Count Vectorizer': 'RFCV.joblib',
                'Random Forest with TFIDF': 'RFTFIDF.joblib',
                'Logistic Regression with Count Vectorizer': 'LRCV.joblib',
                'Logistic Regression with TFIDF': 'LRTFIDF.joblib',
                'Naive Bayes with Count Vectorizer': 'NBCV.joblib',
                'Naive Bayes with TFIDF': 'NBTFIDF.joblib',
            }

            predictions = []
            model_predictions = {}
            prediction_scores = {}

            for model_name, model_path in model_paths.items():
                model = load_model(model_path)
                if model:
                    try:
                        if 'Count Vectorizer' in model_name:
                            transformed_content = cVec_content
                        else:
                            transformed_content = tVec_content

                        predicted_sentiment = model.predict(transformed_content)[0]
                        predicted_score = max(model.predict_proba(transformed_content)[0])

                        predictions.append(predicted_sentiment)
                        model_predictions[model_name] = predicted_sentiment
                        prediction_scores[model_name] = predicted_score
                    except AttributeError as e:
                        logger.error(f"Error with model {model_name}: {str(e)}")
                    except Exception as e:
                        logger.error(f"General error with model {model_name}: {str(e)}")

            # Apply voting mechanism
            if predictions:
                # Find the most common prediction
                most_common_sentiment, _ = Counter(predictions).most_common(1)[0]

                # Filter models that made the most common prediction and calculate the average score
                total_score = 0
                count = 0
                for model_name, sentiment in model_predictions.items():
                    if sentiment == most_common_sentiment:
                        total_score += prediction_scores[model_name]
                        count += 1

                # Calculate the average score
                if count > 0:
                    average_score = total_score / count

                    # Save the results to the Incidence instance
                    incidence.model = 'Ensemble Model'
                    incidence.percentage = f"{average_score * 100:.2f}%"
                    incidence.status = most_common_sentiment

                    # Save the incidence record
                    incidence.save()

            return redirect('admin-reports')

    else:
        form = IncidenceForm()

    context = {
        'form': form,
        'reports': reports,
        'total_reports': total_reports,
        'user_reports': user_reports,
    }

    return render(request, 'admin-reports.html', context)



def admin_hub(request):
    user = request.user
    content = ExpertKnowledge.objects.all()
    total_content = ExpertKnowledge.objects.count()
    my_content = ExpertKnowledge.objects.filter(expert=user).count()

    form = ExpertForm()
    form2 = CategoryForm()

    if request.method == "POST":
        if 'submit_expert_form' in request.POST:
            form = ExpertForm(request.POST)
            if form.is_valid():
                expert_knowledge = form.save(commit=False)
                expert_knowledge.expert = user
                expert_knowledge.save()
                form.save_m2m() 
                return redirect('admin-hub')

        elif 'submit_category_form' in request.POST:
            form2 = CategoryForm(request.POST)
            if form2.is_valid():
                form2.save()
                return redirect('admin-hub')

    context = {
        'form': form,
        'form2': form2,
        'content': content,
        'total_content': total_content,
        'my_content': my_content,
    }
    
    return render(request, 'admin-hub.html', context)

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

def content(request, pk):
    post = get_object_or_404(ExpertKnowledge, pk=pk)
    form = ExpertForm()
    if request.method == "POST":
        form = ExpertForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin-hub')
    
    else:
        form = ExpertForm(instance=post)

    is_creator = request.user == post.expert

    context = {
        'form': form,
        'post': post,
        'is_creator': is_creator,
    }
    
    return render(request, 'content.html', context)

def reporter_dasboard(request):
    reports = Incidence.objects.all()
    paginator = Paginator(reports, 4)
    total_report = Incidence.objects.count()
    total_reporters = CustomUser.objects.filter(role='Reporter').count()
    total_content = ExpertKnowledge.objects.count()
    total_postive = Incidence.objects.filter(status='1').count()
    total_negative = Incidence.objects.filter(status='0').count()
    total_fc = Incidence.objects.filter(social_media = 'Facebook').count()
    total_tw = Incidence.objects.filter(social_media = 'Twitter').count()
    total_in = Incidence.objects.filter(social_media = 'Instagram').count()
    total_ln = Incidence.objects.filter(social_media = 'LinkedIn').count()
    total_ot = Incidence.objects.filter(social_media = 'Others').count()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reports': reports,
        'total_report': total_report,
        'total_content': total_content,
        'total_positive': total_postive,
        'total_negative': total_negative,
        'total_reporters': total_reporters,
        'total_fc': total_fc,
        'total_tw': total_tw,
        'total_in': total_in,
        'total_ln': total_ln,
        'total_ot': total_ot,
        'page_obj': page_obj,
    }
    
    return render(request, 'reporter-dash.html', context)


def reporter_reports(request):
    user = request.user
    reports = Incidence.objects.filter(user_id=user)
    total_reports = Incidence.objects.count()
    user_reports = Incidence.objects.filter(user_id=user).count()

    form = IncidenceForm()
    if request.method == "POST":
        form = IncidenceForm(request.POST)
        if form.is_valid():
            incidence = form.save(commit=False)
            incidence.user = user
            content = form.cleaned_data['content']

            # Apply vectorizers to the content
            cVec_content = cVec.transform([content])
            tVec_content = tVec.transform([content])

            # Load models
            model_paths = {
                'Decision Tree with Count Vectorizer': 'D3CV.joblib',
                'Decision Tree with TFIDF': 'D3TFIDF.joblib',
                'Random Forest with Count Vectorizer': 'RFCV.joblib',
                'Random Forest with TFIDF': 'RFTFIDF.joblib',
                'Logistic Regression with Count Vectorizer': 'LRCV.joblib',
                'Logistic Regression with TFIDF': 'LRTFIDF.joblib',
                'Naive Bayes with Count Vectorizer': 'NBCV.joblib',
                'Naive Bayes with TFIDF': 'NBTFIDF.joblib',
            }

            predictions = []
            model_predictions = {}
            prediction_scores = {}

            for model_name, model_path in model_paths.items():
                model = load_model(model_path)
                if model:
                    try:
                        if 'Count Vectorizer' in model_name:
                            transformed_content = cVec_content
                        else:
                            transformed_content = tVec_content

                        predicted_sentiment = model.predict(transformed_content)[0]
                        predicted_score = max(model.predict_proba(transformed_content)[0])

                        predictions.append(predicted_sentiment)
                        model_predictions[model_name] = predicted_sentiment
                        prediction_scores[model_name] = predicted_score
                    except AttributeError as e:
                        logger.error(f"Error with model {model_name}: {str(e)}")
                    except Exception as e:
                        logger.error(f"General error with model {model_name}: {str(e)}")

            # Apply voting mechanism
            if predictions:
                # Find the most common prediction
                most_common_sentiment, _ = Counter(predictions).most_common(1)[0]

                # Filter models that made the most common prediction and calculate the average score
                total_score = 0
                count = 0
                for model_name, sentiment in model_predictions.items():
                    if sentiment == most_common_sentiment:
                        total_score += prediction_scores[model_name]
                        count += 1

                # Calculate the average score
                if count > 0:
                    average_score = total_score / count

                    # Save the results to the Incidence instance
                    incidence.model = 'Ensemble Model'
                    incidence.percentage = f"{average_score * 100:.2f}%"
                    incidence.status = most_common_sentiment

                    # Save the incidence record
                    incidence.save()

                    # Check if incidence status is "0"
                    if incidence.status == 0:
                        User = get_user_model()
                        admins = User.objects.filter(role='Admin')
                        subject = 'New Negative Incident Reported'
                        message = f"An incident with a Negative status has been reported.\nDetails:\nPost Title: {incidence.title}\nPost Content: {incidence.content}\nPredicted by: {incidence.model}\nwith Percentage of: {incidence.percentage}"
                        from_email = 'rugu@mhinnov8.com.ng'

                        # Send email to all admins
                        recipient_list = [admin.email for admin in admins]
                        send_mail(subject, message, from_email, recipient_list)

            return redirect('reporter-reports')

    else:
        form = IncidenceForm()

    context = {
        'form': form,
        'reports': reports,
        'total_reports': total_reports,
        'user_reports': user_reports,
    }

    return render(request, 'reporter-reports.html', context)



def reporter_hub(request):
    user = request.user
    content = ExpertKnowledge.objects.filter(expert=user)
    total_content = ExpertKnowledge.objects.count()
    my_content = ExpertKnowledge.objects.filter(expert=user).count()

    form = ExpertForm()
    if request.method == "POST":
        form = ExpertForm(request.POST)
        if form.is_valid():
            expert_knowledge = form.save(commit=False)
            expert_knowledge.expert = user
            expert_knowledge.save()
            form.save_m2m() 
            return redirect('reporter-hub')  
    context = {
        'form': form,
        'content': content,
        'total_content': total_content,
        'my_content': my_content,
    }
    
    return render(request, 'reporter-hub.html', context)