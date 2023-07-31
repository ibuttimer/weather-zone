# Locationforecast
[Locationforecast](https://api.met.no/weatherapi/locationforecast/2.0/documentation) is a weather forecast API provided by Met Norway.

The current version is 2.0. (Version 1.9 is deprecated and documentation is unavailable).

One of the main differences between the two version is that Version 2.0 defaults to JSON format for data, while version 1.9 provides information in xml format.
Version 2.0 does provide xml data (with minor changes from Version 1.9) via the `classic` endpoint.  

#### Weather icons
##### Latest version
The latest version of the weather icons are available at [Weathericon 2.0](https://api.met.no/weatherapi/weathericon/2.0/documentation).
The [icons](met-norway/weathericon.tgz) are named according to the `legend` code in the weather forecast.
##### Previous version
The [previous version of the weather icons](https://nrkno.github.io/yr-weather-symbols/), and are named according to the `old_id` in the weather forecast.

#### Weather legends
The legends are available at https://api.met.no/weatherapi/weathericon/2.0/legends

## Met Éireann
The Met Éireann weather forcast API is based on the Version 1.9 of [Locationforecast](https://api.met.no/weatherapi/locationforecast/2.0/documentation).

### API differences
#### Weather Symbol tag
The `symbol` tag is used to provide information about the weather forecast.
##### Met Éireann Symbol tag
The `symbol` tag has the following attributes:
- `id`
 
  The id of the weather symbol. This is a string value.
  **Note:** The id should not be confused with the weather icon 'legend' code. The same weather icon may be used to represent different id's.
- `number`

  The number of the weather symbol. This is a integer value.
  The number is used to reference the weather icon via the `old_id` in the [previous version](#previous-version) of the weather icons.

```xml
<symbol id="Sun" number="1"/>
```

##### Met Norway (Classic) Symbol tag
The `symbol` tag is the same as the one from [Met Éireann Symbol tag](#met-éireann-symbol-tag) with the addition of the following attribute:
- `code`

  The code of the weather symbol. This is a string value.
  The code refers to the name of the image file in the [latest version](#latest-version) of the weather icons,
  the filename being generated with the addition of the appropriate file extension.  

```xml
<symbol id="Sun" number="1" code="clearsky_day"></symbol>
```

#### Weather legends
There differences in the weather legends between the Met Éareann and Met Norway versions of the Locationforcast. 
These difference are applied by the [me-legends.json](../data/locationforecast/me-legends.json) patch file.

Differences applied by the patch file:
- Alternative ids for some of the icons; e.g. Met Norway `clearsky` is also known as Met Éireann `sun`.
- Addition of night specific icons; e.g. Met Éireann `dark_lightcloud` is a night specific icon for Met Norway `fair`.

  The `old_id` field of all `dark_xxx` variants is set to the base old_id value plus 100.

Please see [The Met Éireann Location Forecast API](https://www.met.ie/Open_Data/Notes-on-API-XML-file_V6.odt) and [met-eireann-weather-forecast-api](https://data.gov.ie/dataset/met-eireann-weather-forecast-api) for more information.

[legends.json](../data/locationforecast/legends.json) is the base file downloaded from https://api.met.no/weatherapi/weathericon/2.0/legends.
[me-legends.json](../data/locationforecast/me-legends.json) is the patch file used to apply the Met Éireann specific changes to the base file.
