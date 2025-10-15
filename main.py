#!/usr/bin/python3

#  main.py

import config
from mainwindow import MainWindow
from dict import Dict

def main():
	config.DICT = Dict()
	config.MAINWINDOW = MainWindow(config.ASSETS_DIR, config.ICON_FILE, config.DATA_DIR, config.DICT)
	config.MAINWINDOW.run()


if __name__ == '__main__':
	main()
