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


Setting the project early
=========================

By adding an additional section to the ``.workbench`` config file you
may specify the project when creating the timestamp already. Add a
section mapping a short key to the project's primary key as follows::

  [projects]
  admin = 42
  game = 70

Now, the first word of the notes can be used to set the project::

  tst admin Mails
