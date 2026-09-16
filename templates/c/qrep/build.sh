#!/bin/bash

gcc main.c $(pkg-config --cflags --libs glib-2.0) -o qrep

