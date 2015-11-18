#!/bin/bash
#
# backup.sh- a file to mount, copy data
# to, then unmount my USB stick. As the
# Pi A+ has only one USB port, it makes
# copying data somewhat difficult. This
# script starts a countdown to give you
# time to  swap the  wireless  keyboard
# dongle and the USB stick, then copies
# over all the important data and  code
# for adding to the git repository etc.

echo "Will now copy (including child directories): /home/pi/lobsang/*"
echo "                                             /home/pi/sketchbook/*"
echo "                                             /home/pi/.bashrc"

echo "Please insert Cruzer USB stick."

for value in `seq 0 10` ; do
	printf "Time before copy begins: $((10-value))s \r"
	sleep 1
done

echo "USB stick should now be plugged in."

printf "Copying...\r"
sudo mkdir /media/CRUZER
sudo mount /dev/sda1 /media/CRUZER

cp -r /home/pi/lobsang/     /media/CRUZER/Lobsang/lobsang/
cp -r /home/pi/sketchbook/  /media/CRUZER/Lobsang/sketchbook/
cp    /home/pi/.bashrc      /media/CRUZER/Lobsang/.bashrc

sudo umount /media/CRUZER
sudo rmdir /media/CRUZER
echo "Copied     "
echo "It is safe to remove the USB stick."
exit 0
