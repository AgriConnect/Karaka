#!/usr/bin/sh

pybabel extract alarmbot/*.py -o locales/karaka.pot
pybabel init -i locales/karaka.pot -d locales -D karaka -l vi
