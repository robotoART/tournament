# tournament project
  This is my proof of concept swiss-tournament project. A postgresql database is used to track all players, matches, and stats.

  For more information please see:
  https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true

# Requirements
  ## Prerequisites
  You will need VirtualBox for your particular computer operating system in order to run a Virtual Machine (VM). Vagrant will be needed to setup the VM and run the python test program inside of that VM.

  Here are a few links to get you started:
  https://www.udacity.com/wiki/ud197/install-vagrant
  https://www.youtube.com/watch?v=djnqoEO2rLc
  https://www.vagrantup.com/docs/installation/

  ## Running on your local computer
  Using a command prompt such as Git Bash, change directory to the location of the "vagrant" folder. Start up the vagrant virtual machine and then login to it. Next, change directory to the location of the "tournament" folder. Now run the test program using the command "python tournament_test.py". Succesful result after running the programming will print out the following on the command prompt:

  1. countPlayers() returns 0 after initial deletePlayers() execution.
  2. countPlayers() returns 1 after one player is registered.
  3. countPlayers() returns 2 after two players are registered.
  4. countPlayers() returns zero after registered players are deleted.
  5. Player records successfully deleted.
  6. Newly registered players appear in the standings with no matches.
  7. After a match, players have updated standings.
  8. After match deletion, player standings are properly reset.
  9. Matches are properly deleted.
  10. After one match, players with one win are properly paired.
  Success!  All tests pass!


  ## Good to know
  It helps to know syntax for the following
  * Python2.7
  * Postgresql

# Collaborate
  Suggestions or bugs to improve can be posted at the project GitHub site.
  https://github.com/robotoART/tournament.git

# License
  This project is under the BSD 3-clause "New" or "Revised" License. Please see the file, included with this project, named "LICENSE" for more information.
