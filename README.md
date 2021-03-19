[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
# Corona-in-zahlen.de Homeassistant Sensor
Gets the latest corona stats from corona-in-zahlen.de 
This is currently WIP and will only work for Ebersberg!

<p align="center">
  <img src=images/stats.png>
</p>


Follow the installation instructions below.
Then add the desired configuration via Settings -> Integrations -> corona-in-zahlen.de integration.

## Installation
Pre-requisits:
1. Download this repo as a zip file.
2. Edit the following file at line 21: https://github.com/FaserF/homeassistant-corona-in-zahlen/blob/master/custom_components/corona_in_zahlen/__init__.py#L21
You will find it under custom_components/corona_in_zahlen/__init__.py

And replace "Ebersberg" with your Location.
3. Save the file
4. Then continue with "2. Manual".

### 1. Using HACS (if your location is already supported with this addon)

Open your HACS Settings and add

    https://github.com/FaserF/homeassistant-corona-in-zahlen

as custom repository URL.

Then install the "Corona-in-zahlen.de" integration.

If you use this method, your component will always update to the latest version.

### 2. Manual
Place a copy of:

[`__init__.py`](custom_components/corona_in_zahlen/__init__.py) at `<config>/custom_components/corona_in_zahlen/__init__.py`  
[`sensor.py`](custom_components/corona_in_zahlen/sensor.py) at `<config>/custom_components/corona_in_zahlen/sensor.py`  
[`manifest.json`](custom_components/corona_in_zahlen/manifest.json) at `<config>/custom_components/corona_in_zahlen/manifest.json`
and so on, with every other file

where `<config>` is your Home Assistant configuration directory.

>__NOTE__: Do not download the file by using the link above directly. Rather, click on it, then on the page that comes up use the `Raw` button.

## Configuration variables
- **entity_id**: Choose your location
## Examples

For a better look-and-feel you'll need to install [lovelace-multiple-entity-row](https://github.com/benct/lovelace-multiple-entity-row) (available on HACS), create a bunch of sensors and then use a configuration similar to this for each sensor:

``` yaml
- type: custom:multiple-entity-row
  entity: sensor.corona_stats_yourlocation
  entities:
    - attribute: cases
      name: Cases
    - attribute: deaths
      name: Deaths
    - attribute: incidence
      name: Incidence
  show_state: false
  icon: 'mdi:biohazard'
  name: Hessen
  secondary_info: last-changed
```
