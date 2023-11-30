# NightSky

A simple hobby astronomy app for satellites, planets, stars, and Messier objects!

_Project created for CSC 512, the computer science capstone project, at Cornell College._

## About

NightSky is a desktop astronomy app that features tracking and notifications for certain kinds of objects.
It is designed to give simple information to a user, and assist them in locating objects in the night sky.
The NightSky app allows users to favorite objects to revisit them later and easily find them in the night sky.

NightSky is currently under development.

![A screenshot of the NightSky application.](./Resources/Screenshots/screenshot.png)

## Dependencies

NightSky uses several dependencies, namely PySide6's Qt binding for creation of the GUI. SkyField is also used for \
calculating the positions of objects in the night sky. Pandas is also used in the setup of the program.

## Setup

Begin by cloning this repository. Make sure you have correctly cloned all the GitLFS objects as well.
There are several that are necessary to fully set up the program.

Once you have cloned this repository, please navigate to the project directory and create a new Python virtual \
environment in the project directory like so:

```commandline
python -m venv
```

Then, activate the virtual environment however you need on your platform. On my computer, the venv is activated with \
the following command:

```commandline
source venv/bin/activate
```

Once the virtual environment has been activated, install the needed dependencies:

```commandline
pip install PySide6
pip install pandas
pip install skyfield
```

You must next compile the generated Qt files (.ui, .qrc) in order to create the Python superclasses and resource \
files that Qt needs. I have yet to automate this step as I have only very recently learned how to compile these files \
correctly.

Compile every Qt User Interface file with pyside6-uic by running the following commands on each `.ui` file. \
Remember to navigate to the directory containing only the `.ui` file beforehand.
To compile a file named `UiWidget.ui`:

```commandline
pyside6-uic UiWidget.ui -o UiWidget.py
```

Next, compile every Qt Resource File with pyside6-rcc. You must run this command on each `.qrc` file in the project.
Thankfully, there is only one.
To convert this one `.qrc` file, navigate to the project directory and run the following command:

```commandline
pyside6-rcc Resources/Icons.qrc -o Icons_rc.py
```

At this point, you should be able to run the program. But first, it would be a good idea to set up the data that the \
program relies on. Navigate to the `Tools` directory, then run each of the following commands to setup the database:

```commandline
python make_solarsystem_table.py
python make_messier_table.py
python make_hipparcos_table.py
```

Each of these may take some time to execute, so don't worry if they take a while.
Once you have finished this step, there should be a new file in the parent directory titled `nightsky.db`
This is the database that the program uses to keep track of your objects.

Additionally, there will now be a file titled `de421.bsp`, a JPL ephemeris file that NightSky uses with SkyField to \
predict the locations of planets as time progresses.

Finally, you are ready to start the application. Navigate to the project directory, and start `mainwindow.py` like so:
```commandline
python mainwindow.py
```

## Data Credits
Many different sources of data are used in this program.

* Firstly, for stars the Hipparcos dataset is used, and can be found at the University of Strasbourg: https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=1239/hip_main

* The compiled Messier catalog used to fill the database in this program was organized here: https://starlust.org/messier-catalog/

* The ephemeris files are provided by the Jet Propulsion Laboratory and can be located here: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/

* Satellite Two-Line Element sets are made available by Celestrak: https://celestrak.org/

* All icons reproduced in this program were created by [Delapouite](https://delapouite.com/) and uploaded to [game-icons.net](https://game-icons.net/). Delapouite has made \
them available under the CC BY 3.0 License: https://creativecommons.org/licenses/by/3.0/
They appear in this program with minor modifications.