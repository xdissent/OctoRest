.. |ss| raw:: html

   <strike>

.. |se| raw:: html

   </strike>

===========================
OctoRest
===========================

Python client library for OctoPrint REST API

This is continued work after the great start by Miro Hrončok of covering the
OctoPrint REST API. Nearly all current functionality in the API has been covered (up to OctoPrint 1.3.11),
but as of yet I have not had time to add extensive testing for all aspects of the API.

Installation
------------

The easiest way to install the package is via ``pip``::

    $ pip install octorest
    

Examples
--------

You may want a function which returns an instance of the OctoRest object connected to your printer.

.. code-block:: python

   def make_client(url, apikey):
        """Creates and returns an instance of the OctoRest client.
        
        Args:
            url - the url to the OctoPrint server
            apikey - the apikey from the OctoPrint server found in settings
        """
        try:
            client = OctoRest(url=url, apikey=apikey)
            return client
        except ConnectionError as ex:
            # Handle exception as you wish
            print(ex)
            
Once we have a client we can do many a cool thing with it!
For example the following retrieves all the G-code file names on your OctoPrint server and adds them to a string which is printed out.

.. code-block:: python

   def file_names(client):
        """Retrieves the G-code file names from the
        OctoPrint server and returns a string message listing the
        file names.
        
        Args:
            client - the OctoRest client
        """
        message = "The GCODE files currently on the printer are:\n\n"
        for k in client.files()['files']:
            message += k['name'] + "\n"
        print(message)

Maybe you want to stop your print and then subsequently home the printer. This is very simple to do using OctoRest!

.. code-block:: python

   def toggle_home(client):
        """Toggles the current print (if printing it pauses and
        if paused it starts printing) and then homes all of
        the printers axes.
        
        Args:
            client - the OctoRest client 
        """
        print("Pausing the print!")
        client.pause()
        print("Homing your 3d printer...")
        client.home()

Implemented features of OctoPrint REST API
------------------------------------------

A check list of the features currently implemented can be seen below.

* General information
    - Authorization
    - Login
    - Logout
* Version information
    - |ss| Version information |se|
* Apps
    - Session Keys (Deprecated since version 1.3.11: This functionality will be removed in 1.4.0.
        Use the Application Keys Plugin workflow instead.)
        - Obtaining a temporary session key
        - Verifying a temporary session key
* Connection handling
    - |ss| Get connection settings |se|
    - |ss| Issue a connection command |se|
        - |ss| Connect |se|
        - |ss| Disconnect |se|
        - |ss| Fake_ack |se|
* File operations
    - |ss| Retrieve all files |se|
    - |ss| Retrieve files from specific location |se|
    - |ss| Upload file or create folder |se|
    - |ss| Retrieve a specific file’s or folder’s information |se|
    - |ss| Issue a file command |se|
        - |ss| Select |se|
        - |ss| Slice |se|
        - |ss| Copy |se|
        - |ss| Move |se|
    - |ss| Delete file |se|
* Job operations
    - |ss| Issue a job command |se|
        - |ss| Start |se|
        - |ss| Cancel |se|
        - |ss| Restart |se|
        - |ss| Pause |se|
            - |ss| Pause |se|
            - |ss| Resume |se|
            - |ss| Toggle |se|
    - |ss| Retrieve information about the current job |se|
* Languages
    - |ss| Retrieve installed language packs |se|
    - |ss| Upload a language pack |se|
    - |ss| Delete a language pack |se|
* Log file management
    - |ss| Retrieve a list of available log files |se|
    - |ss| Delete a specific logfile |se|
* Printer operations
    - |ss| Retrieve the current printer state |se|
    - |ss| Issue a print head command |se|
        - |ss| Jog |se|
        - |ss| Home |se|
        - |ss| Feedrate |se|
    - |ss| Issue a tool command |se|
        - |ss| Target |se|
        - |ss| Offset |se|
        - |ss| Select |se|
        - |ss| Extrude |se|
        - |ss| Flowrate |se|
    - |ss| Retrieve the current tool state |se|
    - |ss| Issue a bed command |se|
        - |ss| Target |se|
        - |ss| Offset |se|
    - |ss| Retrieve the current bed state |se|
    - |ss| Issue a chamber command |se|
        - |ss| Target |se|
        - |ss| Offset |se|
    - |ss| Retrieve the current chamber state |se|
    - |ss| Issue an SD command |se|
        - |ss| Init |se|
        - |ss| Refresh |se|
        - |ss| Release |se|
    - |ss| Retrieve the current SD state |se|
    - |ss| Send an arbitrary command to the printer |se|
* Printer profile operations
    - |ss| Retrieve all printer profiles |se|
    - Add a new printer profile
    - Update an existing printer profile
    - |ss| Remove an existing printer profile |se|
* Settings
    - |ss| Retrieve current settings |se|
    - |ss| Save settings |se|
    - Regenerate the system wide API key
    - Fetch template data (in beta)
* Slicing
    - |ss| List All Slicers and Slicing Profiles |se|
    - |ss| List Slicing Profiles of a Specific Slicer |se|
    - |ss| Retrieve Specific Profile |se|
    - Add Slicing Profile
    - |ss| Delete Slicing Profile |se|
* System
    - |ss| List all registered system commands |se|
    - |ss| List all registered system commands for a source |se|
    - |ss| Execute a registered system command |se|
* Timelapse
    - |ss| Retrieve a list of timelapses and the current config |se|
    - |ss| Delete a timelapse |se|
    - |ss| Issue a command for an unrendered timelapse |se|
        - |ss| Render |se|
    - |ss| Delete an unrendered timelapse |se|
    - |ss| Change current timelapse config |se|
* User
    - |ss| Retrieve a list of users |se|
    - |ss| Retrieve a user |se|
    - |ss| Add a user |se|
    - |ss| Update a user |se|
    - |ss| Delete a user |se|
    - |ss| Reset a user’s password |se|
    - |ss| Retrieve a user’s settings |se|
    - Update a user’s settings
    - |ss| Regenerate a user’s personal API key |se|
    - |ss| Delete a user’s personal API key |se|
* Util
    - |ss| Test paths or URLs |se|
        - |ss| Path |se|
        - |ss| URL |se|
        - |ss| Server |se|
* Wizard
    - |ss| Retrieve additional data about registered wizards |se|
    - |ss| Finish wizards |se|

Copyright & License
-------------------

Copyright (c) 2016-2017 `Miro Hrončok <miro@hroncok.cz/>`_. MIT License.

Copyright (c) 2017 `Jiří Makarius <meadowfrey@gmail.com/>`_. MIT License.

Copyright (c) 2018-2019, `Douglas Brion <me@douglasbrion.com/>`_. MIT License.
