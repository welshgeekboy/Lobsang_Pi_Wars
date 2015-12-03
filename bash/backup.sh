#!/bin/bash
#
# backup(.sh)-  will mount,  copy  data
# to, then unmount my USB stick. As the
# Pi A+ has only one USB port, it makes
# copying data somewhat difficult. This
# script starts a countdown to give you
# time to  swap the  wireless  keyboard
# dongle and the USB stick, then copies
# over all the important data and  code
# for adding to the git repository, and
# creates a complete  backup  including
# adding files that don't get copied to
# the GitHub folder.  Files  to  ignore
# are put in  ~/lobsang/.ignore  and do
# not get copied to the  GitHub folder.
#
# Created Nov 2015 by Finley Watson.


# Possible command line arguements (all 0 or 1)
# When they have nothing after '=' sign they are false.
list_usb_folder=
delay=1
unmount_when_finished=1
verbose=1

# A crude way of checking for command line arguements.
if [ -n "$1" ] ; then
	if [ "$1" == "-l" ] || [ "$1" == "-list" ] ; then
		list_usb_folder=1
	elif [ "$1" == "-i" ] || [ "$1" == "-immediate" ] ; then
		delay=
	elif [ "$1" == "-m" ] || [ "$1" == "--leave-mounted" ] ; then
		unmount_when_finished=
	elif [ "$1" == "-q" ] || [ "$1" == "--quiet" ] ; then
		verbose=
	fi
	if [ -n "$2" ] ; then
		if [ "$2" == "-l" ] || [ "$2" == "-list" ] ; then
			list_usb_folder=1
		elif [ "$2" == "-i" ] || [ "$2" == "-immediate" ] ; then
			delay=
		elif [ "$2" == "-m" ] || [ "$2" == "--leave-mounted" ] ; then
			unmount_when_finished=
		elif [ "$2" == "-q" ] || [ "$2" == "--quiet" ] ; then
			verbose=
		fi
		if [ -n "$3" ] ; then
			if [ "$3" == "-l" ] || [ "$3" == "-list" ] ; then
				list_usb_folder=1
			elif [ "$3" == "-i" ] || [ "$3" == "-immediate" ] ; then
				delay=
			elif [ "$3" == "-m" ] || [ "$3" == "--leave-mounted" ] ; then
				unmount_when_finished=
			elif [ "$3" == "-q" ] || [ "$3" == "--quiet" ] ; then
				verbose=
			fi
			if [ -n "$4" ] ; then
				if [ "$4" == "-l" ] || [ "$4" == "-list" ] ; then
					list_usb_folder=1
				elif [ "$4" == "-i" ] || [ "$4" == "-immediate" ] ; then
					delay=
				elif [ "$4" == "-m" ] || [ "$4" == "--leave-mounted" ] ; then
					unmount_when_finished=
				elif [ "$4" == "-q" ] || [ "$4" == "--quiet" ] ; then
					verbose=
				fi
			fi
		fi
	fi
fi

if [ $verbose ] ; then
	echo    "Will now copy, including child directories, excluding files and folders in ~/lobsang/.ignore:"
	echo -e "\t/home/pi/lobsang/*"
	echo -e "\t/home/pi/sketchbook/*"
	echo -e "\t/home/pi/.bashrc"
	echo
	echo "Please insert Cruzer USB stick."
fi

# Waits for tens seconds before copying, with a visual countdown.
# Gives the user time to plug in the USB stick.
if [ $delay ] ; then
	if [ $verbose ] ; then
		for value in `seq 0 10` ; do
			printf "Time before copy begins: $((10-value))s \r"
			sleep 1
		done
		echo "USB stick should now be plugged in."
	else
		sleep 10
	fi
fi

if [ $verbose ] ; then
	printf "Copying...\r"
fi

# Clear the dump file of old data
sudo rm /tmp/delete_me.dump
sudo touch /tmp/delete_me.dump

# Mount the USB stick
sudo mkdir /media/CRUZER 2>> /tmp/delete_me.dump
sudo mount /dev/sda1 /media/CRUZER 2>> /tmp/delete_me.dump

# Just in case the directories don't exist (very unlikely)
# try to create them. Send stderr to a dump file in /tmp/
sudo mkdir /media/CRUZER/Lobsang/                   2>> /tmp/delete_me.dump
sudo mkdir /media/CRUZER/Lobsang/github/            2>> /tmp/delete_me.dump
sudo mkdir /media/CRUZER/Lobsang/github/sketchbook/ 2>> /tmp/delete_me.dump
sudo mkdir /media/CRUZER/Lobsang/backup/            2>> /tmp/delete_me.dump
sudo mkdir /media/CRUZER/Lobsang/backup/sketchbook/ 2>> /tmp/delete_me.dump

# Copy over all the all files to be backed up.
cp -r /home/pi/lobsang/*    /media/CRUZER/Lobsang/github
cp -r /home/pi/sketchbook/* /media/CRUZER/Lobsang/github/sketchbook/
cp    /home/pi/.bashrc      /media/CRUZER/Lobsang/github/.bashrc
cp -r /home/pi/lobsang/*    /media/CRUZER/Lobsang/backup/
cp -r /home/pi/sketchbook/* /media/CRUZER/Lobsang/backup/sketchbook/
cp    /home/pi/.bashrc      /media/CRUZER/Lobsang/backup/.bashrc

# Delete all files listed in .ignore from the USB stick's GitHub folder.
# Not all of the files need to be uploaded to GitHub. The backup folder
# on the USB stick contains every single file though.
if [ $verbose ] ; then
	printf "Deleting...\r"
fi

while read path; do
	rm -r /media/CRUZER/Lobsang/github/$path
done < .ignore

# Automatically remove the sensitive info from Padlock.py so I'm not
# telling the world the login keys to access Lobsang! I use 'sed -i'
# to change the file directly instead of eg. printing to the terminal.
while read key; do
	if [ $verbose ] ; then
		echo "Removing key '$key' from USB stick's Padlock.py for GitHub."
	fi
	sed -i s/$key/****/ /media/CRUZER/Lobsang/github/Padlock.py
done < .passkeys

if [ $verbose ] ; then
	echo "Transferred files."
fi

# If user has specified to list the content of /media/CRUZER/Lobsang/github
# with the arguement "-l" or "--list", then do. Otherwise (auto) don't.
if [ $list_usb_folder ] ; then
	echo "Contents of /media/CRUZER/Lobsang/github/:"
	ls -hal --color=auto /media/CRUZER/Lobsang/github/
fi

# Unmount the USB stick
if [ $unmount_when_finished ] ; then
	sudo umount /media/CRUZER/
	sudo rm -r /media/CRUZER/
fi

if [ $verbose ] ; then
	echo "It is safe to remove the USB stick."
fi

# All finished!
exit 0
