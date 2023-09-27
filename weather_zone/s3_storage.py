"""
AWS S3 storage
based on https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Static file storage
    """
    location = settings.AWS_LOCATION
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
    # Owner gets FULL_CONTROL. The AllUsers group gets READ access.
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    """
    Public media file storage
    """
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """
    Private media file storage
    """
    location = 'private'
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
    # Owner gets FULL_CONTROL. No one else has access rights (default).
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
