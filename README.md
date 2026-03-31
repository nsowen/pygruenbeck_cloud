# pygruenbeck_cloud

<p align="center">
    <a href="https://www.gruenbeck.com/" target="_blank"><img src="https://www.gruenbeck.com/typo3conf/ext/sitepackage_gruenbeck/Resources/Public/Images/gruenbeck-logo.svg" alt="Gruenbeck" /></a>
</p>

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pygruenbeck_cloud?logo=python)
[![PyPI release](https://img.shields.io/pypi/v/pygruenbeck_cloud)](https://pypi.org/project/pygruenbeck_cloud/)
![Release status](https://img.shields.io/pypi/status/pygruenbeck_cloud)
![Build Pipeline](https://img.shields.io/github/actions/workflow/status/p0l0/pygruenbeck_cloud/ci.yml)
[![codecov](https://codecov.io/gh/p0l0/pygruenbeck_cloud/branch/main/graph/badge.svg?token=V5C2O6SK2O)](https://codecov.io/gh/p0l0/pygruenbeck_cloud)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=f8b424)](https://github.com/pre-commit/pre-commit)
![License](https://img.shields.io/github/license/p0l0/pygruenbeck_cloud)

`pygruenbeck_cloud` is a Python 3 (>= 3.12) library to communicate with the Grünbeck Cloud based Water softeners.

It is intended to be used in custom_component [hagruenbeck_cloud](https://github.com/p0l0/hagruenbeck_cloud) for [Home Assistant](https://www.home-assistant.io/).

Implementation is based on the [ioBroker gruenbeck adapter](https://github.com/TA2k/ioBroker.gruenbeck) implementation.

### Supported series

| Series      | Update mechanism | Notes                                                                                   |
|-------------|------------------|-----------------------------------------------------------------------------------------|
| softliQ.SL  | WebSocket (push) |                                                                                         |
| softliQ.SD  | WebSocket (push) |                                                                                         |
| softliQ.SE  | HTTP polling     | Uses a stateless per-poll cycle (`refresh → enter → update → leave → off`) via `poll_sd()`. Do **not** hold a persistent session — the server silently drops it after ~10–15 min. |

### Available realtime data

Realtime data is provided via `DeviceRealtimeInfo` (accessed as `device.realtime`).
SL/SD series receive updates via WebSocket; SE series is polled via `poll_sd()`.

| Attribute                          | Type          | Unit      | Description                                      | Series   |
|------------------------------------|---------------|-----------|--------------------------------------------------|----------|
| `soft_water_quantity`              | int           | l         | Soft water quantity exchanger 1                  | All      |
| `soft_water_quantity_2`            | int           | l         | Soft water quantity exchanger 2                  | SL/SD    |
| `regeneration_counter`             | int           |           | Total regeneration counter                       | All      |
| `current_flow_rate`                | float         | m³/h      | Current flow rate exchanger 1                    | All      |
| `current_flow_rate_2`              | float         | m³/h      | Current flow rate exchanger 2                    | All      |
| `remaining_capacity_volume`        | float         | m³        | Remaining capacity volume exchanger 1            | All      |
| `remaining_capacity_volume_2`      | float         | m³        | Remaining capacity volume exchanger 2            | All      |
| `remaining_capacity_percentage`    | int           | %         | Residual capacity exchanger 1                    | All      |
| `remaining_capacity_percentage_2`  | int           | %         | Residual capacity exchanger 2                    | All      |
| `salt_range`                       | int           | days      | Salt reach (days remaining)                      | All      |
| `salt_consumption`                 | float         | kg        | Total salt consumption                           | All      |
| `next_service`                     | int           | days      | Days until next maintenance                      | SL/SD    |
| `regeneration_remaining_time`      | float         |           | Remaining time/amount of current regen step      | SL/SD    |
| `regeneration_step`                | int           |           | Current regeneration step                        | All      |
| `make_up_water_volume`             | int           | l         | Make-up water volume (water tank)                | All      |
| `exhausted_percentage`             | int           | %         | Adsorber exhausted percentage                    | SL/SD    |
| `actual_value_soft_water_hardness` | int           | °dH       | Actual soft water hardness                       | SL/SD    |
| `capacity_figure`                  | float         | m³x°dH    | Current capacity figure                          | All      |
| `flow_rate_peak_value`             | float         | m³/h      | Flow rate peak value                             | SL/SD    |
| `exchanger_peak_value`             | float         | m³/h      | Exchanger 1 peak flow rate                       | SL/SD    |
| `exchanger_peak_value_2`           | float         | m³/h      | Exchanger 2 peak flow rate                       | SL/SD    |
| `last_regeneration_exchanger`      | time          | HH:MM     | Last regeneration time exchanger 1               | SL/SD    |
| `last_regeneration_exchanger_2`    | time          | HH:MM     | Last regeneration time exchanger 2               | SL/SD    |
| `regeneration_progress_1`          | int           | %         | Regeneration progress exchanger 1                | SE       |
| `regeneration_progress_2`          | int           | %         | Regeneration progress exchanger 2                | All      |
| `regeneration_flow_rate_exchanger` | int           | l/h       | Regeneration flow rate exchanger 1               | SL/SD    |
| `regeneration_flow_rate_exchanger_2` | int         | l/h       | Regeneration flow rate exchanger 2               | All      |
| `blending_flow_rate`               | float         | m³/h      | Blending flow rate                               | All      |
| `step_indication_regeneration_valve` | int         |           | Step indication regeneration valve 1             | SL/SD    |
| `step_indication_regeneration_valve_2` | int       |           | Step indication regeneration valve 2             | All      |
| `current_chlorine`                 | int           | mA        | Current chlorine (chlorine cell)                 | SL/SD    |
| `remaining_amount_of_water`        | float         | m³        | Adsorber remaining amount of water               | All      |
| `lime_scale_indicator`             | int           | %         | Lime scale indicator                             | SE       |
| `days_until_inspection`            | int           | days      | Days until next inspection                       | SE       |
| `regeneration_counter_service`     | int           |           | Regeneration counter since last service          | SE       |
| `water_usage_today`                | int           | l         | Water usage today                                | SE       |
| `salt_usage_today`                 | float         | kg        | Salt usage today                                 | SE       |
| `lime_today`                       | int           |           | Lime value today                                 | SE       |

### Available configuration parameter

| Parameter                            | Type         | Supported series | Description                                                                                                                                                                                                      |
|--------------------------------------|--------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dlst`                               | boolean      | All              | Activation of daylight saving time                                                                                                                                                                               |
| `buzzer`                             | boolean      | All              | Activation of signal on error                                                                                                                                                                                    |
| `buzzer_from`                        | time (HH:MM) | All              | Signal from time                                                                                                                                                                                                 |
| `buzzer_to`                          | time (HH:MM) | All              | Signal to time                                                                                                                                                                                                   |
| `push_notification`                  | boolean      | All              | Activation of push notifications                                                                                                                                                                                 |
| `email_notification`                 | boolean      | All              | Activation of email notifications                                                                                                                                                                                |
| `water_hardness_unit`                | integer      | All              | Water hardness unit (1 = "°dH", 2 = "°fH", 3 = "°e", 4 = "mol/m³", 5 = "ppm")                                                                                                                                  |
| `raw_water_hardness`                 | integer      | All              | Raw water hardness value                                                                                                                                                                                         |
| `soft_water_hardness`                | integer      | All              | Soft water hardness value                                                                                                                                                                                        |
| `mode`                               | integer      | All              | Current operation mode (1 = "Eco", 2 = "Comfort", 3 = "Power", 4 = "Individual")                                                                                                                                |
| `mode_individual_monday`             | integer      | SL/SD            | Individual mode for Monday                                                                                                                                                                                       |
| `mode_individual_tuesday`            | integer      | SL/SD            | Individual mode for Tuesday                                                                                                                                                                                      |
| `mode_individual_wednesday`          | integer      | SL/SD            | Individual mode for Wednesday                                                                                                                                                                                    |
| `mode_individual_thursday`           | integer      | SL/SD            | Individual mode for Thursday                                                                                                                                                                                     |
| `mode_individual_friday`             | integer      | SL/SD            | Individual mode for Friday                                                                                                                                                                                       |
| `mode_individual_saturday`           | integer      | SL/SD            | Individual mode for Saturday                                                                                                                                                                                     |
| `mode_individual_sunday`             | integer      | SL/SD            | Individual mode for Sunday                                                                                                                                                                                       |
| `regeneration_mode`                  | integer      | All              | Regeneration mode (0 = "Auto", 1 = "Fixed")                                                                                                                                                                     |
| `regeneration_time_monday_1`         | time (HH:MM) | All              | Regeneration time Monday slot 1 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_monday_2`         | time (HH:MM) | All              | Regeneration time Monday slot 2 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_monday_3`         | time (HH:MM) | All              | Regeneration time Monday slot 3 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_tuesday_1`        | time (HH:MM) | All              | Regeneration time Tuesday slot 1 (`--:--` = unset)                                                                                                                                                              |
| `regeneration_time_tuesday_2`        | time (HH:MM) | All              | Regeneration time Tuesday slot 2 (`--:--` = unset)                                                                                                                                                              |
| `regeneration_time_tuesday_3`        | time (HH:MM) | All              | Regeneration time Tuesday slot 3 (`--:--` = unset)                                                                                                                                                              |
| `regeneration_time_wednesday_1`      | time (HH:MM) | All              | Regeneration time Wednesday slot 1 (`--:--` = unset)                                                                                                                                                            |
| `regeneration_time_wednesday_2`      | time (HH:MM) | All              | Regeneration time Wednesday slot 2 (`--:--` = unset)                                                                                                                                                            |
| `regeneration_time_wednesday_3`      | time (HH:MM) | All              | Regeneration time Wednesday slot 3 (`--:--` = unset)                                                                                                                                                            |
| `regeneration_time_thursday_1`       | time (HH:MM) | All              | Regeneration time Thursday slot 1 (`--:--` = unset)                                                                                                                                                             |
| `regeneration_time_thursday_2`       | time (HH:MM) | All              | Regeneration time Thursday slot 2 (`--:--` = unset)                                                                                                                                                             |
| `regeneration_time_thursday_3`       | time (HH:MM) | All              | Regeneration time Thursday slot 3 (`--:--` = unset)                                                                                                                                                             |
| `regeneration_time_friday_1`         | time (HH:MM) | All              | Regeneration time Friday slot 1 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_friday_2`         | time (HH:MM) | All              | Regeneration time Friday slot 2 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_friday_3`         | time (HH:MM) | All              | Regeneration time Friday slot 3 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_saturday_1`       | time (HH:MM) | All              | Regeneration time Saturday slot 1 (`--:--` = unset)                                                                                                                                                             |
| `regeneration_time_saturday_2`       | time (HH:MM) | All              | Regeneration time Saturday slot 2 (`--:--` = unset)                                                                                                                                                             |
| `regeneration_time_saturday_3`       | time (HH:MM) | All              | Regeneration time Saturday slot 3 (`--:--` = unset)                                                                                                                                                             |
| `regeneration_time_sunday_1`         | time (HH:MM) | All              | Regeneration time Sunday slot 1 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_sunday_2`         | time (HH:MM) | All              | Regeneration time Sunday slot 2 (`--:--` = unset)                                                                                                                                                               |
| `regeneration_time_sunday_3`         | time (HH:MM) | All              | Regeneration time Sunday slot 3 (`--:--` = unset)                                                                                                                                                               |
| `maintenance_interval`               | integer      | All              | Maintenance interval [days]                                                                                                                                                                                      |
| `installer_name`                     | string       | SL/SD            | Installer name                                                                                                                                                                                                   |
| `installer_phone`                    | string       | SL/SD            | Installer phone                                                                                                                                                                                                  |
| `installer_email`                    | string       | SL/SD            | Installer email                                                                                                                                                                                                  |
| `ntp_sync`                           | boolean      | All              | Get date/time automatically (NTP)                                                                                                                                                                                |
| `fault_signal_contact`               | boolean      | SL/SD            | Function fault signal contact                                                                                                                                                                                    |
| `knx`                                | boolean      | SL/SD            | KNX connection                                                                                                                                                                                                   |
| `nominal_flow_monitoring`            | boolean      | SL/SD            | Monitoring of nominal flow                                                                                                                                                                                       |
| `disinfection_monitoring`            | boolean      | All              | Disinfection monitoring                                                                                                                                                                                          |
| `led_ring_mode`                      | integer      | All              | Illuminated LED ring mode (0 = "deactivated", 1 = "permanent", 2 = "on failure", 3 = "on user operation + failure", 4 = "on water treatment + user operation + failure")                                        |
| `led_ring_flash_on_signal`           | boolean      | SL/SD            | Illuminated LED ring flashes for pre-alarm salt supply                                                                                                                                                           |
| `led_ring_brightness`                | integer      | All              | LED ring brightness [%]                                                                                                                                                                                          |
| `residual_capacity_limit`            | integer      | SL/SD            | Residual capacity limit value [%]                                                                                                                                                                                |
| `current_setpoint`                   | integer      | All              | Current setpoint [mA]                                                                                                                                                                                            |
| `charge`                             | integer      | All              | Charge [mAmin]                                                                                                                                                                                                   |
| `interval_forced_regeneration`       | integer      | All              | Interval of forced regeneration [days]                                                                                                                                                                           |
| `end_frequency_regeneration_valve`   | integer      | All              | End frequency regeneration valve 1 [Hz]                                                                                                                                                                          |
| `end_frequency_regeneration_valve_2` | integer      | All              | End frequency regeneration valve 2 [Hz]                                                                                                                                                                          |
| `end_frequency_blending_valve`       | integer      | All              | End frequency blending valve [Hz]                                                                                                                                                                                |
| `treatment_volume`                   | integer      | SL/SD            | Treatment volume [m³]                                                                                                                                                                                            |
| `soft_water_meter_pulse_rate`        | float        | All              | Soft water meter pulse rate [l/Imp]                                                                                                                                                                              |
| `blending_water_meter_pulse_rate`    | float        | All              | Blending water meter pulse rate [l/Imp]                                                                                                                                                                          |
| `regeneration_water_meter_pulse_rate` | float       | All              | Regeneration water meter pulse rate [l/Imp]                                                                                                                                                                      |
| `capacity_figure_monday`             | float        | All              | Capacity figure Monday [m³x°dH]                                                                                                                                                                                  |
| `capacity_figure_tuesday`            | float        | SL/SD            | Capacity figure Tuesday [m³x°dH]                                                                                                                                                                                 |
| `capacity_figure_wednesday`          | float        | SL/SD            | Capacity figure Wednesday [m³x°dH]                                                                                                                                                                               |
| `capacity_figure_thursday`           | float        | SL/SD            | Capacity figure Thursday [m³x°dH]                                                                                                                                                                                |
| `capacity_figure_friday`             | float        | SL/SD            | Capacity figure Friday [m³x°dH]                                                                                                                                                                                  |
| `capacity_figure_saturday`           | float        | SL/SD            | Capacity figure Saturday [m³x°dH]                                                                                                                                                                                |
| `capacity_figure_sunday`             | float        | SL/SD            | Capacity figure Sunday [m³x°dH]                                                                                                                                                                                  |
| `nominal_flow_rate`                  | float        | All              | Nominal flow rate [m³/h]                                                                                                                                                                                         |
| `regeneration_monitoring_time`       | integer      | All              | Regeneration monitoring time [min]                                                                                                                                                                               |
| `salting_monitoring_time`            | integer      | All              | Salting monitoring time [min]                                                                                                                                                                                    |
| `slow_rinse`                         | float        | All              | Slow rinse [min]                                                                                                                                                                                                 |
| `backwash`                           | float        | All              | Backwash [l]                                                                                                                                                                                                     |
| `washing_out`                        | float        | All              | Washing out [l]                                                                                                                                                                                                  |
| `minimum_filling_volume_smallest_cap` | float       | All              | Minimum filling volume smallest cap [l]                                                                                                                                                                          |
| `maximum_filling_volume_smallest_cap` | float       | All              | Maximum filling volume smallest cap [l]                                                                                                                                                                          |
| `minimum_filling_volume_largest_cap` | float        | All              | Minimum filling volume largest cap [l]                                                                                                                                                                           |
| `maximum_filling_volume_largest_cap` | float        | All              | Maximum filling volume largest cap [l]                                                                                                                                                                           |
| `longest_switch_on_time_chlorine_cell` | integer    | All              | Longest switch-on time chlorine cell [min]                                                                                                                                                                       |
| `maximum_remaining_time_regeneration` | integer     | SL/SD            | Maximum remaining time regeneration [min]                                                                                                                                                                        |
| `language`                           | integer      | All              | Current language (1 = "German", 2 = "English", 3 = "French", 4 = "Italian", 5 = "Dutch", 6 = "Spanish", 7 = "Russian", 9 = "Danish")                                                                           |
| `programmable_output_function`       | integer      | All              | Programmable output function                                                                                                                                                                                     |
| `programmable_input_function`        | integer      | All              | Programmable input function                                                                                                                                                                                      |
| `reaction_to_power_failure`          | integer      | All              | Reaction to power failure > 5 min                                                                                                                                                                                |
| `chlorine_cell_mode`                 | integer      | All              | Activate/deactivate chlorine cell                                                                                                                                                                                |
| `blending_monitoring`                | integer      | All              | Blending monitoring                                                                                                                                                                                              |
| `system_overloaded`                  | integer      | All              | System overloaded                                                                                                                                                                                                |

And these are additional parameters which are provided by the API, but their meaning and/or value is not known:

| Parameter      | Type |
|----------------|------|
| `ppressurereg` | int  |

Feel free to open an [issue](https://github.com/p0l0/pygruenbeck_cloud/issues) if you know the meaning of them and their possible values.
