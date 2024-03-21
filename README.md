### SteamVR Basestation Control

A home assistant intergration that allows you to control your SteamVR Basestations.

Your Home Assistant need to have a bluetooth module for this to work and close enough to your stations to be picked up.

## Installation

```
cd ~
cd homeassistant
mkdir custom_components
cd custom_components
git clone https://github.com/NgNority/Home_assistant_Basestation.git
```
After this, restart your Home Assistant and it should now be working.

## Adding basestations

You need your basestations MAC address to add it to Home Assistant. I recomend using Lighthouse PM to find the MAC addresses of your basestations.

To add a basestation, this is the required YAML code:

```
light:
  - platform: basestation
    name: "Basestation"
    mac: "D8:71:4D:31:09:68"
```

You can change the name and the MAC address accordingly.

One more reboot and they should now show up in your Overview!
