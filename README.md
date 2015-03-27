ubuntu-airplay 0.0.22 !frozen
===

I have always been annoyed about how iOS, Mac OSX, and all of Apples proprietary hardware/software has inhibited so many of us technology savvy people.  

Project Status:
---
The GUI is mostly working and I have basic Python to Ruby things figured out.  
Now I'm waiting on [this issue](https://github.com/elcuervo/airplay/issues/70#issuecomment-85132968) to be resolved so that I can load the full list of Airplay Receivers as options.

Project Details:
---
Right now it's Python 2 & 3 using the QT system from PyQt4.  
It is made to support Ubuntu only, but I'm trying to make this thing OS-independent.  
From my last testing, this ran fine on my Dad's Windows 8 laptop.

Requirements:
---
See the `dependencies.md` file for installing the needed software.

Why I'm doing this:
---
I go to a school where everyone has iPads as their learning tool, which are horrid for coding/programming and software development, but make a good classroom common tool. As a result, there is an Apple TV in every single room for the students to quickly present whatever is on their screen, and the teachers can show their presentations with their assigned Macbooks.

I am one of two people at this school who use Linux (Ubuntu) and who bring their laptops every day. I use mine for school work fairly often, as I understand how much I can do in Linux and not iOS. But whenever some task comes up where I'd need to airplay my work to an Apple TV, I'm being restrained to my iPad.

What this aims to be:
---
This application is designed to sit in your System Tray just like in OSX, with a drop down list of available Airplay Recievers, and allow you to:
- Stream your desktop
- Send a photo/picture
- Play a video
- Stream Music  
And whatever else the users and developers of this project wish it to be.
