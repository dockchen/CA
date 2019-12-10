#!/usr/bin/env python
# coding: utf-8
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.options import Options

import datetime
import pytz
import random

#from selenium.common.exceptions import *
import time
#import json
#import pyautogui

# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
from CA_util import CA_log

class CA_instance:
    CA_pages = {
            'Home': 'https://web3.castleagegame.com/castle_ws/index.php',
            'Login': 'https://web3.castleagegame.com/castle_ws/connect_login.php',
            'LogOut': 'https://web3.castleagegame.com/castle_ws/connect_login.php?platform_action=CA_web3_logout',
            'Keep': 'https://web3.castleagegame.com/castle_ws/keep.php',
            'Collect_Classic_GB_Template': 'https://web3.castleagegame.com/castle_ws/guild_battle.php?action=collect_battle&attacker_guild_id={}&defender_guild_id={}&battle_type=2000&is_attacker={}&ajax=1',
            'mystical_emporium': 'https://web3.castleagegame.com/castle_ws/mystical_emporium.php',
            'mystical_emporium_buy_Template': 'https://web3.castleagegame.com/castle_ws/mystical_emporium.php?action=buy_goods&goods_id={}&buy_fresh_count=0&ajax=1',            
            'Resource': 'https://web3.castleagegame.com/castle_ws/index.php?action=conquestResourceCollectHeader&ajax=1&ajax=1',
            'Crystal': 'https://web3.castleagegame.com/castle_ws/index.php?action=conquestDemiCollectHeader&ajax=1&ajax=1',
            'Enable': 'https://web3.castleagegame.com/castle_ws/index.php?action=enableItemArchiveBonusHeader&ajax=1&ajax=1',
            'Bless_Template': 'https://web3.castleagegame.com/castle_ws/symbolquests.php?symbol={}&action=tribute&ajax=1&ajax=1',
            'Reward_100P':'https://web3.castleagegame.com/castle_ws/hundred_battle_view.php?action=collect_battle&attacker_guild_id=100000450039200_1282860245&defender_guild_id=1355667530_1282912208&battle_type=hundred&is_attacker&ajax=1'
            }
    #CA_actions = {
    #        'Reward_10P': 0,
    #        'Reward_100P': 0,
    #        'Reward_CGB': 0,
    #        'Bonus': 0,
    #        'Blessing': 0,
    #        'DailySpin': 0,
    #        'Resource': 0,
    #        'Crystal': 0,
    #        'mystical_emporium': 0,
    #        'DailyClick': 0,
    #        }
    
    #CA_user_prop = {
    #        'NO': 0,
    #        'Name': '',
    #        'Email': '',
    #        'PWD': '',
    #        'Guild': '',
    #        'DailyClick': 0,
    #        'Blessing': 0,
    #        'Reward_100P': 0,
    #        'Reward_10P': 0,
    #        'Reward_CGB': 0
    #        }
    
    # Properties with default value
    chrome_path = r".\WebDriver\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
       
    implicitly_wait_time = 3
    max_wait_time = 5
    
    # Define log level
    # Log levels: NOTSET DEBUG INFO WARNING ERROR CRITICAL
    log = CA_log.CALog()
    #log.basicConfig(level=log.DEBUG,format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log.setLevel(10)

    #CA_Bless_URL = CA_pages('Home') + 'symbolquests.php?symbol={}&action=tribute&ajax=1&ajax=1'.format(blessing_goal)
    logged_in = 0
    
    #default bless goal
    # Bless goal
    # 1: Energy
    # 2: Attack
    # 3: Defense
    # 4: Health
    # 5: Stamina
    #bless_goal = 2

    #with open('CA_accounts_full.json', 'r') as f:
    #    CA_user_prop = json.load(f)

    # Constructor
    def __init__(self, args):
        # Test code for Chrome options
        # ref - https://blog.taiker.space/how-to-add-chrome-extension-in-selenium-at-runtime/
        # ref - https://intoli.com/blog/chrome-extensions-with-selenium/
        # ref - https://chrome-extension-downloader.com/
        # ref - http://coreygoldberg.blogspot.com/2018/09/python-using-chrome-extensions-with.html
        # ref - https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions
        options = Options()
        #packed_extension_path = 'C:\Chrome Extension\Swap-My-Cookies_v0.3.crx'
        #options.add_extension(packed_extension_path)
        #self.driver = webdriver.Chrome(self.chrome_path, chrome_options=options)
        
        #options = options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu')
        #options.add_argument('--headless')
        options.add_argument("disable-infobars")
        options.add_argument("start-maximized")
        #options.add_argument('--remote-debugging-port=9222')
        
        self.driver = webdriver.Chrome(self.chrome_path, chrome_options=options)
        self.driver.implicitly_wait(self.implicitly_wait_time)  # 隐性等待，最长等delay_between_actions秒
        
        #self.driver.execute_script('window.innerWidth = screen.width/2; window.screenX=screen.width/2;')
        
        #self.driver.maximize_window()
        #time.sleep(3)
        size = self.driver.get_window_size()
        self.driver.set_window_size(size['width']/2, size['height'])
        self.driver.set_window_position(size['width']/2-13, 0)
        self.driver.execute_script('window.focus()')
        
        # https://stackoverflow.com/questions/57298901/unable-to-hide-chrome-is-being-controlled-by-automated-software-infobar-within
        # https://sites.google.com/a/chromium.org/chromedriver/capabilities
        # https://peter.sh/experiments/chromium-command-line-switches/
        # https://stackoverflow.com/questions/48467961/possible-to-open-display-render-a-headless-selenium-session

        # https://xiang1023.blogspot.com/2017/09/python-pyautogui.html
        #self.driver.execute_script('window.focus()')
        #pyautogui.hotkey('winleft', 'right')

        #self.driver.execute_script('window.focus();')
        #time.sleep(1)
        #pyautogui.PAUSE = 1
        #pyautogui.FAILSAFE = True
        #pyautogui.keyDown('winleft')
        #pyautogui.press('right')
        #pyautogui.keyUp('winleft')        
        #pyautogui.typewrite('esc')
        
        #self.driver.minimize_window()
        #self.clear_CA_actions()
        self.args = args
        self.bqh = ''
        with open(args.filename, 'r') as f:
            self.CA_user_prop = json.load(f)
        return
    
    # Desstructor
    def __del__(self):
        self.driver.close()
        self.driver.quit()
        return

    # Replaced by args
    #def clear_CA_actions(self):
    #    self.CA_actions['Reward_10P'] = 0
    #    self.CA_actions['Reward_100P'] = 0
    #    self.CA_actions['Reward_CGB'] = 0
    #    self.CA_actions['Bonus'] = 0
    #    self.CA_actions['Blessing'] = 0
    #    self.CA_actions['DailySpin'] = 0
    #    self.CA_actions['Resource'] = 0
    #    self.CA_actions['Crystal'] = 0
    #    self.CA_actions['mystical_emporium'] = 0

    # replaced by CA_user_prop which read user profile from json file
    def clear_CA_user_prop(self):
    #    self.CA_user_prop['NO'] = 0
    #    self.CA_user_prop['Name'] = ''
    #    self.CA_user_prop['Email'] = ''
    #    self.CA_user_prop['PWD'] = ''
    #    self.CA_user_prop['Guild'] = ''
    #    self.CA_user_prop['DailyClick'] = 0
    #    self.CA_user_prop['Blessing'] = 2
    #    self.CA_user_prop['Reward_100P'] = 0
    #    self.CA_user_prop['Reward_10P'] = 0
    #    self.CA_user_prop['Reward_CGP'] = 0
        #if (self.logged_in):
        #    self.log_out()
        self.logged_in = 0
        self.bqh = ''
    
    # Login CA
    def log_in(self, player_email, player_password):
        try:
            log = self.log            
            if (self.logged_in):
                log.info('OK - LOGIN Already - {}'.format(self.driver.current_url))
                return 0
            
            # If Email/Password available, login
            # Retrieve log in page of Castle Age
            ##self.driver.get(self.CA_pages['Login'])    
            #if (self.driver)
            #locator = (By.NAME, 'player_email')
            #WebDriverWait(self.driver, self.max_wait_time, 0.5).until(EC.presence_of_element_located(locator))
            ##WebDriverWait(self.driver, self.max_wait_time, 0.5)                        
            
            self.websurf(self.CA_pages['Login'])
            
            q = self.driver.find_element_by_name('player_email')
            q.clear()
            q.send_keys(player_email)

            q = self.driver.find_element_by_name('player_password')
            q.clear()
            q.send_keys(player_password)

            q.send_keys(Keys.RETURN)
            #time.sleep(delay_between_actions)

            # Check if logged in successfully
            # Check "Logout" link on the top right corner
            locator = (By.PARTIAL_LINK_TEXT, 'Logout')
            WebDriverWait(self.driver, self.max_wait_time, 0.5).until(EC.presence_of_element_located(locator))
            if (self.driver.current_url.find(self.CA_pages['Home'])>=0):
                #log.info('OK - LOGIN - {}'.format(self.driver.current_url))
                pass
            else:
                log.info('NG - LOGIN - {}'.format(self.driver.current_url))
            
            q = self.driver.find_element_by_name('bqh') 
            #bqh = q.get_attribute('value')
            self.bqh = q.get_property('value')

            # Try to get username from loaded page
            #q = self.driver.find_element_by_xpath('//*[@id="main_bntp"]')
            #username = q.text.split('|')[-1].split(' ')[2]
            #log.info('OK - Welcome! {}'.format(username))
            self.logged_in = 1
            return 1
        except TimeoutException:
            log.error('NG - Time out - log_in')
        except NoSuchElementException:
            log.error('NG - No Such Element Exception - log_in')
        except:
            log.error('NG - Already logged in Castle Age or wrong Email/Password - log_in')
            return 0

    def log_out(self):
        # Logged out
        try:
            log = self.log
            # Method 1
            #q = driver.find_element_by_partial_link_text('Logout')
            #q.click()

            # Method 2
            self.driver.get(self.CA_pages['LogOut'])    
            locator = (By.NAME, 'player_email')

            WebDriverWait(self.driver, self.max_wait_time, 0.5).until(EC.presence_of_element_located(locator))
            #WebDriverWait(driver, max_wait_time, 0.5).until(EC.title_is(CA_Login_URL))
            #log.info('Title: ' + driver.title)
            #self.logged_in = 0
            self.clear_CA_user_prop()
            #log.info('OK - LOGGED OUT')

        except TimeoutException:
            log.error('NG - Time out - log_out')
        except NoSuchElementException:
            log.error('NG - No Such Element Exception - log_out')
        except:
            log.error('NG - FAIL TO LOGGED OUT - log_out')

    def enable_bonus(self):
        try:
            log = self.log
            
            # Method 1
            driver = self.driver
            driver.get(self.CA_pages['Enable'])
            
            # Method 2
            #q = self.driver.find_element_by_name('Enable Bonus!')
            #q.click()
            
            WebDriverWait(driver, self.max_wait_time, 0.5)  

            q = driver.find_element_by_xpath('//*[@id="results_main_wrapper"]/div/div/span')            
            #WebDriverWait(driver, self.max_wait_time, 0.5)            
            if (q.text.find("Error")>=0):
                log.info('NG - BONUS - {}'.format(q.text))
            else:
                log.info('OK - BONUS - {}'.format(q.text))
            #log.info('OK - Enable Bonus!')
            #time.sleep(self.delay_between_actions)
        except TimeoutException:
            log.error('NG - Time out - enable_bonus')
        except NoSuchElementException:
            log.error('NG - No Such Element Exception - enable_bonus')
        except:
            log.error('NG - NOT ABLE TO Enable Bonus! - enable_bonus')

    # Bless goal
    # 1: Energy
    # 2: Attack
    # 3: Defense
    # 4: Health
    # 5: Stamina
    def bless(self, goal):
        try:
            # Force to bless 'Stamina' on Saturday (weekday=5)
            # Ref - https://www.itread01.com/content/1542339684.html
            t = datetime.datetime.now(pytz.timezone('US/Pacific'))
            if (t.weekday() == 5):
                goal = 5
 
            log = self.log
            driver = self.driver
            driver.get(self.CA_pages['Bless_Template'].format(goal))
            #locator = (By.ID, 'results_main_wrapper')
            #WebDriverWait(driver, self.max_wait_time, 0.5).until(EC.presence_of_element_located(locator))
            WebDriverWait(driver, self.max_wait_time, 0.5)
            q = driver.find_element_by_xpath('//*[@id="results_main_wrapper"]/div/div/span')            
            #WebDriverWait(driver, self.max_wait_time, 0.5)
            if (q.text.find("You cannot pay another tribute so soon")>=0):
                log.info('NG - BLESS - {}'.format(q.text))
            else:
                log.info('OK - BLESS - {}'.format(q.text))
            #log.info("OK - Bless Successfully")
        except TimeoutException:
            log.error('NG - Time out - bless')
        except NoSuchElementException:
            log.error('NG - No Such Element Exception - bless')
        except:
            log.error('NG - Bless - Something went wrong - bless')
        
        #try:
        #    q = self.driver.find_element_by_name('symbolsubmit')
        #    q.click()
        #    WebDriverWait(self.driver, self.max_wait_time, 0.5)
        #    log.info('OK - symbolsubmit clicked')
        #    #time.sleep(self.delay_between_actions)
        #except:
        #    log.info('NG - NOT ABLE TO click symbolsubmit')    

    def daily_spin(self):
        try:
            log = self.log
            driver = self.driver
            driver.get(self.CA_pages['Home'])
            WebDriverWait(driver, self.max_wait_time, 0.5)
            
            q = driver.find_element_by_xpath('//*[@id="newsFeedSection"]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/a/img')
            imgsrc = q.get_property('src').split('/')[-1]
            if (imgsrc == "news_btn_join.gif"):
                q.click()
                WebDriverWait(driver, self.max_wait_time, 0.5)
                log.info('OK - DAILY SPIN')
                #time.sleep(self.delay_between_actions)
            else:
                log.info('NG - DAILY SPIN')
        except TimeoutException:
            log.error('NG - Time out - daily_spin')
        except NoSuchElementException:
            log.error('NG - No Such Element Exception - daily_spin')
        except:
            log.error('NG - NOT ABLE TO Daily Spin - daily_spin')

    def resource(self):
        try:
            log = self.log
            # Way 1 - visit resource page directly
            log = self.log
            driver = self.driver
            driver.get(self.CA_pages['Resource'])
            
            # Way 2 - to find and click resource button
            # q = self.driver.find_element_by_css_selector('div:nth-child(4) > div > div > div > form > .imgButton')
            # q.click()            
            # WebDriverWait(self.driver, self.max_wait_time, 0.5)
            
            # retrieve feedback from Castle Age
            q = driver.find_element_by_xpath('//*[@id="results_main_wrapper"]/div/div/span')            
            WebDriverWait(driver, self.max_wait_time, 0.5)
            str_result = q.text
            if (str_result.find("There are currently no resources to collect.")>=0):
                log.info('NG - RESOURCE - {}'.format(str_result))
            elif (str_result.find("You have already collected today!")>=0):
                log.info('NG - RESOURCE - {}'.format(str_result))
            else:
                log.info('OK - RESOURCE - {}'.format(str_result))

            #log.info('OK - Resource clicked')
            #time.sleep(self.delay_between_actions)
        except TimeoutException:
            log.error('NG - Time out - resource')
        except NoSuchElementException:
            log.error('NG - NOT ABLE TO Collect Resource - resource')
        except:
            log.error('NG - Something wrong - resource')

    def crystal(self):
        try:
            log = self.log
            driver = self.driver
            
            # Way 1
            driver.get(self.CA_pages['Crystal'])
            
            # Way 2
            #q = self.driver.find_element_by_css_selector('div:nth-child(5) form > .imgButton')
            #q.click()
            
            #WebDriverWait(self.driver, self.max_wait_time, 0.5)
            
            #time.sleep(self.delay_between_actions)
            #q = self.driver.find_element_by_id('single_popup_background_event')
            #q.click()
            
            log.info('OK - CRYSTAL')
            #WebDriverWait(self.driver, self.max_wait_time, 0.5)
        except TimeoutException:
            log.error('NG - Time out - crystal')
        except NoSuchElementException:
            log.info('NG - CRYSTAL - No Such Element Exception')
        except:
            log.error('NG - NOT ABLE TO Collect Crystal - crystal')

    def mystical_emporium(self, choice=-1):
        try:
            log = self.log
            driver = self.driver
            driver.get(self.CA_pages['mystical_emporium'])
            WebDriverWait(driver, self.max_wait_time, 0.5)
            qlist = driver.find_elements_by_xpath('//*[@id="app_body"]/table/tbody/tr/td/div[8]/table/tbody/tr/td/div/div')
            #log.info('total {} items found'.format(len(q)))
            if (len(qlist)>0):
                found = 0
                for i in range(len(qlist)):
                    if (not found): 
                        str_cost = qlist[i].text.split('\n')[-1]
                        str_target = qlist[i].text.split('\n')[0]
    
                        if (str_cost.find('B')>0):
                            found = 1                            
                            CA_mystical_emporium_buy_URL = self.CA_pages['mystical_emporium_buy_Template'].format(i)
                            driver.get(CA_mystical_emporium_buy_URL)
                            WebDriverWait(driver, self.max_wait_time, 0.5)
                            q = driver.find_element_by_class_name('result')
                            if (q.text.find("non_renewable_purchase")>=0):
                                log.info('NG - EMPORIUM - [{}] - [{}] - [{}]'.format(str_target, str_cost, q.text))             
                            else:
                                log.info('OK - EMPORIUM - [{}] - [{}] - [{}]'.format(str_target, str_cost, q.text))             
        except TimeoutException:
            log.error('NG - Time out - mystical_emporium')
        except NoSuchElementException:
            log.error('NG - No Such Element Exception - mystical_emporium')
        except:
            log.error('NG - mystical emporium error - mystical_emporium')

    def websurf(self, url):
        try:
            log = self.log
            driver = self.driver
            driver.get(url)
            WebDriverWait(driver, self.max_wait_time, 0.5)
            return 1
        except:
            log.error('NG - websurf failed')
            return 0
 
    def tenpbattle(self):
        log = self.log

        driver = self.driver
        driver.get(self.CA_pages['Home'])
        WebDriverWait(driver, self.max_wait_time, 0.5)
    
        # If 10pbattle button exist, click it and get reward
        try:
            #q = driver.find_element_by_name('player_email')
            q = driver.find_element_by_css_selector('#newsFeedSection > div > div:nth-child(2) > div > div > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div > a > img')
            WebDriverWait(driver, self.max_wait_time, 0.5)
            q.click()
            log.info('OK - Click 10 battle button')            
            
            q = driver.find_element_by_css_selector('#guild_battle_banner_section > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > form > div > input[type=image]')
            WebDriverWait(driver, self.max_wait_time, 0.5)
            q.click()
            log.info('OK - Click Collect Reward button')
            
            return 1
        except:
            log.error('NG - NOT ABLE TO FIND 10P BATTLE')
            return 0

    def cgbbattle(self):
        log = self.log

        driver = self.driver
        driver.get(self.CA_pages['Home'])
        WebDriverWait(driver, self.max_wait_time, 0.5)
        
        # If 10pbattle button exist, click it and get reward
        try:
            #q = driver.find_element_by_name('player_email')
            q = driver.find_element_by_css_selector('#newsFeedSection > div > div:nth-child(2) > div > div > div:nth-child(3) > div:nth-child(4) > div:nth-child(3) > div > a > img')
            WebDriverWait(driver, self.max_wait_time, 0.5)
            q.click()
            #log.info('OK - Click Classical GB battle button')            
            
            # Click Classical Battle Button
            q = driver.find_element_by_css_selector('#guildv2_battle_middle > div:nth-child(2) > div > form > div > input[type=image]')
            WebDriverWait(driver, self.max_wait_time, 0.5)
            q.click()
            #log.info('OK - Entering Classical GB page')
            
            q = driver.find_element_by_css_selector('#guild_battle_banner_section > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > form > div > input[type=image]')
            WebDriverWait(driver, self.max_wait_time, 0.5)
            q.click()
            log.info('OK - Click Classical GB reward button')
            return 1
        except:
            log.error('NG - NOT ABLE TO FIND Classical GB BATTLE')
            return 0

    def do_CA_actions(self):     
        # 2019/11/29
        # Read army code from file directly
        with open('target_id_list.json', 'r') as f:
            target_id_list = json.load(f)

#        target_id_list = ['1435420452', '100000679131828','1510099904','1510099904','652039832',
#                  '100001794195370', '1022637340', '100000289129570', '100001414674017','100001525393037', 
#                  '400000022087940', '100004701243191', '100003273240571','100000170212020','685535295',
#                  '100000921887627','800958264','1554515592','100000852434386','1210736580', 
#                  '100000226485474', '100001872491434', '1596566340', '1583962246', '100005667843637',
#                  '100000719537202', '105462343377810', '100006456836854','100000696251470','100000248455063', 
#                  '590571182','1188497716', '100000581927572','100001699937786','100000019076690',
#                  '500000005687330', '100006270017322','100000778405632','1259524444', '1339535260',
#                  '10211526885304730', '400000021819550', '1206683746', '100005848323670', '400000012607620',
#                  '1612273746', '1708228670', '697477866','100003464384141','100004701243191',
#                  '1461813629', '1851901330', '741284166', '537147708', '100000983384685',  
#                  '100001402814754', '100000180220590', '1735415398','1446697808987746','400000024556000',
#                  '100006511742971', '100003258109160', '100004238596605', '100001396841163', '1115353523', 
#                  '100000556103900','110750499259542', '646965216','400000036079700'
#                 ]
        for i in range(len(self.CA_user_prop)):
            self.clear_CA_user_prop()
            user_prop = self.CA_user_prop[i]

            # Do nothing if not right Guild and Squad
            if (self.args.Guild != 'Any'):
                if (self.args.Guild != user_prop['Guild']):
                    #print('Wrong Guild - Guild={}, Squad={}'.format(self.args.Guild, self.args.Squad))
                    #time.sleep(5)
                    continue
            if (self.args.Squad != None):
                bRightSqd = 0
                for j in range(len(self.args.Squad)):
                    if (self.args.Squad[j] == user_prop['Squad']):
                        bRightSqd = 1
                if (not bRightSqd):
                    #print('Wrong Squad - Guild={}, Squad={}'.format(self.args.Guild, self.args.Squad))
                    #time.sleep(5)
                    continue
            #print('Corret Guild/Squad - Guild={}, Squad={}, Name={}'.format(self.args.Guild, self.args.Squad, user_prop['Name']))
            #time.sleep(5)
        
            # Log in when any action to take
            # format string reference
            # ref: https://officeguide.cc/python-string-formatters-tutorial/
            self.log.info('===== {} - [{}][SQD {}][{}] {}'.format(user_prop['NO'], user_prop['Guild'], user_prop['Squad'], user_prop['Name'], user_prop['Email'].split('@')[0]))
            
            if ((self.args.DailyClick) and (user_prop['DailyClick'])):
                if (not self.logged_in):
                    self.log_in(user_prop['Email'],user_prop['PWD']) 
                if (self.logged_in):
                    # Demi goal will depends on Campain
                    self.start_campaign(user_prop['Campaign'].upper())
                    demigoal = self.check_campaign_demi()
                    # if not assign blessing goal with command line argument
                    if (demigoal <= 0):
                        if (self.args.Blessing == 0):
                            demigoal = user_prop['Blessing']
                        else:
                            demigoal = self.args.Blessing
                    self.dailyclicksCA(demigoal)
            if ((self.args.Reward_10P) and (user_prop['Reward_10P'])):
                if (not self.logged_in):
                    self.log_in(user_prop['Email'],user_prop['PWD']) 
                if (self.logged_in):
                    self.tenpbattle()
            if ((self.args.Reward_100P) and (user_prop['Reward_100P'])):
                if (not self.logged_in):
                    self.log_in(user_prop['Email'],user_prop['PWD']) 
                if (self.logged_in):
                    self.websurf(self.CA_pages['Reward_100P'])
                    self.log.info('OK - Collect 100p reward')
            if ((self.args.Reward_CGB) and (user_prop['Reward_CGB'])):
                if (not self.logged_in):
                    self.log_in(user_prop['Email'],user_prop['PWD']) 
                if (self.logged_in):
                    self.cgbbattle()
            if (self.args.Blessing != None):
                if (not self.logged_in):
                    self.log_in(user_prop['Email'],user_prop['PWD']) 
                if (self.logged_in):
                    # demigoal priority: Campaign -> command line -> user_prop
                    self.start_campaign(user_prop['Campaign'].upper())
                    demigoal = self.check_campaign_demi()
                    # if not assign blessing goal with command line argument
                    if (demigoal <= 0):
                        if (self.args.Blessing == 0):
                            demigoal = user_prop['Blessing']
                        else:
                            demigoal = self.args.Blessing
                    self.bless(demigoal)
            if (self.args.ConquestDuel and (user_prop['Conquest_Duel'])):
                if (not self.logged_in):
                    self.log_in(user_prop['Email'],user_prop['PWD']) 
                if (self.logged_in):
                    self.conquest_duel(target_id_list, user_prop)

            if (self.logged_in):
                #self.websurf("https://web3.castleagegame.com/castle_ws/hot_swap_ajax_handler.php?ajax_action=change_loadout&ajax=1&target_loadout={}".format(user_prop['Def_Loadout']))
                self.driver.execute_script(f"sel=document.getElementsByName('choose_loadout'); sel[0].selectedIndex={user_prop['Def_Loadout']-1}; sel[0].onchange();")
                time.sleep(1)
                self.log_out()
            
            #self.log.info("==============================")
            #self.log.info("")
        
        with open('target_id_list.json', 'w') as f:
            #print(f.read())
            print(json.dumps(target_id_list, indent=2, ensure_ascii=False), file = f)

        return 1
        #if ((self.CA_actions['Blessing']) and (self.CA_user_prop['Blessing'])):
        #    self.bless(self.bless_goal)
        #if ((self.CA_actions['Bonus']) and (self.CA_user_prop['Bonus'])):
        #    self.enable_bonus()
        #if ((self.CA_actions['DailySpin']) and (self.CA_user_prop['DailySpin'])):
        #    self.daily_spin()
        #if ((self.CA_actions['Resource']) and (self.CA_user_prop['Resource'])):
        #    self.resource()
        #if ((self.CA_actions['Crystal']) and (self.CA_user_prop['Crystal'])):
        #    self.crystal()
        #if ((self.CA_actions['mystical_emporium']) and (self.CA_user_prop['mystical_emporium'])):
        #    self.mystical_emporium()
        
    def dailyclicksCA(self, blessing_goal=5):
        ret = 0
        
        #self.log.info("===== Start of daily click =====")
        if (not self.logged_in):
            self.log.error('NG - Abort due to not logged in yet.')
            return ret
    
        self.daily_spin()
        self.bless(blessing_goal)
        self.enable_bonus()    
        self.resource()
        self.crystal()
        self.mystical_emporium()
        #self.log.info("====== End of daily click ======")
        ret = 1
        return ret
    
    def conquest_duel(self, target_id_list, user_prop):
        log = self.log
        # Check tokens remain
        driver = self.driver
        driver.get("https://web3.castleagegame.com/castle_ws/conquest_duel.php")
        q = driver.find_element_by_xpath('//*[@id="persistHomeConquestPlateOpen"]/div[1]/div')
        token = int(q.text.strip())
        #log.info('{}, token={}'.format(user_prop['Name'], token))
    
        if (token <= 0):
            return        
    
        id_len = len(target_id_list)
        #q = driver.find_element_by_name('bqh') 
        #bqh = q.get_property('value')
    
        # Change to PvP loadout
        loadout = user_prop['PvP_Loadout']
        #driver.get("https://web3.castleagegame.com/castle_ws/hot_swap_ajax_handler.php?ajax_action=change_loadout&ajax=1&target_loadout={}".format(loadout))
        driver.execute_script(f"sel=document.getElementsByName('choose_loadout'); sel[0].selectedIndex={loadout-1}; sel[0].onchange();")
        time.sleep(1)
        
        i = 0
        vic_count = 0
        def_count = 0
        random.seed
        idx = random.randint(0,id_len-1)
    
        # Conquest duel with assigned list
        while (token > 0):
            i = i + 1
            #for i in range(token):
            target_prop = target_id_list[idx]
            
            # check bsi
            if (user_prop["BSI"] < target_prop["max_bsi"]):
                new_idx = idx
                
                while ((user_prop["BSI"] < target_prop["max_bsi"]) and (new_idx != idx - 1)):
                    print(f"my bsi {user_prop['BSI']}, target info {target_prop}")
                    new_idx = (new_idx + 1) % len(target_id_list)
                    target_prop = target_id_list[new_idx]
            

            target_id = target_prop['target_id']
            
            #idx = (idx + 1) % len(target_id_list)
            url = "https://web3.castleagegame.com/castle_ws/conquest_duel.php?target_id={}&action=battle&duel=true&bqh={}&ajax=1&ajax=1".format(target_id, self.bqh)
            #print('[{}] Hit #{} - {}'.format(user_prop['Name'], i, target_id))
            driver.get(url)
    
            q = driver.find_element_by_xpath('//*[@id="persistHomeConquestPlateOpen"]/div[1]/div')
            token = int(q.text.strip())
                            
            # Check result
            # Victory
            # Defeat
            # Dead or Weak
            try:
                q = driver.find_element_by_css_selector('#results_main_wrapper > div:nth-child(1)')
                victory = q.get_attribute('style').find('victory')
    
                # Victory - conqduel_victory3.jpg
                # Defeat - conqduel_defeat3.jpg
                # Weak
                if (victory>0):
                    #print('Hit #{} [Victory!] - {}'.format(i, target_id))
                    vic_count = vic_count + 1
                    
                    # update target_id_list[idx]
                    if ((target_id_list[idx]['max_bsi'] > user_prop['BSI']) or
                        (target_id_list[idx]['max_bsi'] == 0)):
                        target_id_list[idx]['max_bsi'] = user_prop['BSI'] - 1
                        if ((target_id_list[idx]['max_bsi']) < (target_id_list[idx]['min_bsi'])):
                            target_id_list[idx]['min_bsi'] = target_id_list[idx]['max_bsi'] - 1

                # if too weak... find 'weak' and heal self
                else:
                    weak = q.get_attribute('style').find('weak')
                    if (weak>0):
                        print('todo: heal self')    
                    else:
                        log.info('Hit #{} [Defeat!] - {}'.format(i, target_id))
                        # update target_id_list[idx]
                        if ((target_id_list[idx]['min_bsi'] < user_prop['BSI']) or
                            (target_id_list[idx]['min_bsi'] == 0)):
                            target_id_list[idx]['min_bsi'] = user_prop['BSI'] + 1
                            if ((target_id_list[idx]['min_bsi']) > (target_id_list[idx]['max_bsi'])):
                                target_id_list[idx]['max_bsi'] = target_id_list[idx]['min_bsi'] + 1

                        def_count = def_count + 1
                        idx = random.randint(0,id_len-1)
            except:
                #print('Hit #{} [Dead!] - {}'.format(i, target_id))
                idx = random.randint(0,id_len-1)
                continue
            #if ((target_id_list[idx]['min_bsi']) > (target_id_list[idx]['max_bsi'])):
            #    target_id_list[idx]['min_bsi'] = target_id_list[idx]['max_bsi'] - 1

        log.info('OK - Conquest Duel - Victory: {}; Defeat: {}'.format(vic_count, def_count))
        return target_id_list

    def bank(self, user_prop):
        driver = self.driver
        if (self.logged_in):
            # Check tokens remain
            # change general "Aeris"
            driver.get("https://web3.castleagegame.com/castle_ws/generals.php?item={}&itype=0&ajax=1&ajax=1".format(16))
            
            # Bank
            driver.get("https://web3.castleagegame.com/castle_ws/generals.php?bqh={}&header_stash_gold=1&ajax=1&ajax=1".format(self.bqh))

            driver.get("https://web3.castleagegame.com/castle_ws/keep.php")
            q = driver.find_element_by_css_selector('#keepGuardAndBank > div > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > div')
            stored_money =  int(q.text.split('$')[-1].replace(',',''))
            #print('Stored = {}'.format(stored_money))
            
            # Restore to defaul loadout
            loadout = user_prop['Def_Loadout']
            # driver.get("https://web3.castleagegame.com/castle_ws/hot_swap_ajax_handler.php?ajax_action=change_loadout&ajax=1&target_loadout={}".format(loadout))
            driver.execute_script(f"sel=document.getElementsByName('choose_loadout'); sel[0].selectedIndex={loadout-1}; sel[0].onchange();")
            time.sleep(1)
            return stored_money
        else:
            return -1
    
    def start_campaign(self, campaign = 'EASY'):
        # Common/Rare/Epic Chaos Gem status trial code
        # Easy/Normal/Hard Campaign
        driver = self.driver
        ret = -1
        #print('check_campaign_demi')
        
        # Open Gem block, is this necessary? If not, ignore this to save time
        try:
            #print('1. Open Gem block')
            q = driver.find_element_by_xpath("//div[@id='persistHomeCampaignPlateClosed']//div[1]")
            q.click()
            #print('1. Open Gem block')
            #time.sleep(delay_between_actions)
        except:
            #print('Chaos Gem block already open')
            pass
    
        # Find Common Cahos Gem image button and click if found
        try:
            #print('2. Activated {} campaign'.format(campaign)) 
            if (campaign == 'EASY'):
                q = driver.find_element_by_xpath("//div[contains(text(), 'Common Chaos Gem')]//following-sibling::form//input[@type='image']")
            elif (campaign == 'NORMAL'):
                q = driver.find_element_by_xpath("//div[contains(text(), 'Rare Chaos Gem')]//following-sibling::form//input[@type='image']")
            elif (campaign == 'HARD'):
                q = driver.find_element_by_xpath("//div[contains(text(), 'Epic Chaos Gem')]//following-sibling::form//input[@type='image']")
            else:
                return ret
            q.click()
            ret = 1
            #print('2. Activated {} campaign'.format(campaign))   
            #time.sleep(delay_between_actions)
        except:
            # if not found, Chaos Gem is working in progress
            #print('Campaign is already activated')
            pass
        
        return ret
        

    def get_campaign_type(self):
        # Common/Rare/Epic Chaos Gem status trial code
        # Easy/Normal/Hard Campaign
        driver = self.driver
        ret = ''
        #print('check_campaign_demi')
        
        # Open Gem block        
         # Check Campaign type - Common/Rare/Epic
        #try:    
        #    q = driver.find_element_by_xpath("//div[@id='persistHomeCampaignPlateStart']//div[contains(text(),'Easy')]")
        #    print('Easy - Common Chaos Gem')   
            #time.sleep(delay_between_actions)
        #except:
        #    pass
    
        #try:    
        #    q = driver.find_element_by_xpath("//div[@id='persistHomeCampaignPlateStart']//div[contains(text(),'Normal')]")
        #    print('Normal - Rare Chaos Gem')   
            #time.sleep(delay_between_actions)
        #except:
        #    pass
    
        #try:    
        #    q = driver.find_element_by_xpath("//div[@id='persistHomeCampaignPlateStart']//div[contains(text(),'Hard')]")
        #    print('Hard - Epic Chaos Gem')   
            #time.sleep(delay_between_actions)
        #except:
        #    pass
        
        try:
            q = driver.find_element_by_xpath("//div[@id='monster_ticker']//preceding-sibling::div[1]")
            ret = q.text
            #print(q.text)
        except:
            ret = ''
            pass
        
        return ret
           
    def check_campaign_demi(self):   
        # Common/Rare/Epic Chaos Gem status trial code
        # Easy/Normal/Hard Campaign
        driver = self.driver
        ret = -1

        #print('check_campaign_demi')
        # find missions
        try:
            #for i in range(1, 13, 2):
                #xpath = '//div[@id="persistHomeCampaignPlateStart"]/div[3]/div[1]/div[{}]/div[1]/img'.format(i)
            xpath = '//div[@id="persistHomeCampaignPlateStart"]//img[contains(@src, "icons_demi_")]'
            #print(xpath)
            q = driver.find_element_by_xpath(xpath)
    
            imgsrc = q.get_property('src').split('/')[-1]
            if (imgsrc == "icons_demi_ambrosia.png"):
                #print('Bless Ambrosia')
                ret = 1
            elif (imgsrc == "icons_demi_malk.png"):
                #print('Bless Malekus')
                ret = 2
            elif (imgsrc == "icons_demi_corv.png"):
                #print('Bless Corvintheus')
                ret = 3
            elif (imgsrc == "icons_demi_aurora.png"):
                #print('Bless Aurora')
                ret = 4
            elif (imgsrc == "icons_demi_azeron.png"):
                #print('Bless Azeron')
                ret = 5
    
            #print(q.get_property('src'))
            # https://image4test.castleagegame.com/graphics/icons_demi_ambrosia.png
            # https://image4test.castleagegame.com/graphics/icons_demi_malk.png
            # https://image4test.castleagegame.com/graphics/icons_demi_corv.png
            # https://image4test.castleagegame.com/graphics/icons_demi_aurora.png
            # https://image4test.castleagegame.com/graphics/icons_demi_azeron.png
            #time.sleep(delay_between_actions)
        except:
            #print('Cannot find missions')
            ret = -1
            pass
    
        #//div[@id="persistHomeCampaignPlateStart"]/div[3]/div[1]/div[1]/div[1]/img
        #//div[@id="persistHomeCampaignPlateStart"]/div[3]/div[1]/div[3]/div[1]/img
        #//div[@id="persistHomeCampaignPlateStart"]/div[3]/div[1]/div[5]/div[1]/img
    
        # Closed activated Gem block
        #try:
        #    q = driver.find_element_by_xpath("//div[@id='persistHomeCampaignPlateStart']//div[1]")
        #    q.click()
            #print('Activated Gem block is closed now')
            #time.sleep(3)
        #except:
            #print('Cannot close Gem block')
        #    pass
        
        # Close Chaos Gem block (Not Activated status)
        #try:
        #    q = driver.find_element_by_xpath("//div[@id='persistHomeCampaignPlateOpen']//div[1]")
        #    q.click()
        #    print('3')
        #    time.sleep(3)
        #except:
        #    print('Unknown error')
        #    pass
        
        return ret