"""
Constants for base app
"""
from collections import namedtuple
from enum import Enum
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
from pathlib import Path

from utils import Crud


# name of this app
THIS_APP = Path(__file__).resolve().parent.name

# general context
APP_NAME_CTX = 'app_name'
APP_VERSION_CTX = 'app_version'
REDIRECT_TO_CTX = 'redirect_to'
SET_LANGUAGE_CTX = 'set_language'
LANG_COUNTRY_CTX = 'lang_country'
ARIA_CHANGE_LANG_CTX = 'change_lang'

TITLE_CTX = 'title'
ABOUT_INFO_CTX = 'about_info'
CREDITS_CTX = 'credits'

TITLE_CLASS_CTX = 'title_class'
MODAL_LEVEL_CTX = 'modal_level'

PAGE_HEADING_CTX = 'page_heading'
PAGE_SUB_HEADING_CTX = 'page_sub_heading'

TOAST_POSITION_CTX = 'toast_position'

InfoModalCfg = namedtuple(
    'InfoModalCfg',
    ['name', 'title_class', 'title_text'],
    defaults=['', '', '']
)
"""
Info modal configuration
name: info modal name
title_class: class to apply to title
title_text: title text
"""


class InfoModalLevel(Enum):
    """ Enum representing info modal levels """
    NONE = (0, InfoModalCfg(name='none'))
    DANGER = (1, InfoModalCfg(
        name='danger', title_class='text-danger', title_text='Danger'))
    WARN = (2, InfoModalCfg(
        name='warn', title_class='text-warning', title_text='Warning'))
    INFO = (3, InfoModalCfg(name='info', title_class='text-info'))
    QUESTION = (4, InfoModalCfg(name='question'))


SUBMIT_BTN_TEXT = {
    Crud.CREATE: 'Save',
    Crud.UPDATE: 'Update',
    Crud.DELETE: 'Delete',
    Crud.READ: 'Close',
}
