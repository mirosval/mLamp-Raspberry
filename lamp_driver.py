from __future__ import print_function, division
from color_interpolation import color_interpolate_map, color_interpolate_fade_in
from time import sleep
import logging
import datetime
import os

logging.basicConfig(filename="lamp_driver.log", level=logging.INFO, format='%(asctime)s %(message)s')

# TODO: All these config variables should be moved into a config file...
lamp_addresses = [
    "FC:8F:6C:07:0C:DC",
    "FB:AE:B7:C9:D2:CB"
]

alarm_start_hour = 7
alarm_start_minute = 0
alarm_stop_hour = 7
alarm_stop_minute = 30

color_map = {
    0.0: (0, 0, 255),
    0.2: (255, 255, 255),
    0.5: (255, 255, 255),
    0.8: (255, 200, 0),
    1.0: (255, 0, 0)
}


def alarm_length():
    """Calculate the "alarm" duration in seconds based on configuration

    Returns:
        alarm length in seconds
    """
    start = datetime.time(hour=alarm_start_hour, minute=alarm_start_minute)
    stop = datetime.time(hour=alarm_stop_hour, minute=alarm_stop_minute)

    delta = datetime.timedelta(hours=stop.hour - start.hour, minutes=stop.minute - start.minute)

    return delta.seconds


def current_time():
    """Distance in seconds from "alarm start"

    Returns:
        float current time
    """
    start = datetime.time(hour=alarm_start_hour, minute=alarm_start_minute)
    now = datetime.datetime.now()

    delta = datetime.timedelta(hours=now.hour - start.hour, minutes=now.minute - start.minute)

    return max(0, delta.seconds)


def read_temperature():
    """Retrieve temperature from the daily_temp.txt file

    Returns:
        float temperature or 0.0 on error
    """
    temp = 0.0
    with open("daily_temp.txt", "r") as f:
        temp = float(f.readline())

    return temp


def interpolate_temperature(temperature):
    """Transform temperature from degree celsius to 0.0 - 1.0 range
    0.0 is -10 degrees (very cold)
    1.0 is 35 degrees (very hot)

    Parameters:
        temperature - float in degrees celsius

    Returns:
        float normalized temperature
    """
    return min(1.0, max(0.0, (10 + temperature) / 45))


def lamp_set_color(color):
    """Actually send the color to the lamp HW using gatttool command line tool

    Parameters:
        color - tuple RGB 0 - 255; color to send to lamp
    """
    addresses = lamp_addresses

    r = hex(color[0])[2:].zfill(2)
    g = hex(color[1])[2:].zfill(2)
    b = hex(color[2])[2:].zfill(2)

    # the 01 here at the beginning of the message means that
    # the lamp will hold the color even when the connection is lost
    value = "01" + r + g + b

    for address in addresses:
        command = "gatttool -b {} -t random --char-write --handle=0x0011 --value={}".format(address, value)
        logging.debug("Sending command to RFduino: " + command)
        os.system(command)


def main():
    """Main method

    This is run from cron. Will keep running until the specified stop time
    """
    logging.info("Starting mLamp Driver")

    temperature = read_temperature()
    temp_progress = interpolate_temperature(temperature)
    color = color_interpolate_map(color_map, temp_progress)

    logging.info("Temperature is: {}C, final color will be: {}".format(temperature, color))

    while True:
        now = datetime.datetime.now()
        is_alarm_hour = alarm_start_hour <= now.hour <= alarm_stop_hour
        is_alarm_minute = alarm_start_minute <= now.minute <= alarm_stop_minute

        if is_alarm_hour and is_alarm_minute:
            time_progress = current_time() / alarm_length()

            final_color = color_interpolate_fade_in(color, time_progress)
            logging.debug("Setting color to: {}".format(final_color))

            lamp_set_color(final_color)

            sleep(10)
        elif now.hour > alarm_stop_hour and now.minute > alarm_stop_minute:
            # don't forget to turn the lamps off when the time comes
            lamp_set_color((0, 0, 0))
            break
        else:
            sleep(60)

    logging.info("Stopping mLamp Driver")

if __name__ == "__main__":
    main()
