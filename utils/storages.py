from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.core.files.storage import DefaultStorage

class SupabaseBaseStorage(S3Boto3Storage):
    """
    Base storage class for Supabase S3 using boto3.
    """
    access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
    secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
    endpoint_url = getattr(settings, 'AWS_S3_ENDPOINT_URL', '')
    region_name = getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1')
    
    default_acl = 'public-read'
    file_overwrite = False

def get_storage(bucket_name):
    if getattr(settings, 'AWS_ACCESS_KEY_ID', None) and getattr(settings, 'AWS_SECRET_ACCESS_KEY', None):
        class DynamicStorage(SupabaseBaseStorage):
            bucket_name = bucket_name
        return DynamicStorage()
    return DefaultStorage()

def ProfileImageStorage(): return get_storage('profile-images')
def CourseThumbnailStorage(): return get_storage('course-thumbnails')
def DocumentStorage(): return get_storage('documents')
def AssignmentStorage(): return get_storage('assignments')
def SubmissionStorage(): return get_storage('submissions')
def CertificateStorage(): return get_storage('certificates')
def PublicAssetStorage(): return get_storage('public-assets')
