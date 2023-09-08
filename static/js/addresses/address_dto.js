/*
 * MIT License
 *
 * Copyright (c) 2023 Ian Buttimer
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

const addressDefaultLinkClass = "a--addr-dflt";
const addressDeleteLinkClass = "a--addr-del";
const addressEditLinkClass = "a--addr-edit";
const addressCardClasses = [addressDefaultLinkClass, addressDeleteLinkClass, addressEditLinkClass];
const addressDefaultLinkSelector = `a[class*='${addressDefaultLinkClass}']`;

$(document).ready(function () {
    /* Handler for new address */
    $(ADD_ADDRESS_SELECTOR).on('click', function (event) {
        document.location.href = ADD_ADDRESS_URL;
        event.preventDefault();
        event.stopPropagation();
    });

    /* Handler for address */
    $(ADDRESS_CARD_SELECTOR).on('click', function (event) {
        let cardLink = false;
        for (let cls of addressCardClasses) {
            cardLink = event.target.classList.contains(cls);
            if (cardLink) {
                break;
            }
        }
        if (!cardLink) {
            // redirect to forecast page
            const addressId = event.currentTarget.id.split('-');
            document.location.href = ADDRESS_FORECAST_URL.replace('0', addressId[addressId.length - 1]);

            // event.target.classList.contains('a--addr-edit')
            event.preventDefault();
            event.stopPropagation();
        }
    });

    $(addressDefaultLinkSelector).on('click', function (event) {
        /* Add delete link to delete confirm modal and display it */

        // request make default
        $.ajax({
            method: 'patch',
            // address_dto.html: href of make default 'a' tag
            url: event.currentTarget.attributes['href'].textContent,
            headers: csrfHeader(),
        }).done(function (data) {
            redirectRewriteInfoResponseHandler(data)
        });

        event.preventDefault();
        event.stopPropagation();
    });
});
