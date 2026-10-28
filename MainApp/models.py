from django.db import models


# -----------------------------
# User Registration
# -----------------------------
class UserRegister(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -----------------------------
# Prediction History
# -----------------------------
class PredictionHistory(models.Model):

    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)

    uploaded_image = models.ImageField(
        upload_to='uploads/',
        max_length=255
    )

    predicted_image = models.ImageField(
        upload_to='predictions/',
        max_length=255,
        blank=True,
        null=True
    )
    
    heatmap_image = models.ImageField(
        upload_to="heatmaps/",
        max_length=500,
        blank=True,
        null=True
    )


    disease_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    confidence = models.FloatField(
        blank=True,
        null=True
    )

    symptoms = models.TextField(
        blank=True,
        null=True
    )

    causes = models.TextField(
        blank=True,
        null=True
    )

    prevention = models.TextField(
        blank=True,
        null=True
    )

    treatment = models.TextField(
        blank=True,
        null=True
    )

    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease_name or "Prediction"

    @property
    def disease_display(self):
        if self.is_no_detection:
            return "Unable to identify condition"
        return (self.disease_name or "Analysis pending").replace("_", " ")

    @property
    def is_healthy(self):
        return "healthy" in (self.disease_name or "").lower() and not self.is_no_detection

    @property
    def is_no_detection(self):
        return self.disease_name == "No_Detection" or (
            self.disease_name == "Healthy" and self.confidence == 0
        )


# -----------------------------
# Disease Information
# -----------------------------
class DiseaseInformation(models.Model):

    disease_name = models.CharField(max_length=100)

    symptoms = models.TextField()

    causes = models.TextField()

    prevention = models.TextField()

    treatment = models.TextField()
    heatmap_image = models.ImageField(
        upload_to="heatmaps/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.disease_name
