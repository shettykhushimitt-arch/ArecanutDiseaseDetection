import cv2

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import constant_time_compare
from .forms import RegisterForm
from .models import UserRegister


def index(request):
    return render(request, "index.html")


def register(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        address = request.POST['address']

        if UserRegister.objects.filter(email=email).exists():

            return render(
                request,
                "user/register.html",
                {"msg": "Email already exists"}
            )

        UserRegister.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            password=make_password(password),
            address=address
        )

        return render(
            request,
            "user/register.html",
            {"success": "Registration Successful"}
        )

    return render(request, "user/register.html")


def login(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        try:

            user = UserRegister.objects.get(email=email)
            password_matches = check_password(password, user.password)

            # Upgrade existing plain-text passwords after a successful login.
            if not password_matches and constant_time_compare(user.password, password):
                password_matches = True
                user.password = make_password(password)
                user.save(update_fields=['password'])

            if password_matches:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('dashboard')

            raise UserRegister.DoesNotExist

        except UserRegister.DoesNotExist:

            return render(
                request,
                "user/login.html",
                {"msg":"Invalid Email or Password"}
            )

    return render(request,"user/login.html")


def dashboard(request):

    if "user_id" not in request.session:

        return redirect("login")

    predictions = PredictionHistory.objects.filter(
        user_id=request.session['user_id']
    ).order_by('-prediction_date')

    context = {
        'total_predictions': predictions.count(),
        'healthy_count': predictions.filter(disease_name__icontains='Healthy').count(),
        'diseased_count': predictions.exclude(
            disease_name__icontains='Healthy'
        ).exclude(disease_name='No_Detection').count(),
        'recent_predictions': predictions[:4],
    }

    return render(request, "user/dashboard.html", context)


def logout(request):

    request.session.flush()

    return redirect("index")



from django.shortcuts import render, redirect
from .models import PredictionHistory


def history(request):

    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']

    predictions = PredictionHistory.objects.filter(
        user_id=user_id
    ).order_by('-prediction_date')

    total_predictions = predictions.count()

    healthy_count = predictions.filter(
        disease_name__icontains='Healthy'
    ).count()

    diseased_count = predictions.exclude(
        disease_name__icontains='Healthy'
    ).exclude(disease_name='No_Detection').count()

    if total_predictions > 0:

        total_confidence = 0

        for prediction in predictions:

            if prediction.confidence is not None:
                total_confidence += float(prediction.confidence)

        average_confidence = round(
            total_confidence / total_predictions,
            2
        )

    else:

        average_confidence = 0

    context = {

        'predictions': predictions,

        'total_predictions': total_predictions,

        'healthy_count': healthy_count,

        'diseased_count': diseased_count,

        'average_confidence': average_confidence,

    }

    return render(
        request,
        'user/history.html',
        context
    )


from .forms import ImageUploadForm
from .utils import detect_disease, detect_live_frame, PersonDetectedError
from .models import PredictionHistory

def upload_image(request):

    if 'user_id' not in request.session:
        return redirect('login')

    form=ImageUploadForm()

    if request.method=="POST":

        form=ImageUploadForm(request.POST,
                             request.FILES)

        if form.is_valid():

            obj=form.save(commit=False)

            obj.user=UserRegister.objects.get(
                id=request.session['user_id']
            )

            obj.save()

            return redirect("predict",
                            obj.id)

    return render(request,
                  "user/upload.html",
                  {"form":form})


def live_scan(request):
    if 'user_id' not in request.session:
        return redirect('login')

    return render(request, 'user/live_scan.html')


@require_POST
def live_predict(request):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Please sign in to use live scanning.'}, status=401)

    image = request.FILES.get('image')
    if image is None:
        return JsonResponse({'error': 'No camera frame was received.'}, status=400)

    if image.size > 10 * 1024 * 1024:
        return JsonResponse({'error': 'Camera frame is too large.'}, status=400)

    try:
        disease, confidence, annotated_image = detect_live_frame(image)
        info = DiseaseInformation.objects.filter(disease_name=disease).first()

        if info:
            guidance = {
                'symptoms': info.symptoms,
                'causes': info.causes,
                'prevention': info.prevention,
                'treatment': info.treatment,
            }
        else:
            guidance = get_disease_guidance(disease)

        return JsonResponse({
            'disease': disease,
            'disease_display': 'Unable to identify condition' if disease == 'No_Detection' else disease.replace('_', ' '),
            'confidence': confidence,
            'is_healthy': 'healthy' in disease.lower(),
            'is_no_detection': disease == 'No_Detection',
            'annotated_image': annotated_image,
            'guidance': guidance,
        })
    except (ValueError, cv2.error) as error:
        return JsonResponse({'error': str(error)}, status=400)
    
    
import os
import shutil

from django.conf import settings

from .utils import detect_disease
from .models import PredictionHistory, UserRegister, DiseaseInformation
from .disease_guide import get_disease_guidance


from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404
from .utils import detect_disease



def predict(request, id):

    # Check user login
    if "user_id" not in request.session:
        return redirect("login")

    # Get prediction object
    prediction = get_object_or_404(
        PredictionHistory,
        id=id,
        user_id=request.session['user_id']
    )

    # Run AI prediction
    try:
        disease, confidence, prediction_path, heatmap_path = detect_disease(
            prediction.uploaded_image.path
        )
    except PersonDetectedError as error:
        prediction.uploaded_image.delete(save=False)
        prediction.delete()
        return render(request, 'user/upload.html', {
            'form': ImageUploadForm(),
            'msg': str(error),
        })

    # Save prediction details
    prediction.disease_name = disease
    prediction.confidence = confidence

    # Save prediction image
    if prediction_path and os.path.exists(prediction_path):

        prediction.predicted_image = os.path.relpath(
            prediction_path,
            settings.MEDIA_ROOT
        )

    # Save heatmap image
    if heatmap_path and os.path.exists(heatmap_path):

        prediction.heatmap_image = os.path.relpath(
            heatmap_path,
            settings.MEDIA_ROOT
        )

    # Get disease information
    info = DiseaseInformation.objects.filter(
        disease_name=disease
    ).first()

    if info:
        prediction.symptoms = info.symptoms
        prediction.causes = info.causes
        prediction.prevention = info.prevention
        prediction.treatment = info.treatment
    else:
        guidance = get_disease_guidance(disease)
        prediction.symptoms = guidance['symptoms']
        prediction.causes = guidance['causes']
        prediction.prevention = guidance['prevention']
        prediction.treatment = guidance['treatment']

    # Save to database
    prediction.save()

    return redirect(
        "result",
        prediction.id
    )


def result(request, id):

    if "user_id" not in request.session:
        return redirect("login")

    prediction = get_object_or_404(
        PredictionHistory,
        id=id,
        user_id=request.session['user_id']
    )

    return render(
        request,
        "user/result.html",
        {
            "prediction": prediction
        }
    )


from .disease_data import get_disease_info, normalize_disease_name


def result_symptoms(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    prediction = get_object_or_404(
        PredictionHistory,
        id=id,
        user_id=request.session['user_id']
    )

    info = get_disease_info(prediction.disease_name)

    return render(
        request,
        "user/disease_symptoms.html",
        {
            "prediction": prediction,
            "disease_name": info["canonical_name"],
            "symptoms": info["symptoms"],
            "active_section": "symptoms",
        }
    )


def result_cause(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    prediction = get_object_or_404(
        PredictionHistory,
        id=id,
        user_id=request.session['user_id']
    )

    info = get_disease_info(prediction.disease_name)

    return render(
        request,
        "user/disease_cause.html",
        {
            "prediction": prediction,
            "disease_name": info["canonical_name"],
            "causes": info["cause"],
            "active_section": "cause",
        }
    )


def result_prevention(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    prediction = get_object_or_404(
        PredictionHistory,
        id=id,
        user_id=request.session['user_id']
    )

    info = get_disease_info(prediction.disease_name)

    return render(
        request,
        "user/disease_prevention.html",
        {
            "prediction": prediction,
            "disease_name": info["canonical_name"],
            "prevention": info["prevention"],
            "active_section": "prevention",
        }
    )


def result_treatment(request, id):
    if "user_id" not in request.session:
        return redirect("login")

    prediction = get_object_or_404(
        PredictionHistory,
        id=id,
        user_id=request.session['user_id']
    )

    info = get_disease_info(prediction.disease_name)

    return render(
        request,
        "user/disease_treatment.html",
        {
            "prediction": prediction,
            "disease_name": info["canonical_name"],
            "treatment": info["treatment"],
            "active_section": "treatment",
        }
    )