"""
Miscellaneous URL path utilities
"""
#  MIT License
#
#  Copyright (c) 2022-2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#
from urllib.parse import urlencode

from django.urls import reverse as django_reverse


# Request methods
GET = 'GET'
PATCH = 'PATCH'
POST = 'POST'
DELETE = 'DELETE'


def append_slash(url: str) -> str:
    """
    Append a slash to the specified url if necessary.
    (See
    https://docs.djangoproject.com/en/4.1/misc/design-philosophies/#definitive-urls)
    :param url: url string
    :return: updated url string
    """
    result: str = url
    if result[-1] != '/':
        result = f"{url}/"
    return result


def namespaced_url(*args: str) -> str:
    """
    Concatenate supplied arguments into a namespaced URL.
    See https://docs.djangoproject.com/en/4.1/topics/http/urls/#url-namespaces
    :param args: elements of url
    :return: concatenated url string
    """
    return ":".join([arg for arg in args if arg])


def app_template_path(app: str, *args: str) -> str:
    """
    Concatenate supplied arguments into a relative path to a template file
    :param app: name of app
    :param args: elements of path
    :return: concatenated path string
    """
    path = [app]
    path.extend(args)
    return "/".join(path)


def url_path(*args: str) -> str:
    """
    Concatenate arguments into a url path
    :param args: elements of path
    :return: concatenated path string
    """
    return "".join([append_slash(segment) for segment in args if segment])


def reverse_q(viewname, urlconf=None, args=None, kwargs=None,
              current_app=None, query_kwargs: dict = None) -> str:
    """
    Wrapper to add query argument support to django's standard `reverse`
    https://docs.djangoproject.com/en/4.1/topics/http/urls/#url-namespaces
    :param viewname: URL pattern name or the callable view object
    :param urlconf:
            URLconf module containing the URL patterns to use for reversing
    :param args: arguments for url
    :param kwargs: keyword args
    :param current_app: application to which the view belongs
    :param query_kwargs: query arguments
    :return: url str
    """
    url = django_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
                         current_app=current_app)
    if query_kwargs:
        url = f'{url}?{urlencode(query_kwargs)}'
    return url
