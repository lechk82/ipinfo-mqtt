"""
Collect data ipinfo and send to MQTT
"""

import argparse
import json
import logging
import sys
import time
import mqtt
import ipinfo

logging.basicConfig(level=logging.INFO)


def load_config(file):
    """
    Load configuration
    :return:
    """
    with open(file, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        return config

def single_run(file):
    """
    Output current watts and kilowatts
    :return:
    """

    _t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timestamp = {"timestamp" : _t}
    config = load_config(file)
    topic = config["mqtt"]["topic"]
    id = config["id"]

    handler = ipinfo.getHandler(config["token"])
    details = handler.getDetails()
    details = details.all
    details.update(timestamp)
    
    if config["debug"]:
        logging.info(json.dumps(details, indent=4, sort_keys=True))

    logging.info("%s -  Publishing MQTT to %s...", _t, topic+"/"+id)
    mqtt.message(config["mqtt"], topic+"/"+id, json.dumps(details))
       
def daemon(file, interval):
    """
    Run as a daemon process
    :param file: Config file
    :param interval: Run interval in seconds
    :return:
    """
    interval = int(interval)
    logging.info("Starting daemonized with a %s seconds run interval", str(interval))
    while True:
        try:
            single_run(file)
            time.sleep(interval)
        except Exception as error:  # pylint: disable=broad-except
            logging.error("Error on start: %s", str(error))
            sys.exit(1)


def main():
    """
    Main
    :return:
    """
    parser = argparse.ArgumentParser(description="Ipinfo")
    parser.add_argument("-d", "--daemon",
                        action="store_true",
                        help="run as a service")
    parser.add_argument("-s", "--single",
                        action="store_true",
                        help="single run and exit")
    parser.add_argument("-i", "--interval",
                        default="300",
                        help="run interval in seconds (default 300 sec.)")
    parser.add_argument("-f", "--file",
                        default="config.json",
                        help="config file (default ./config.json)")
    parser.add_argument("-v", "--version",
                        action='version',
                        version='%(prog)s 0.0.1')
    args = parser.parse_args()
    if args.single:
        single_run(args.file)
    elif args.daemon:
        daemon(args.file, args.interval)
    else:
        parser.print_help(sys.stderr)


if __name__ == '__main__':
    main()
