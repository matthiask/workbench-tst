===========================================
Workbench Timestamps command-line interface
===========================================

Installation
============

1. Install `pipx <https://pipxproject.github.io/pipx/>`__
2. Install fh-fablib

   a. ``pipx install workbench-tst`` if you're happy with the packaged version
   b. ``pipx install --editable git+ssh://git@github.com/matthiask/workbench-tst.git@main#egg=workbench-tst`` otherwise

3. Create a file named ``.workbench`` in your home folder. It should
   contain the following settings (you can find the correct values for you
   by navigating to the Timestamps page and inspecting the
   Controller link)::

       [workbench]
       url = https://workbench.feinheit.ch/create-timestamp/
       user = email@example.org:HASH


Usage
=====

Stopping a task right now::

    tst stop                    # Bare stop
    tst stop one two three      # Including notes

Stopping some other time::

    tst stop -5                 # 5 Minutes ago
    tst stop 13:30              # At 13:30 exactly
    tst stop -10 one two three  # Splitting 10 minutes ago with notes
    tst stop +15                # Split in 15 minutes

Submitting starts::

    tst start
    tst start -5                # I started 5 minutes ago
    tst start -5 one two three  # I started 5 minutes ago with notes

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

    tst stop admin Mails
