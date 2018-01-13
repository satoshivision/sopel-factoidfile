#
# Serve simple factoids from files.
# v0.1 (work in progress, untested, insecure, review before use!)
# (C) Copyrighted rfree 2017, BSD 3-clause Licence.
#
# https://github.com/satoshivision/sopel-factoidfile
#

import sopel.module
import os.path
import re

cfg_dir_factoids = '~/sopel-factoidfile/factoids-bitcoins/' # directory with the factoid files


def info_user_error(bot,trigger,msg):
    bot.say('Error: '+msg, trigger.nick);

def check_filename_normal_no_parent(fn):
    if not bool(re.match('^[a-zA-Z0-9_-]+$',fn)): return False # not alnum (with few extra characters)
    if bool(re.match('\.\.',fn)): return False # something stargin with ".." (danger!) or strange with ".." in midle
    if bool(re.match('^/',fn)): return False # absolute path not allowed
    if bool(re.match('^\.',fn)): return False # starting with a hidden dir not allowed
    if bool(re.match('^/\.',fn)): return False # hidden subfile/subdir "foo/.hide"
    return True

def search_factoid_filename(factoid_name, db_dir):
    fn = db_dir + factoid_name
    if (os.path.isfile(fn)): return fn;
    fn = db_dir + factoid_name.upper()
    if (os.path.isfile(fn)): return fn;
    fn = db_dir + factoid_name.lower()
    if (os.path.isfile(fn)): return fn;
    return "" # no factoid found

def use_factoid(bot,trigger,factoid_name,target_users):
    # bot.replay("factoid name="+factoid_name)
    if (not check_filename_normal_no_parent(factoid_name)):
        info_user_error(bot,trigger,"Invalid factoid file name ("+factoid_name+")")
        return False
    try:
        factoid_fn = search_factoid_filename(
            factoid_name + '.txt',
            os.path.expanduser(cfg_dir_factoids) + '/'
         )
        if (not os.path.isfile(factoid_fn)):
            info_user_error(bot,trigger,'No such factoid named '+factoid_name
                +'. Ask me about: edit e.g. with `edit (best in private message)')
            return False
        with open(factoid_fn, 'r') as myfile:
            factoid_text=myfile.read().replace('\n',' ').replace('\r',' ')
        factoid_text = re.sub('[ ]+',' ',factoid_text); # normalize whitespace
        factoid_text = factoid_text.strip()
        if (len(factoid_text)<1):
            info_user_error(bot,trigger,"Factoid was empty ("+factoid_name+")")
            return False
        reply=""
        if len(target_users)>0:
            reply = target_users + ': ';
        reply = reply + factoid_text;
        bot.say(reply) # <---
    except Exception as e:
        info_user_error(bot,trigger,"Exception processing the factoid file: " + str(e)
            + " for factoid ["+factoid_name+"]")
        return False
    return True

def try_factoid(bot,trigger):
    try:
        factoid_name = trigger.group(1)
        target_users=""
        try:
            target_users = trigger.group(2)
        except:
            target_users=""
            # info_user_error(bot,trigger,"no group 2")
    except Exception as e:
        info_user_error(bot,trigger,"Exception processing the factoid command"
            + ": " + str(e)
            + " for factoid ["+factoid_name+"]")
        return False
    use_factoid(bot,trigger,factoid_name,target_users)

# Trigger on "`factoid"  or "`factoid user" or "`factoid user otherusers"
@sopel.module.rule('^`([^`][^ ]*)[ ]*(.*)$')
def trigger_try_factoid(bot, trigger):
    try_factoid(bot,trigger)

