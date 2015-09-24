# mLamp Raspberry

I use my Raspberry PI as a headless server that is always on. The idea was to create a proxy server with a nice web interface to control the lamps. However so far I have only built a smart alarm clock. I'm really proud of this, because this is something that is uniquely possible with my lamp design and would be much harder to do with any comercially available RGB LED lamps.

I wake up every day at 7:30, which is when my iPhone alarm clock rings. The Raspberry alarm clock fades in between 7:00 and 7:30 to create a nice ambient light that helps me get up rested and happy. You know, like in the advertisements!

On top of that, Raspberry checks weather forecast for my city at 6:55 and then it actually fades in with a color that is matched to the forecast peak temperature of the day using a custom made color map (cold temps go to blue, moderate to yellow and hot to red)

### Setup

In this repository I have a set of scripts that I run on the Raspberry. They are not particularly well combed, because they are still work in progress and in the end they are just a couple of simple scripts.

I'm using Raspbian Jessie, but the only really important thing is Python 3

For most of the things vanilla Python 3 install should do. If you want to calibrate your own temperature scale, you'll need also `numpy` and `opencv2`, required by `color_test.py`.

1. Place all the files in this repository into /home/pi/mlamp you can do that by doing

    git clone github.com:mirosval/mLamp-Raspberry.git mlamp

2. Make sure it is writable and that the scripts are executable
3. Install crontab (see below)

### Crontab

Root crontab:

    35 6 * * * /home/pi/mlamp/rebooter.sh

Pi's crontab

    30,40,50 6 * * * cd /home/pi && python3 mlamp/weather.py &> weather_error.log
    00 7 * * * cd /home/pi && python3 mlamp/lamp_driver.py &> lamp_error.log

### Problems

The main problem with the Raspberry I had was wifi. The router in my house is weak and far away, so the wifi would often drop. At first I even had problems with just maintaining an already established connection. This turned out to be a power saving issue, I fixed that with:

    sudo vi /etc/modprobe.d/8192cu.conf

And then entering the following:

    # Disable power saving
    options 8192cu rtw_power_mgnt=0 rtw_enusbss=1 rtw_ips_mode=1

Reboot:

    sudo reboot

This immediately cleared the connection issues, but after a few days Raspberry still disconnects from the network and does not want to communicate. I tried to mitigate this by introducing a reboot script (that is actually the root crontab entry). What this does is it runs after the first weather fetching script, which should have updated the temperature in `daily_temp.txt`. If the temperature has been updated, it does nothing. If it hasn't it will reboot raspberry, hopefully fixing the wifi issue. The weather fetching script is then set to run again, now with (hopefully) working network.
