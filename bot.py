from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re
import random
import sys
DELAY = 3
CAP = 350
class Bot():
    def __init__(self):
            
        ## GET THE LOGIN INFORMATION ##
        print("Username: ")
        user = input()
        #Get the password#
        print("Password: ")
        passw = input()
        ## END ##
        
        ## GET HASHTAGS ##
        print("List only 1 hashtag('eg. blacklove'): ")
        tag = input()
        tags = tag.split()
        ## END ##
        
        ### SET LIMIT ###
        print("How many people should we engage with?(per hashtag)")
        limit = input()
        limit = int(limit)
        if limit > CAP:
            limit = CAP
        ## END ##
            
        ## UNFOLLOW OPTION ##
        option = ""
        if limit <= 0:
            print("How many users would you like to unfollow after following is fininshed?")
            option = input()
        ## END ##
        
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com/")  
        self.driver.delete_all_cookies()
        sleep(DELAY)
        username_input = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
        username_input.send_keys(user)
        pass_input = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
        pass_input.send_keys(passw)
        button_input = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button")
        button_input.click()
        sleep(DELAY)
        
        ## OPEN ACCOUNT FOLLOWINGS AND START UNFOLLOWING ##        
            
        def get_account_and_unfollow(name, cout):
            while cout < int(option):
                delayer = 10
                src = "https://www.instagram.com/" + name
                self.driver.get(src)
                following = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
                following.click()
                sleep(delayer)
                peeps = self.driver.find_elements_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div//button")
                for p in peeps:
                    p.click()
                    popup = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]")
                    sleep(delayer)
                    popup.click()
                    if p == peeps[4]:
                        self.driver.get(src)
                        return get_account_and_unfollow(name, cout)
                cout += 1
        if limit <= 0:
            get_account_and_unfollow(user, 0)
            
        ## GET POST AND LIKE/FOLLOW USER ##
        def get_post_like_and_follow(src, i):
            while i < limit:
                recent = self.driver.find_elements_by_xpath("/html/body/div[1]/section/main/article/div[2]//*[@class='v1Nh3 kIKUG  _bz0w']")
                delayer = 10
                for post in recent:
                    sleep(delayer)
                    post.click()
                    sleep(delayer)
                    like = ""
                    try:
                        like = self.driver.find_element_by_xpath("//*[@class='fr66n']//button")
                        like.click()
                    except NoSuchElementException:
                        self.driver.get(src)
                        return get_post_like_and_follow(src, i)                     
                    sleep(delayer)
                    follow = self.driver.find_element_by_xpath("//*[@class='bY2yH']//button")
                    if not re.search('Following', follow.text):
                        follow.click()
                    else:
                        self.driver.get(src)
                        return get_post_like_and_follow(src, i)
                    ## GET USERNAME AND ADD IT TO FOLLOWING FILE FOR LATER UNFOLLOW FEATURES ##    
                    user = self.driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a")
                    with open('following.txt', 'a') as f:
                        f.write(user.text)
                        f.write('\n')
                    ## END ##
                    sleep(delayer)
                    exit = self.driver.find_element_by_xpath("//*[@class='                     Igw0E     IwRSH      eGOV_         _4EzTm                                                                                  BI4qX            qJPeX            fm1AK   TxciK yiMZG']//button")
                    exit.click()
                    i += 1
                    if post == recent[-1]:
                        self.driver.get(src)
                        return get_post_like_and_follow(src, i)
            sys.exit("Task completed successfully")
                
        ## OPEN HASHTAG PAGE ##
        def open_page(tg):
            strr = "https://www.instagram.com/explore/tags/" + tg
            self.driver.get(strr)
            get_post_like_and_follow(strr, 0)        
        ## STARTUP ##
        def start_page():
            sleep(2)
            button = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
            button.click()
            sleep(2)
            button = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
            button.click()
            if len(tags) <= 1:
                open_page(tags[0])
            else:
                for t in tags:
                    open_page(t)        
        start_page()
        
def main():
    my_bot = Bot()
if __name__ == '__main__':
    main()
