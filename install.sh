echo "This is the Ubuntu-Airplay installer for Ubuntu and other debian-based systems."
sleep 1
echo "We are about to install required Python libraries, please enter your password when prompted."
sleep 2
echo "sudo apt-get install libavahi-compat-libdnssd-dev ruby rubygems-integration python3 python3-pyqt4 python3-qt4"
sudo apt-get install libavahi-compat-libdnssd-dev ruby rubygems-integration python3 python3-pyqt4 python3-qt4
echo "Required system packages have been installed."
echo "We will now install the required Ruby Gem"
sleep 3
echo "sudo gem install airplay"
sudo gem install airplay
echo "You can now run the program using run.sh."
