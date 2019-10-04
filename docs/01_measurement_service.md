# Set up energy measurement

## Unix service for measuring energy

### Prerequisites

Install the necessary packages with the following command.

```sh
sudo apt-get install -y build-essential libsystemd-dev

sudo pip3 install pi-ina219
sudo pip3 install systemd
```

These packages are required to use the systemd properly.

### Create a configuration file

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

### Starting the service

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

### Check logs

The logs are avaliable through JournalCTL.

```sh
journalctl -u energymeasurement
```

## FTP Server for publishing measurements

Install the necessary package with the following command.

```sh
sudo apt-get install -y proftpd
```

During the installation process, it  will ask how ProFTP should be started. Choose “standalone” option.

### Configure the FTP server

```sh
sudo ftpasswd --passwd  --name energy --gid 33 --uid 33 --home /var/www/ --shell /bin/false
```

The following content should be put at the end of  `/etc/proftpd/proftpd.conf` configuration file.

```txt
DefaultRoot /home/pi/work/measurement_logs
AuthOrder mod_auth_file.c  mod_auth_unix.c
AuthUserFile /etc/proftpd/ftpd.passwd
AuthPAM off
RequireValidShell off
```

Restart the service.

```sh
sudo /etc/init.d/proftpd restart
```

Open a browser and searh for the `ftp://<raspberry-pi>`. It should ask for the credentials.

If the set-up has failed, check [Raspberry Pi tutorials](https://tutorials-raspberrypi.com/raspberry-pi-ftp-server-installation/) or [Patchesoft](https://www.patchesoft.com/learn-linux-installing-and-configuring-ftp-with-proftpd) for more detailed information.
