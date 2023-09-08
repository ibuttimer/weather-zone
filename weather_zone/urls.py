"""
URL configuration for weather_zone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#  MIT License
#
#  Copyright (c) 2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

from django.contrib import admin
from django.urls import path, include

from .constants import (
    ADMIN_URL, FORECAST_URL, WARNING_URL, ACCOUNTS_URL, USERS_URL,
    ADDRESSES_URL,
    FORECAST_APP_NAME, WARNING_APP_NAME, BASE_APP_NAME, USER_APP_NAME,
    ADDRESSES_APP_NAME
)

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),

    # urls_auth precedes allauth so that its urls override allauth's
    path(ACCOUNTS_URL, include(f'{USER_APP_NAME}.urls_auth')),
    path(ACCOUNTS_URL, include('allauth.urls')),
    path(USERS_URL, include(f'{USER_APP_NAME}.urls')),
    path(ADDRESSES_URL, include(f'{ADDRESSES_APP_NAME}.urls')),

    path(FORECAST_URL, include(f'{FORECAST_APP_NAME}.urls')),
    path(WARNING_URL, include(f'{WARNING_APP_NAME}.urls')),
    path('', include(f'{BASE_APP_NAME}.urls')),
]
