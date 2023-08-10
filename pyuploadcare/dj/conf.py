# coding: utf-8

from typing import TypedDict

from django import get_version as django_version
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from pyuploadcare import __version__ as library_version


if not hasattr(settings, "UPLOADCARE"):
    raise ImproperlyConfigured("UPLOADCARE setting must be set")

if "pub_key" not in settings.UPLOADCARE:
    raise ImproperlyConfigured("UPLOADCARE setting must have pub_key")
if "secret" not in settings.UPLOADCARE:
    raise ImproperlyConfigured("UPLOADCARE setting must have secret")


pub_key = settings.UPLOADCARE["pub_key"]
secret = settings.UPLOADCARE["secret"]
user_agent_extension = "Django/{0}; PyUploadcare-Django/{1}".format(
    django_version(), library_version
)

cdn_base = settings.UPLOADCARE.get("cdn_base")

legacy_widget = settings.UPLOADCARE.get("legacy_widget", False)

if legacy_widget:

    widget_version = settings.UPLOADCARE.get("widget_version", "3.x")
    widget_build = settings.UPLOADCARE.get(
        "widget_build", settings.UPLOADCARE.get("widget_variant", "full.min")
    )
    widget_filename_js = "uploadcare.{0}.js".format(widget_build).replace(
        "..", "."
    )
    widget_filename_css = ""
    hosted_url_js = (
        "https://ucarecdn.com/libs/widget/{version}/{filename}".format(
            version=widget_version, filename=widget_filename_js
        )
    )
    hosted_url_css = ""

else:
    widget_version = settings.UPLOADCARE.get("widget_version", "0.25.4")
    widget_build = settings.UPLOADCARE.get(
        "widget_build", settings.UPLOADCARE.get("widget_variant", "regular")
    )
    widget_filename_js = "blocks.min.js"
    widget_filename_css = "lr-file-uploader-{0}.min.css".format(widget_build)
    hosted_url_js = "https://cdn.jsdelivr.net/npm/@uploadcare/blocks@{version}/web/{filename}".format(
        version=widget_version, filename=widget_filename_js
    )
    hosted_url_css = "https://cdn.jsdelivr.net/npm/@uploadcare/blocks@{version}/web/{filename}".format(
        version=widget_version, filename=widget_filename_css
    )


local_url_js = "uploadcare/{filename}".format(filename=widget_filename_js)
local_url_css = "uploadcare/{filename}".format(filename=widget_filename_css)

use_hosted_assets = settings.UPLOADCARE.get("use_hosted_assets", True)

if use_hosted_assets:
    uploadcare_js = hosted_url_js
    uploadcare_css = hosted_url_css
else:
    uploadcare_js = settings.UPLOADCARE.get(
        "widget_url_js", settings.UPLOADCARE.get("widget_url", local_url_js)
    )
    uploadcare_css = settings.UPLOADCARE.get("widget_url_css", local_url_css)

if "widget_url" in settings.UPLOADCARE:
    uploadcare_js = settings.UPLOADCARE["widget_url"]

if "widget_url_js" in settings.UPLOADCARE:
    uploadcare_js = settings.UPLOADCARE["widget_url_js"]

if "widget_url_css" in settings.UPLOADCARE:
    uploadcare_css = settings.UPLOADCARE["widget_url_css"]

upload_base_url = settings.UPLOADCARE.get("upload_base_url")
