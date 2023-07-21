"""
Constants for the weather_zone package
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
from utils import append_slash

APP_NAME = "Weather-Zone"
COPYRIGHT_YEAR = 2023
COPYRIGHT = "Ian Buttimer"

# Namespace related
BASE_APP_NAME = "base"
FORECAST_APP_NAME = "forecast"
MET_EIREANN_APP_NAME = "met_eireann"

# Base routes related
HOME_URL = "/"
HELP_URL = append_slash("help")
ABOUT_URL = append_slash("about")
PRIVACY_URL = append_slash("privacy")
ROBOTS_URL = "robots.txt"
SITEMAP_URL = "sitemap.xml"

HOME_ROUTE_NAME = "home"
HELP_ROUTE_NAME = "help"
ABOUT_ROUTE_NAME = "about"
PRIVACY_ROUTE_NAME = "privacy"
ROBOTS_ROUTE_NAME = "robots.txt"

# Admin routes related
ADMIN_URL = append_slash("admin")

# Forecast routes related
FORECAST_URL = append_slash("forecast")

# context related
HOME_MENU_CTX = "home_menu"
HELP_MENU_CTX = "help_menu"
ABOUT_MENU_CTX = "about_menu"

IS_SUPER_CTX = "is_super"
IS_DEVELOPMENT_CTX = "is_development"
IS_TEST_CTX = "is_test"
NO_ROBOTS_CTX = "no_robots"
