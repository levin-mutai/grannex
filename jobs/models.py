import uuid
from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    id         = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Jobs(BaseModel):
    company      = models.CharField(max_length=200)
    location     = models.CharField(max_length=200)
    url          = models.URLField()
    application_deadline   = models.DateField()
    description  = models.TextField()
    title        = models.CharField(max_length=200)
    category     = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ['created_at']
        get_latest_by = 'created_at'
        indexes = [
            models.Index(fields=['-created_at']),
        ]
      

    def get_applicants(self):
        '''returns a list of all applicants to a job'''
        return self.applicants_set.all()
    
    def get_number_of_applicants(self):
        '''returns the number of applicants who've applied to a given job'''
        return self.applicants_set.count()
    
    def get_by_category(self):
        '''returns jobs of a given category'''
        return self.filter(category=self.category)
    
def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(('File must be a PDF.'))

class Applicants(BaseModel):
    status = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('withdrawn', 'withdrawn'),
    )

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    phone       = models.CharField(max_length=200)
    resume      = models.FileField(upload_to="resumes",validators=[validate_pdf])
    cover_letter= models.TextField()
    job         = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    status      = models.CharField(max_length=200, choices=status, default='pending')

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"
        ordering = ['created_at']
        get_latest_by = 'created_at'
        indexes = [
            models.Index(fields=['-created_at']),
        ]

