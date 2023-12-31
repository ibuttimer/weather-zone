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
from utils.url_path import append_slash, url_path

APP_NAME = "Weather-Zone"
COPYRIGHT_YEAR = 2023
COPYRIGHT = "Ian Buttimer"

# Namespace related
BASE_APP_NAME = "base"
BROKER_APP_NAME = "broker"
FORECAST_APP_NAME = "forecast"
LOCATIONFORECAST_APP_NAME = "locationforecast"
WARNING_APP_NAME = "weather_warning"
USER_APP_NAME = "user"
ADDRESSES_APP_NAME = "addresses"

# Base routes related
HOME_URL = "/"
HELP_URL = append_slash("help")
ABOUT_URL = append_slash("about")
PRIVACY_URL = append_slash("privacy")
LANGUAGE_URL = append_slash("language")
ROBOTS_URL = "robots.txt"
SITEMAP_URL = "sitemap.xml"

HOME_ROUTE_NAME = "home"
HELP_ROUTE_NAME = "help"
ABOUT_ROUTE_NAME = "about"
LANGUAGE_ROUTE_NAME = "language"
PRIVACY_ROUTE_NAME = "privacy"
ROBOTS_ROUTE_NAME = "robots.txt"

# Admin routes related
ADMIN_URL = append_slash("admin")

# Accounts routes related
ACCOUNTS_URL = append_slash("accounts")

# mounting allauth on 'accounts' and copying paths from
# allauth/account/urls.py
LOGIN_URL = url_path(ACCOUNTS_URL, "login")
LOGOUT_URL = url_path(ACCOUNTS_URL, "logout")
REGISTER_URL = url_path(ACCOUNTS_URL, "signup")
# excluding mount prefix as used to override allauth
CHANGE_PASSWORD_URL = url_path("password", "change")
MANAGE_EMAIL_URL = url_path(ACCOUNTS_URL, "email")
# copying route names from allauth/account/urls.py
LOGIN_ROUTE_NAME = "account_login"
LOGOUT_ROUTE_NAME = "account_logout"
REGISTER_ROUTE_NAME = "account_signup"
CHANGE_PASSWORD_ROUTE_NAME = "account_change_password"
MANAGE_EMAIL_ROUTE_NAME = "account_email"

# User routes related
USERS_URL = append_slash("users")

# User routes related
ADDRESSES_URL = append_slash("addresses")

# Forecast routes related
FORECAST_URL = append_slash("forecast")

# Weather warning routes related
WARNING_URL = append_slash("warning")

# context related
HOME_MENU_CTX = "home_menu"
USER_MENU_CTX = "user_menu"
SIGN_IN_MENU_CTX = "sign_in_menu"
REGISTER_MENU_CTX = "register_menu"
HELP_MENU_CTX = "help_menu"
ABOUT_MENU_CTX = "about_menu"

IS_SUPER_CTX = "is_super"
IS_DEVELOPMENT_CTX = "is_development"
IS_TEST_CTX = "is_test"
NO_ROBOTS_CTX = "no_robots"
