/*
 * MIT License
 *
 * Copyright (c) 2022-2023 Ian Buttimer
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *
 */

/**
 * Enable Bootstrap tooltips
 * @param selector - element selector; default all elements
 */
function enableTooltips(selector = undefined) {
    const ttSelector = selector === undefined ? '[data-bs-toggle="tooltip"]' : selector;
    const tooltipTriggerList = document.querySelectorAll(ttSelector);
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

const SHOW_INFO_PROP = 'show_info';
const REDIRECT_PROP = 'redirect';
const REDIRECT_PAUSE_PROP = 'pause';
const REWRITES_PROP = 'rewrites';
const ELEMENT_SELECTOR_PROP = 'element_selector';
const TOOLTIPS_SELECTOR_PROP = 'tooltips_selector';
const HTML_PROP = 'html';
const INNER_HTML_PROP = 'inner_html';
const INFO_TOAST_PROP = 'info_toast';
const TOAST_POSITION_PROP = 'toast_position';

const replaceHtml = (data) => $(data[ELEMENT_SELECTOR_PROP]).replaceWith(data[HTML_PROP]);
const replaceInnerHtml = (data) => $(data[ELEMENT_SELECTOR_PROP]).html(data[INNER_HTML_PROP]);

/**
 * Handle a html/innerHtml replacement
 * :param data: json data
 */
function htmlUpdateHandler(data) {
    if (data !== undefined) {
        if (data.hasOwnProperty(ELEMENT_SELECTOR_PROP)) {
            if (data.hasOwnProperty(HTML_PROP)) {
                // replace single element's html
                replaceHtml(data);
            } else if (data.hasOwnProperty(INNER_HTML_PROP)) {
                // replace single element's inner html
                replaceInnerHtml(data);
            }
        }
        if (data.hasOwnProperty(TOOLTIPS_SELECTOR_PROP)) {
            enableTooltips(data[TOOLTIPS_SELECTOR_PROP]);
        }
    }
}

/**
 * Handle a rewrites replacement
 * :param data: json data
 */
function htmlRewritesHandler(data) {
    if (data !== undefined) {
        // replace multiple element's html
        for (const element of data) {
            if (element.hasOwnProperty(REWRITES_PROP)) {
                // nested rewrites
                htmlRewritesHandler(element[REWRITES_PROP]);
            } else {
                htmlUpdateHandler(element);
            }
        }
    }
}

/**
 * Handle a redirect/rewrite response
 * :param data: json data
 * :return: true if modal/toast was displayed
 */
function redirectRewriteInfoResponseHandler(data) {
    let feedbackDisplayed = false;
    if (data !== undefined) {
        // replace single element html
        htmlUpdateHandler(data);
        if (data.hasOwnProperty(REWRITES_PROP)) {
            // replace multiple element's html
            htmlRewritesHandler(data[REWRITES_PROP])
        }
        if (data.hasOwnProperty(REDIRECT_PROP)) {
            // redirect to new url
            if (data.hasOwnProperty(REDIRECT_PAUSE_PROP)) {
                setTimeout(() => {
                    document.location.href = data[REDIRECT_PROP];
                }, parseInt(data[REDIRECT_PAUSE_PROP]))
            } else {
                document.location.href = data[REDIRECT_PROP];
            }
        }
        if (data.hasOwnProperty(SHOW_INFO_PROP)) {
            // show info modal
            feedbackDisplayed = displayInfoModal(data[SHOW_INFO_PROP]);
        }
        if (data.hasOwnProperty(INFO_TOAST_PROP)) {
            // show info toast
            const position = data.hasOwnProperty(TOAST_POSITION_PROP) ? data[TOAST_POSITION_PROP] : undefined;
            feedbackDisplayed = showInfoToast(data[INFO_TOAST_PROP], position);
        }
        return feedbackDisplayed;
    }
}

/**
 * Add the CSRF header to the specified object
 * @param update - object to update
 * @returns updated object
 */
function csrfHeader(update = undefined) {
    if (update === undefined) {
        update = {}
    }
    return Object.assign(update, {
        'X-CSRFTOKEN': csrfToken()
    });
}


enableTooltips();
