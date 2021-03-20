[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
# German RKI Corona Homeassistant Sensor
Gets the latest corona stats from RKI (Robert Koch Institut) API for an given district.

<p align="center">
  <img src=images/stats.png>
</p>


## Installation
### 1. Using HACS (recommended)

Open your HACS Settings and add

    https://github.com/FaserF/homeassistant-rki-corona-stats

as custom repository URL.

Then install the "RKI Corona Stats" integration.

If you use this method, your component will always update to the latest version.

### 2. Manual
Place a copy of:

[`__init__.py`](custom_components/rki_corona_stats/__init__.py) at `<config>/custom_components/rki_corona_stats/__init__.py`  
[`sensor.py`](custom_components/rki_corona_stats/sensor.py) at `<config>/custom_components/rki_corona_stats/sensor.py`  
[`manifest.json`](custom_components/rki_corona_stats/manifest.json) at `<config>/custom_components/rki_corona_stats/manifest.json`
and so on, with every other file

where `<config>` is your Home Assistant configuration directory.

>__NOTE__: Do not download the file by using the link above directly. Rather, click on it, then on the page that comes up use the `Raw` button.

## Configuration
Follow the installation instructions above. <br /> 
Then add the desired configuration via Settings -> Integrations -> RKI Corona Stats integration. <br /> 
Then enter your district. It will most likely begin with LK (Landkreis) or SK (Stadtkreis). Example "SK München".<br /> 

## Better Looking custom entity-row

For a better look-and-feel you'll need to install [lovelace-multiple-entity-row](https://github.com/benct/lovelace-multiple-entity-row) (available on HACS), create a bunch of sensors and then use a configuration similar to this for each sensor:

``` yaml
- type: custom:multiple-entity-row
  entity: sensor.rki_corona_stats_yourlocation
  entities:
    - attribute: cases
      name: Cases
    - attribute: deaths
      name: Deaths
    - attribute: incidence
      name: Incidence
  show_state: false
  icon: 'mdi:biohazard'
  name: Stadtkreis München
  secondary_info: last-changed
```

## Thanks to
Big thanks to @knorr3 for his help. <br /> 
Also thanks to RKI for their API.