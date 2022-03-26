Install CUPS
1. sudo apt install dpkg
2. sudo apt-get install cups -y
3. sudo usermod -a -G lpadmin pi
4. sudo cupsctl --remote-admin --remote-any --share-printers
5. sudo reboot

Config Printer
1. http://127.0.0.1:613
2. Administration (user:"pi", password:"raspberry")
3. Add Printer
4. Select Printer
5. Default option
6. Print Test Page