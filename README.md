Pluralnotes is a simple, terminal-based notebook utility designed with plural people in mind. It allows you to create multiple users on the same OS user, making it easy to keep several people's notes separate without ever logging off on the OS level. It includes a shared directory for keeping group notes or communicating, and an archive directory for the notes of deleted users.

Notes can be created with your preferred editor, edited, deleted, viewed, and searched. They can also be exported as a ZIP file for easy backups. The default text editors are nano for Un*x operating systems and Notepad for Windows (as Windows unfortunately lacks a default command line editor), but this easily can be changed to suit your preferences in the settings.

Users can be added, renamed, deleted, and searched through. There is no upper limit to the number of users you can have other than your disk's storage space. Users each have their own personal directory for personal notes in addition to the shared and archived notes directories.

Pluralnotes is written in Python 3. It works on Linux and Windows for certain, and should theoretically run on MacOS as well. You can download the latest executables <a href="https://github.com/candlebrae/pluralnotes/releases">here</a>.

If you'd like, it can be run from source with <code>python (path to pluralnotesapp.py)</code>. Make sure all three .py files are in the same directory! It requires the colorama module for adding color on the command line; if you don't have the colorama module installed, you can install it with pip via <code>pip install colorama</code>. All other modules should be contained within Python's default installation.
