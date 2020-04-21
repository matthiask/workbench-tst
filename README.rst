===========================================
Workbench Timestamps command-line interface
===========================================

Installation
============

::

   [sudo] ./setup.py install


Create a file named ``.workbench`` in your home folder. It should
contain the following settings (you can find the correct values for you
by navigating to the Timestamps page and inspecting the
Controller link)::

   [workbench]
   url = https://workbench.feinheit.ch/create-timestamp/
   user = email@example.org:HASH


Usage
=====

Splitting right now::

    tst split              # Bare split
    tst one two three      # Including notes

Splitting some other time::

    tst -5                 # 5 Minutes ago
    tst 13:30              # At 13:30 exactly
    tst -10 one two three  # Splitting 10 minutes ago with notes
    tst +15                # Split in 15 minutes

Submitting other types::

    tst stop
    tst start
    tst start -5           # I started 5 minutes ago

Show today's timestamps::

    tst list

Show help::

    tst
    tst help
