ubuntu-airplay
===

I have always been annoyed about how iOS, Mac OSX, and all of Apples proprietary hardware/software has inhibited so many of
us technology savvy people.  

Why I'm doing this:
---
I go to a school where everyone has iPads as their learning tool, which are horrid for coding/programming and software
development, but make a good classroom common tool. As a result, there is an Apple TV in every single room for the students to
quickly present whatever is on their screen, and the teachers can show their presentations with their assigned Macbooks.

I am one of two people at this school who use Linux (Ubuntu) at this school and who bring their laptops every day. I use mine
for school work fairly often, as I understand how much I can do in Linux and not iOS. But whenever some task comes up where I'd
need to airplay my work to an Apple TV, I'm being restrained to my iPad.

What this aims to be:
---
This application is designed to sit in your System Tray just like in OSX, with a drop down list of available Airplay Recievers,
and allow you to:
- Stream your desktop
- Send a photo/picture
- Play a video
- Stream Music  
And whatever else the users and developers of this project wish it to be.

Project Details:
---
Right now it's Python 3 using the QT system from PyQt4.  
It is made to support Ubuntu only, but I'm trying to make this thing OS-independent.

Requirements:
---
- PyQt4
- Rython
  - Rython for Python 2 is `pip install rython`
  - Rython for Python 3 is included with this project from https://github.com/fbauer/rython
    - Use `python3 setup.py install` from the rython-master directory to install it, `pip3 install rython` does not work properly.
