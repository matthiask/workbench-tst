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

::

   tst split
   # OR
   tst split 12:34
   # OR
   tst stop Yay I finished work
   # OR
   tst start 09:00 Oops I forgot to press start at the right time
   # OR ('split' is the default)
   tst Just some notes
