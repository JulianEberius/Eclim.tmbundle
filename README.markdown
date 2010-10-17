**Eclim.tmbundle**
===========================

Brings Eclipse Java completion powers (and other neat JDT stuff) to TextMate by integrating with [Eclim](http://eclim.org/).

Eclim adds a server component to Eclipse that makes a lot of it's IDE features 
available to the outside. Eclim was created to integrate Vim and Eclipse, but the Eclipse plugin can
in principle support other editors as well.

Copyright (C) 2010 Julian Eberius

INSTALLATION
-------------
First you need an Eclipse installation (including the JDT of course).

Then install Eclim from [eclim.org](eclim.org).

**Update:** You'll also need to set an environment variable named ECLIM in TM to point
to the eclim script, which is located in your Eclipse directory after installing Eclim.
So in TextMate->Preferences->Advanced->Shell_Variables add a variable ECLIM with a value
"/YOUR_ECLIPSE_DIR/eclim".

USAGE
-----

Start Eclipse, either normally or using the headless (no GUI) variant that Eclim provides.
I would recommend the normal way for now, as Eclim.tmbundle has not implemented all
the project management functions that Eclim provides, so you'll need the Eclipse GUI 
for that anyway. I prefer to start Eclipse normally, then minimize it and use TextMate for coding.

**IMPORTANT:** if you're using the GUI, open the "eclimd" view. The eclimd server inside Eclipse is
only started if you open this view. This is just how eclim works.

To work on an Eclipse project in TM, just open the project folder. You can then use

* Ctrl-Space to get Eclipse's completions
* Cmd-Shift-I to import the class under the cursor (the bundle does not automatically do that when you autocomplete-insert a new class like Eclipse does)
* Cmd-F3 to go to the definition of the thing under the cursor
* Saving a document with Cmd-S will make Eclipse compile in the background. A clickable panel will popup to show you Eclipse's compilation errors.
* Cmd-Esc (Eclipse's Cmd-1 is alredy used by TM) on a line with an error to get code corrections.
 
The first time you invoke one of the functions, it may take 2-4 seconds, subsequent times it will be just as fast as with Eclipse itself.


ISSUES
------
- For now, the popups (errors and corrections) have to be double clicked, hitting Return does not work.

- From time to time there are problems with different line endings when using
files created or edited on Windows. When the completion does not work, or a 
correction operation puts the whole code on one line in TM, it is usually a line
ending problem. So for now, this is best used with matching line endings in TM,
Eclipse, and the files edited.


LICENSE
-------
MIT License (see LICENSE.txt)