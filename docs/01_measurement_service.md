# Unix service for measuring energy

## Prerequisites

Install the necessary packages with the following command.

```sh
sudo apt-get install -y build-essential libsystemd-dev

sudo pip3 install pi-ina219
sudo pip3 install systemd
```

TODO: document this
https://tutorials-raspberrypi.com/raspberry-pi-ftp-server-installation/
https://www.patchesoft.com/learn-linux-installing-and-configuring-ftp-with-proftpd

These packages are required to use the systemd properly.

## Create a configuration file

```sh
sudo nano /etc/systemd/system/energymeasurement.service
```

Copy the following content to the editor:

```txt
[Unit]
Description=Energy measurement service.
StartLimitIntervalSec=0

[Service]
Type=simple

Restart=always
RestartSec=1

User=pi
WorkingDirectory=/home/pi/work
ExecStart=/usr/bin/python3 /home/pi/work/serial_listener.py

SyslogIdentifier=energymeasurement

[Install]
WantedBy=multi-user.target
```

Save it. This config defines a service which is able run background just after the restart. You need to set proper premissions for this file.

```sh
sudo chmod 644 /etc/systemd/system/energymeasurement.service
```

## Starting the service

```sh
sudo systemctl start energymeasurement
sudo systemctl enable energymeasurement
sudo systemctl status energymeasurement
```

If the service has been set up correctly, the output should be the following:

```sh
● energymeasurement.service - Energy measurement service.
   Loaded: loaded (/etc/systemd/system/energymeasurement.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2019-07-09 20:49:34 CEST; 16s ago
 Main PID: 1362 (python3)
   CGroup: /system.slice/energymeasurement.service
           └─1362 /usr/bin/python3 /home/pi/work/serial_listener.py

júl 09 20:49:34 energyPi systemd[1]: Started Energy measurement service..

```

The `enable` command is used to start the service when the OS boots. Furthermore it can be handled with the standard `stop`, `restart` unix commands.

## Check logs

The logs are avaliable through JournalCTL.

```sh
journalctl -u energymeasurement
```
