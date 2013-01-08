chatbot
=======

Simple Spreadsheet Editing Chatbot; I use it to add agenda items to a spreadsheet four our society.

The entire chatbot principle operates off pygtalk. The spreadsheet adding aspect required reading a couple of different sources and combining lines from here and there (and writing a few of my own :P)

It's not a huge project, and the chatbot uses a regex on each line (defined as until a \n) to determine what functions to call.

Currently the username/password are hardcoded in.

Code Research/Sources:
http://code.google.com/p/pygtalkrobot/
http://pseudoscripter.wordpress.com/2011/05/20/automatically-update-spreadsheets-and-graphs-part-2/
http://www.mattcutts.com/blog/write-google-spreadsheet-from-python/
http://gdata-python-client.googlecode.com/hg/pydocs/gdata.spreadsheet.service.html
