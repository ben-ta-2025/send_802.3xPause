# send_802.3xPause.py

## Overview

`send_802.3xPause.py` is a Python script for sending IEEE 802.3x Ethernet PAUSE frames from a specified network interface. This can be useful for testing flow control mechanisms on network devices or simulating congestion scenarios.

## Features

- Sends 802.3x PAUSE frames with customizable source MAC address, pause time, and repeat count.
- Uses raw sockets for direct frame transmission.
- Validates MAC address and input parameters.

## Requirements

- Python 3.x
- Root privileges (required for raw socket operations)
- Linux environment

## Usage

```sh
sudo python3 send_802.3xPause.py [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-i Interface`, `--interface=Interface` | **(Required)** The network interface to send packets from (e.g., eth0). |
| `-s SourceMac`, `--sourcemac=SourceMac` | The source MAC address to use (format: XX-XX-XX-XX-XX-XX or XX:XX:XX:XX:XX:XX). Default: 01-02-03-04-05-06 |
| `-p PauseTime`, `--pausetime=PauseTime` | The pause time value (0-65535). Default: 65535 |
| `-r RepeatNumber`, `--repeatnum=RepeatNumber` | Number of times to send the PAUSE frame. Default: 1 |

### Example

```sh
sudo python3 send_802.3xPause.py -i eth0 -s 00-11-22-33-44-55 -p 1000 -r 5
```

This command sends 5 PAUSE frames from interface `eth0` with source MAC `00-11-22-33-44-55` and pause time `1000`.

## Notes

- The script must be run as root to access raw sockets.
- The destination MAC address for PAUSE frames is fixed to `01-80-C2-00-00-01` as per the IEEE 802.3x standard.
- The Ethertype is set to `0x8808` and the opcode to `0x0001`.
