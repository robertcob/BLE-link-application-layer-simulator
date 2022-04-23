# BLE link/application layer simulator

This is a simulation of a heart monitering device using bluetooth low energy.

This repository is part of the Final Year Project Module of the Computer Science Degree course at the [School of Computer Science and Information Technology](https://www.ucc.ie/en/compsci/ "School of Computer Science and Information Technology") (CSIT) at [University College Cork](https://www.ucc.ie/en/ "University College Cork") (UCC), Ireland.  


<summary><h3 style="display: inline-block">Table of Contents</h3></summary>
  <ol>
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#user-guide">User Guide</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#application-walk-through">Application walk-through</a></li>
      </ul>
    </li>
  </ol>

___________________

### Abstract

Secure Live-Boot Linux Environment For Bitcoin Paper Wallet Generation

This app creates a live bootable USB linux distribution. When booted shows a simplstic one-app system, completely air-gapped with no networking intefaces
and no desktop environment. A simplistic UI created using Pythons frontend framework Kivi will help the user create/restore a valid bitcoin wallet in the 
simplest and easiest way possible, while being completely secure at the same time.

- **NOTE:** Unfortunately our custom Linux distribution is not ready for deployment as the scope of our project was too large. So we are releasing the application as a standalone Windows app. 
  It all works as intended, same as the other Paper Wallet Generators out there, it's just the superb security aspect of our project that's lacking.

### Author
- Robert O'Brien


### Built With

* [Tkinter](https://docs.python.org/3/library/tkinter.html) - The  Python Frontend framework used
* [simpy](https://simpy.readthedocs.io/en/latest/) - A Process-based discrete-event simulation framework based on standard Python.
* [CS4628 Internet of Things](https://reg.ucc.ie/curriculum/modules/?mod=CS4628) - Media classes for abstraction taken from Internet of Things class taken alongside FYP

# User Guide

## Installation
The installation assumes that:

-  _Python 3_ or above is already installed on your machine

-  An up-to-date version of _Pip_ is also available on your machine

-  A stable internet connection is present

### Instructions
First extract the zipped file as provided
Navigate to the extracted folder. 

You should see the following files:

.
├── application
├── ATT
│   └── packets
├── controller
├── GAP
├── GAT
├── guiExtensions
├── image-assets
├── simulations
└── utilities
etc..

You will need to use pip to install all python requiremeints
The command to do this is simply _pip install -r requirements.txt_

If this command fails, ensure you are using the '-r' flag.
Otherwise you can open the _requirements.txt_ file and use pip to individually install each library.
The individual requirements are...
- numpy==1.22.3
- Pillow==9.1.0
- simpy==4.0.1
- tk==0.1.0

## Application walk-through
To run each of the simulatiions _BLEWhitelist.py_ and _fullBLE5.py_ simpy run the command _python3 BLEWhitelist.py_ or _python3 fullBLE5.py_

To run the GUI enter the command _python3 gui.py_ and the Graphical User interface will appear.

Within each simulation file there are two flags set for logging and debugging.
- ENABLE_GUI
- DEBUG_RADIO

ENABLE GUI allows for logging to an external csv file in the _simulations_ directory.
DEBUG_RADIO logs information to the terminal.
