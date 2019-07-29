#!/usr/bin/sh

pybabel extract alarmbot/*.py -o locales/alarmbot.pot
pybabel init -i locales/alarmbot.pot -d locales -D alarmbot -l vi
