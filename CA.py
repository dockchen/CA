#!/usr/bin/env python
# coding: utf-8

# In[5]:
import argparse
from CA_util import CA_util_class

version_number = '1.0'
# In[7]:
def ParseCmdLine(cmd_line=None):
#{

    # https://docs.python.org/zh-tw/3/howto/argparse.html
    # https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse
    parser = argparse.ArgumentParser(description='Castle Age Automation')
    parser.add_argument('-v', '--version', action='version', version=version_number)
    parser.add_argument('-f', '--filename', type=str, default='CA_accounts_full.json')
    parser.add_argument('-10p', '--Reward_10P', default=False, action='store_true', help='Collect 10P battle reward')
    parser.add_argument('-100p', '--Reward_100P', default=False, action='store_true', help='Collect 100P battle reward')
    parser.add_argument('-CGB', '--Reward_CGB', default=False, action='store_true', help='Collect Classical GB reward')
    parser.add_argument('-DC', '--DailyClick', default=False, action='store_true', help='Daily clicks - Enable, Bless, Resource, Crystal...')
    parser.add_argument('-b', '--Blessing', type=int, choices=range(0, 6), help='Blessing - 0: profile; 1:Eng; 2:Atk; 3:Def; 4:Health; 5:STA')
    parser.add_argument('-CD', '--ConquestDuel', default=False, action='store_true', help='Auto Conquest Duel')
    
    parser.add_argument('-g', '--Guild', choices=['Any', 'YoPing', 'Fu', 'Lu'], default='Any', type=str, help='Specify guild to do actions')
    parser.add_argument('-sqd', '--Squad', type=int, choices=range(1, 11), action='append', help='Specify squads to do actions')
    

    #parser.add_argument('--verbose', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='ERROR', type=str, help='Level of information, default=%(default)s')
    #parser.add_argument('--test_mode', choices=['MS', 'S3', 'S4', 'WB', 'CB'], required=True, type=str, help='Test to run')
	#parser.add_argument('--delay_time', default=90, type=CheckPositive, help='Delay time between tests (secs) >0, default=%(default)s')
	#parser.add_argument('--cycle_count', default=1, type=CheckPositive, help='Number of cycles >0, default=%(default)s')
	#parser.add_argument('--sleep_time', default=60, type=CheckPositive, help='Sleep time (secs) >0, default=%(default)s')
	#parser.add_argument('--no_init', dest='init', default=True, action='store_false', help='Do not initialize script')
	#parser.add_argument('--no_timer', dest='timer', default=True, action='store_false', help='Do not use timer')
	#parser.add_argument('--no_setup', dest='setup', default=True, action='store_false', help='Do not setup test')
	#parser.add_argument('--cleanup', default=False, action='store_true', help='Only cleanup system files and exit')
	#parser.add_argument('--use_DASH_exe', default=False, action='store_true', help='Use installed DASH executables when possible, default=%(default)s')
	#parser.add_argument('--debug_script', default=False, action='store_true', help='Bypass sleep and boot system calls, default=%(default)s')
	#parser.add_argument('--no_connect', dest='connect', default=True, action='store_false', help='Do not connect to DASH')
    if cmd_line:
        args = parser.parse_args(cmd_line)
    else:
        args = parser.parse_args()

    print(args)
    return args
#}
# In[6]:

def Main(args):    
    CA = CA_util_class.CA_instance(args)
    CA.do_CA_actions()
    del CA
    return 1

if __name__ == '__main__':
	rc = -1
	args = ParseCmdLine()

	rc = Main(args)
	exit(rc)


# In[ ]:




