The Met Éireann API is based on a package originally developed by Met Norway.

[legends.json](legends.json) is the base file downloaded from https://api.met.no/weatherapi/weathericon/2.0/legends.
[me-legends.json](me-legends.json) is the patch file used to apply the Met Éireann specific changes to the base file.

Differences applied by the patch file:
- Alternative names for some of the icons; e.g. Met Norway `clearsky` is also known as Met Éireann `sun`.
- Additional of night specific icons; e.g. Met Éireann `dark_lightcloud` is a night specific icon for Met Norway `fair`.

    The `old_id` field of all `dark_xxx` variants is set to the base old_id value plus 100.    


Please see [The Met Éireann Location Forecast API](https://www.met.ie/Open_Data/Notes-on-API-XML-file_V6.odt) and [met-eireann-weather-forecast-api](https://data.gov.ie/dataset/met-eireann-weather-forecast-api) for more information.