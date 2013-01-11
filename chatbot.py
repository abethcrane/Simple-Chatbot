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

def SendEmail(recipient, subject, body, sender):     
    '''Sends an e-mail to the specified recipient.'''
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    #body = "" + body + ""  # why?
     
    if sender is not "" and sender is not None:
        from_addr = email + " via " + str(sender)
    else:
        from_addr = email
        
    print from_addr
    headers = ["From: " + from_addr,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(email, password)
     
    session.sendmail(email, recipient, headers + "\r\n\r\n" + body)
    session.quit()

#########################################################################################

class SampleBot(GtalkRobot):

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

    #This method is used to send email for users.
    def command_002_SendEmail(self, user, message, args):
        #email blah@gmail.com "hello blah" "nice to meet you"
        '''(email|mail|em|m)\s+(.*?@.+?)\s+(.*?),\s*(.*)(?i)'''
        user_email = re.sub("\/.*", "", str(user))
        email_addr = args[1]
        subject = args[2]
        body = args[3]
        body = body + "\n\nSent from a Chatbot via " + user_email
        SendEmail(email_addr, subject, body, user_email)
        
        self.replyMessage(user, "\nEmail sent to "+ email_addr +" at: "+time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))

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
