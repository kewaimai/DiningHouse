#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiningHouse.settings")

    from django.core.management import execute_from_command_line
    # from django_crontab.management.commands.crontab import Command


    execute_from_command_line(sys.argv)

