# FF_ShellyMilight
Integrates Shelly as switch in an MQTT environment with remotely commanded bulbs

## What's for?

This code manages a button and a relay (inside a Shelly 1PM module but can be anything else) to light a Milight bulb (but can be anything else, including ZigBee lights), with a local bypass (per WAF requirement).

Functions are as follow:
  - Initially relay is off, so power is off, connected bulb is off, initial state is set to off,
  - MQTT is connected and a state topic is queried,
  - As state topic is retained, module receives last Milight bulb state, and sets internal state accordingly,
  - When internal state turns to on, relay is set to on and stays on,
  - When a state topic is received, internal state is set accordingly,
  - If button state changes, internal state is toggled, and internal state value is send to command topic,
  - (External) Milight server is listening to command topic, sends radio command to bulb, then updates state topic,
  - State topic update is received and internal state updated.

Note: Milight server send State topic or Update topic or both. This code is able to manage either or both. Should your server have only one topic, just let the other empty.

## What's not so common?

This is nice, but you may stay in black is something don't work as expected (WiFi, MQTT, Milight server, ...)

To fulfill WAF (Wife Acceptance Factor) requirements, few things have been added:
  - A timer is started when a command is sent,
  - If no state message is received in 1.5 seconds, it means that there's a problem somewhere,
  - In this case, we're running in bypass mode, where bulb is managed locally by the relay,
  - When entering in bypass mode, we have to take in account a specific case, when we have to switch the bulb on, while power (relay) is already on (but has previously received an OFF frame). To fix this, we turn the relay off for second, in order for capacity in build to discharge, and turn relay on to light bulb. Then, we enter a normal cycle where bulb is light by power it on, and turned off by cutting power (amazing, isn't it?),
  - Automatic cycle resumes when a state message is received. When this occurs, message is ignored (as state could have changed meanwhile), and internal state is sent back. Normal cycle resumes (and Milight state will match internal state).

Doing that way, module is autonomous, and can work alone, while being able to integrate your domotic system when working ;-)

## What can be setup?

Lot of things are driven by parameters set in FF_ShellyMilight.c file. Please have a look to it. Here are the main:
  - Traces are sent to serial (should you decide to test code on a "classical" ESP8266) if you define SERIAL_TRACE,
  - Traces are sent to SYSLOG if you define SYSLOG_HOST (and not SERIAL_TRACE),
  - Else traces are not generated,
  - You may define SHADOW_LED_PIN to visualize internal state on a LED,
  - You should define button level change(s) that will trigger an internal state change (BUTTON_LOW_TO_HIGH or BUTTON_HIGH_TO_LOW for a push button, both for a switch),
  - You may write stats to trace defining STATS_INTERVAL,
  - You may send periodically internal temperature to MQTT defining TEMPERATURE_TOPIC.

## Prerequisites

This codes comes with a PlatformIo configuration file, allowing to setup multiple environments. If you don't want to use PlatformIo, you may use Arduino IDE, but should move lib and src folder to root folder, and add the few defines from platformio.ini to FF_ShellyMilight.h.

You may also use VSCodium (or VsCode if you're an MS fan) with platformio extension.

## Installation

Follow these steps:
1. Clone repository somewhere on your disk.
```
cd <where_you_want_to_install_it>
git clone https://github.com/FlyingDomotic/FF_ShellyMilight.git FF_ShellyMilight
```

2. Copy platformio.ini file from examples to project root folder
```
cd <where_you_installed_FF_ShellyMilight>
cp ./example/platformio.example ./platformio.ini
```

3. Copy FF_ShellyMilight.h from examples to /src folder
```
cd <where_you_installed_FF_ShellyMilight>
cp ./example/FF_ShellyMilight.example ./src/FF_ShellyMilight.h
```

4. Adapt these two files to your needs

## Update

1. Go to code folder and pull new version:
```
cd <where_you_installed_FF_ShellyMilight>
git pull
```

Note: if you did any changes to plugin files and `git pull` command doesn't work for you anymore, you could stash all local changes using
```
git stash
```
or
```
git checkout <modified file>
```

## ** WARNING - DANGER OF DEATH **

** MODULES SHOULD BE PHYSICALLY DISCONNECTED (WIRES REMOVED) FROM POWER BEFORE DOING ANYTHING **.

As told everywhere, Shelly modules are connected to 120V/240V power. This can kill you should you touch anything when module is connected to power. In addition, connecting both power on module and serial on a PC will fry the latest.

## Code download

This code includes Arduino OTA routines. This allows (remote) code update through WiFi connection. As usual, first version would probably need a serial connection to load it, unless module already has OTA code already loaded. In any case, follow mandatory rule of disconnecting wires before using serial connection.
