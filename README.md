# Project

**This script is made to collect Prometheus metrics for the disk of the PC, using an application called CrystalDiskInfo**

Metrics are collected for each drive on the PC/server, consisting of:
- Disk Model
- Disk temperature
- Disk size
- Disk Health

This project was created at a summer internship, I would say that this was my first ever "proper" project

# Information

- As this file uses Prometheus, you would need to install it:

  `pip install prometheus-client`

- The version of CrystalDiskInfo used in this program is **CrystalDiskInfo8_17_3**

- This file uses *regular expressions* to search for disk information, a useful tool to figure out the correct expressions to use is [regex101](https://regex101.com/)

**This program assumes that CrystalDiskInfo is located directly under the C:\ drive, this is where the *DiskInfo.txt* file and the *results.prom* file are generated**
