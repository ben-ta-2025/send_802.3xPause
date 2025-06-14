#!/usr/bin/env python3

"""
python3 send_802.3xPause.py
Egress Interface must be specified.
Usage: python3 send_802.3xPause.py [options]

Options:
  -h, --help            show this help message and exit
  -i Interface, --interface=Interface
                        The Interface to egress packets.(Must)
  -s SourceMac, --sourcemac=SourceMac
                        The Source Mac to egress packets. XX-XX-XX-XX-XX-XX
  -p PauseTime, --pausetime=PauseTime
                        The Pause Time. (InterfaceSpeed x PauseTime x 512BitTimes..
  -r RepeatNumber, --repeatnum=RepeatNumber
                        The Number of times to send packets.

MAC-specific control protocols 802.3x PAUSE
Destination MAC | 01-80-C2-00-00-01
Source MAC      | Machine MAC
Ethertype       | 0x8808
OpCode          | 0x0001
"""

import socket
import sys
import optparse
import re

# 定数
DEFAULT_SRC_MAC = '010203040506'
DEFAULT_PAUSE_TIME = 65535
DEFAULT_REPEAT_NUM = 1
DST_MAC = '0180c2000001'
ETHERTYPE = '8808'
OPCODE = '0001'
DUMMY_PADDING = '00' * 42

def validate_mac(mac):
    """Validate MAC address (12-digit hexadecimal)"""
    return re.fullmatch(r'[0-9a-fA-F]{12}', mac) is not None

def main():
    usage = "usage: python3 %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--interface", type="string", dest="interface", help="The Interface to egress packets.(Must)", metavar="Interface")
    parser.add_option("-s", "--sourcemac", type="string", dest="sourcemac", help="The Source Mac to egress packets. XX-XX-XX-XX-XX-XX", metavar="SourceMac")
    parser.add_option("-p", "--pausetime", type="int", dest="pausetime", help="The Pause Time. (InterfaceSpeed x PauseTime x 512BitTimes..", metavar="PauseTime", default=DEFAULT_PAUSE_TIME)
    parser.add_option("-r", "--repeatnum", type="int", dest="repeatnum", help="The Number of times to send packets.", metavar="RepeatNumber", default=DEFAULT_REPEAT_NUM)
    (options, args) = parser.parse_args()

    if not options.interface:
        print("Egress Interface must be specified.\n")
        parser.print_help()
        sys.exit(1)

    # Format and validate MAC address
    if options.sourcemac:
        srcmac = options.sourcemac.replace('-', '').replace(':', '')
        if not validate_mac(srcmac):
            print(f"Incorrect Mac Address pattern: {options.sourcemac}")
            print("e.g. -> XX-XX-XX-XX-XX-XX or XX:XX:XX:XX:XX:XX\n")
            parser.print_help()
            sys.exit(1)
    else:
        srcmac = DEFAULT_SRC_MAC

    # Format PauseTime
    if options.pausetime < 0 or options.pausetime > 65535:
        print("Pause Time must be between 0 and 65535.\n")
        parser.print_help()
        sys.exit(1)
    if options.pausetime == 0:
        print("Pause Time is set to 0, which means no pause.\n")
        options.pausetime = DEFAULT_PAUSE_TIME  # Default to 65535 if 0 is given
    elif options.pausetime > 65535:
        print("Pause Time exceeds maximum value of 65535. Setting to 65535.\n")
        options.pausetime = DEFAULT_PAUSE_TIME  # Cap to 65535 
    else:
        print(f"Pause Time set to {options.pausetime}.")   
        pausetime = format(options.pausetime, '04x')

    # Number of transmissions
    if options.repeatnum < 1:
        print("Repeat Number must be at least 1.\n")
        parser.print_help()
        sys.exit(1)
    else:
        print(f"Repeat Number set to {options.repeatnum}.") 
        repeat_num = options.repeatnum

    # Create socket
    try:
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        sock.bind((options.interface, 0))
    except Exception as e:
        print(f"Socket error: {e}\n")
        parser.print_help()
        sys.exit(1)
    
    # Generate frame
    frame_hex = DST_MAC + srcmac + ETHERTYPE + OPCODE + pausetime + DUMMY_PADDING
    frame = bytes.fromhex(frame_hex)

    # Send the frame
    for i in range(repeat_num):
        sock.sendall(frame)
        print(f"Sent 802.3x PAUSE packet {i + 1} times.")

    sock.close()

if __name__ == "__main__":
    main()
    sys.exit(0)
