#!/usr/bin/python

from PyGtalkRobot import GtalkRobot
import csv
import re
import sys
import time
import gdata.spreadsheet.service

email = 'email'
password = 'password'
# Find this value in the url with 'key=XXX' and copy XXX below
spreadsheet_key = 'spreadsheet key'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = 'od6'

gs_client = gdata.spreadsheet.service.SpreadsheetsService()
gs_client.email = email
gs_client.password = password
gs_client.ProgrammaticLogin()


def EditSpreadsheet(items, email):
    data = {}
    for row in items:
        data['date'] = time.strftime('%m/%d/%Y')
        data['time'] = time.strftime('%H:%M:%S')
        data['item'] = row
        data['email'] = email
        gs_client.InsertRow(data, spreadsheet_key, worksheet_id)

#########################################################################################

class SampleBot(GtalkRobot):
    
    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == 'admin@email.com':
            print jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid)
            self.setState(show, status)
            self.replyMessage(user, "State settings changed!")

    def command_003_AddItem(self, user, message, args):
        '''add\((.*)\)'''
        email = re.sub("\/.*", "", str(user))
        EditSpreadsheet(args, email)
        self.replyMessage(user, "Added '%s' as an item" % (args[0]))
    
    #This method is used to response users.
    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))



#########################################################################################
if __name__ == "__main__":
    bot = SampleBot()
    bot.setState('available', "Add agenda items to me - add([^\\n]*)")
    bot.start(email, password)
