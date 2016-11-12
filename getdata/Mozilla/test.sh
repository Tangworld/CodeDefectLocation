#! /bin/sh
printf "Enter new password: "
stty -echo
read pass < /dev/tty
printf "\nEnter again: "
read pass2 < /dev/tty
stty echo
echo $pass
echo $pass2