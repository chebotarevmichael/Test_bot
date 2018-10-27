#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"This script is intended for testing purposes"

from bot.analyze import *

while True:
    data = input("> ").split()
    if len(data) == 2:
        process(data[0], int(data[1]))
    elif len(data) == 1:
        go_back(int(data[0]))
