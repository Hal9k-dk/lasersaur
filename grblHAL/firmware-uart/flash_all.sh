#!/bin/sh
esptool.py --chip esp32 -p /dev/ttyUSB0 -b 460800 write_flash --flash_mode dio --flash_freq 40m --flash_size 4MB 0x1000 bootloader.bin 0x10000 grbl.bin 0x8000 partitions.bin
