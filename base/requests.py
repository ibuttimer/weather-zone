"""
Requests related functions
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
import platform

from django.conf import settings

from weather_zone.constants import APP_NAME

from .app_info import get_version


_USER_AGENT = None


def get_user_agent():
    """
    Get the user agent string
    :return: User agent string
    """
    global _USER_AGENT
    if _USER_AGENT is None:
        uname = platform.uname()

        _USER_AGENT = (f"{APP_NAME}/{get_version()} "
                       f"({uname.system}; {uname.version}; {uname.machine})")

    return _USER_AGENT


def get_request_headers():
    """
    Get the request headers
    :return: Request headers
    """
    return {
        'User-Agent': get_user_agent(),
        'Accept': '*/*',
    }
