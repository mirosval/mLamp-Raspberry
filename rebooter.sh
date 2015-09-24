# if the daily_temp.txt hasn't been updated in the last 10 minutes
if test `find "/home/pi/daily_temp.txt" -mmin +10`
then
    /sbin/shutdown -r
fi
