# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Before Run anything you should download Geckodriver
from idlelib import replace

from pandas.io.sas.sas7bdat import _column
from pycparser.c_ast import Constant
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import Constant
import pandas as pd
import datetime



class InstagramBot:
    def __init__(self, username, password):
        self.username = 'username'
        self.password =  'password'
        self.bot = webdriver.Firefox(executable_path='C:\\geckodriver.exe',
                                     log_path="C:\\geckodriver.log")

    def login(self,login_wait=Constant.c_login_wait):
        print('Start Login ... ')

        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(login_wait)
        try:
            email = bot.find_element_by_name('username').send_keys(self.username)
            password = bot.find_element_by_name('password').send_keys(self.password)
            time.sleep(1)
            try:
                bot.find_element_by_name('password').send_keys(Keys.RETURN)
            except:
                time.sleep(3)
                bot.find_element_by_name('password').send_keys(Keys.RETURN)

            time.sleep(3)
            print('Login Finished.')
        except:
            print('Your Internet is slow. You should increase login_wait variable.')

    def FindMyFollower(self, number_of_followers=Constant.c_big_number):
        # List of Variables
        attemp_counter=0
        bot = self.bot
        followers_array = []

        print('Enter to my home page ...')
        bot.get('https://instagram.com/' + self.username)
        time.sleep(2)
        print('Open follower window ...')
        bot.find_element_by_xpath('//a[@href="/' + self.username + '/followers/"]').click()
        time.sleep(2)
        popup = bot.find_element_by_class_name('isgrP')
        print('Get followers names ...')

        while len(followers_array) < number_of_followers:
            followers_array = list(set(followers_array))
            current_list = len(followers_array)
            bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)
            time.sleep(Constant.c_scroll_waiting)
            followers = bot.find_elements_by_class_name('FPmhX')

            print('Number of followers after each scrolling: ' + str(len(followers)))
            for follower in followers:
                if follower.text not in followers_array:
                    followers_array.append(follower.text)

            if current_list == len(followers_array):
                attemp_counter += 1
                if attemp_counter == Constant.c_attemp_number:
                    break
        print('Followers number: ' + str(len(followers_array)))
        print('Finish Finding Followers.')
        return followers_array

    def FindMyFollowing(self, number_of_following=Constant.c_big_number):
        # List of Variables
        attemp_counter=0
        bot = self.bot
        following_array = []

        print('Enter to my home page ...')
        bot.get('https://instagram.com/' + self.username)
        time.sleep(2)
        print('Open following window ...')
        bot.find_element_by_xpath('//a[@href="/' + self.username + '/following/"]').click()
        time.sleep(2)
        popup = bot.find_element_by_class_name('isgrP')

        print('Get following names ...')

        while len(following_array) <= number_of_following:
            followers_array = list(set(following_array))
            current_list = len(following_array)
            bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)
            time.sleep(Constant.c_scroll_waiting)
            followings = bot.find_elements_by_class_name('FPmhX')
            print('Number of following list after each scrolling: ' + str(len(followings)))
            for follower in followings:
                if follower.text not in following_array:
                    following_array.append(follower.text)


            if current_list == len(following_array):
                attemp_counter += 1
                if attemp_counter == Constant.c_attemp_number:
                    break
        print('Following Number: ' + str(len(following_array)))
        print('Finish Finding Followings.')
        return following_array

    def UpdateMyFollowersFile(self):
        # List of Variables
        try:
            l_followers_unfollow =[]
            print('Reading Followers File ...')
            l_followers = pd.read_csv(Constant.c_home_directory + 'followers.txt')
            print('Reading followers_unfollow File ...')
            f_followers_unfollow = open(Constant.c_home_directory + 'followers_unfollow.txt','+a')
            for line in f_followers_unfollow:
                l_followers_unfollow.append(line.strip())
            print('Start fetching followers ...')
            followers= self.FindMyFollower()
            print('Finding new unfollower list ...')
            for follower in l_followers['username'].values:
                if follower not in followers:
                    f_followers_unfollow.write(follower.strip()+'\n')
            f_followers_unfollow.close()
            print('Write followers list in a file ...')
            df_followers = pd.DataFrame (followers,columns=['username'])
            df_followers.to_csv(Constant.c_home_directory + 'followers.txt',index=False)
            print('Finish Updating MyFollowersFile.')
        except Exception as e:
            print('Updating File has not been done correctly... try again')
            print('Error Massage:' + str(e))

    def UpdateMyFollowingsFile(self):
        # List of Variables
        l_followers_unfollow = []

        try:
            print('Reading Following File ...')
            l_followers = pd.read_csv(Constant.c_home_directory + 'following.txt')
            print('Start fetching following ...')
            following= self.FindMyFollowing()
            print('Write followers list in a file ...')
            df_followers = pd.DataFrame (following,columns=['username'])
            df_followers.to_csv(Constant.c_home_directory + 'following.txt',index=False)
            print('Finish Updating MyFollowingFile.')
        except Exception as e:
            print('Updating File has not been done correctly... try again')
            print('Error Massage:' + str(e))

    def FetchSourcePagePosts(self,postnumber=Constant.c_number_of_posts):
        # List of Variables
        bot = self.bot
        l_followers_unfollow = []

        try:

            print('Reading Source_Page File ...')
            l_source_page = pd.read_csv(Constant.c_home_directory + 'source_page.txt')
            l_source_page_post = pd.DataFrame(columns={'source_page','posts'})

            print('Start fetching posts ...')
            for source_page in l_source_page['source_page'].values:
                l_posts=[]
                print('Open the page '+source_page)
                bot.get('https://instagram.com/' + source_page)
                homePage = bot.find_element_by_class_name('sDN5V')
                bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', homePage)
                time.sleep(Constant.c_scroll_waiting)
                posts = bot.find_elements_by_class_name('v1Nh3')

                if len(posts) < 5:
                    time.sleep(2)
                    bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', homePage)
                    posts = bot.find_elements_by_class_name('v1Nh3')

                print('Number of posts '+source_page +' page: ' +str(len(posts)))
                if len(posts) >0 :
                    for i in range(0,Constant.c_number_of_posts):
                        post_link = posts[i].find_element_by_css_selector("div a")
                        l_posts.append(post_link.get_attribute("href"))

                print('Adding posts to list l_source_page_post.')
                for post in l_posts:
                    if  len(l_source_page_post[(l_source_page_post['posts']==post)
                                                      & (l_source_page_post['source_page']==source_page)] ) == 0 :
                        l_source_page_post.loc[len(l_source_page_post.index)] = [source_page.strip(),post.strip()]

            print('Write in the list l_source_page_post file.')
            l_source_page_post.to_csv(Constant.c_home_directory + 'source_page_posts.txt',index=False)
            print('Finish Fetching SourcePagePosts.')
        except Exception as e:
            print('Fetch source page posts has error... try again')
            print('Error Massage:' + str(e))

    def FetchSourcePagePostsLikers(self):
        # List of Variables
        bot = self.bot
        letters = set('/')

        try:

            print('Reading Source_Page_Posts File ...')
            l_source_page_posts = pd.read_csv(Constant.c_home_directory + 'source_page_posts.txt')

            print('Start fetching likers ...')
            for post in l_source_page_posts.values:
                likers_list = []
                likers_counter = 0
                attemp_counter = 0
                print('Open the post '+post[1]+ ' from page '+post[0])
                bot.get(post[1])
                time.sleep(2)
                like_bottun = bot.find_element_by_class_name('Nm9Fw').find_element_by_class_name('sqdOP')
                num_of_like = int(like_bottun.text.split(' ')[0].replace(',',''))
                print('Number of total likes: '+str(num_of_like))
                bot.find_element_by_class_name('Nm9Fw').find_element_by_class_name('sqdOP').click()
                try:
                    popup = bot.find_element_by_xpath("//div[@style='height: 356px; overflow: hidden auto;']")
                except:
                    time.sleep(1)
                    popup = bot.find_element_by_xpath("//div[@style='height: 356px; overflow: hidden auto;']")

                print('Start finding likers...')
                while likers_counter < num_of_like:
                    current_list = len(likers_list)
                    bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)
                    time.sleep(Constant.c_scroll_waiting)
                    likers = bot.find_elements_by_css_selector('a.FPmhX')
                    likers_list = list(set(likers_list))
                    print('Number of Likers after each scrolling: ' + str(len(likers_list)))
                    for liker in likers:
                        try:
                            if liker.text not in likers_list:
                                likers_list.append(liker.text)
                                likers_counter += 1
                        except Exception as e:
                            ee = e
                            matches = re.findall(r'\"(.+?)\"', str(ee))
                            for word in matches:
                                if letters & set(word):
                                    word = word.replace('/', '')
                                    if word not in likers_list:
                                        likers_list.append(word)
                                        likers_counter += 1
                                        break
                    if current_list == len(likers_list):
                        attemp_counter += 1
                        if attemp_counter == Constant.c_attemp_number:
                            break

                print('Finish crawling the '+post[1]+ ' likers of page '+post[0])
                print('Reading source_page_posts_likers and user_list_to_follow Files ...')

                l_source_page_posts_likers = pd.read_csv(Constant.c_home_directory + 'source_page_posts_likers.txt')
                l_user_list_to_follow = pd.read_csv(Constant.c_home_directory + 'user_list_to_follow.txt')
                f_user_list_to_follow=open(Constant.c_home_directory + 'user_list_to_follow.txt','+a')
                for liker in likers_list:
                    if liker not in l_user_list_to_follow['username'].values :
                        #Format file user_list_to_follow: username,follow_flag,date_insert,date_follow
                        f_user_list_to_follow.write(liker+','+'0,'+str(datetime.datetime.now())+','+'None'+'\n')
                    #Format file l_source_page_posts_likers: source_page,posts,likers,date_fetch
                    if len(l_source_page_posts_likers[(l_source_page_posts_likers['posts'] == post[1])
                                              & (l_source_page_posts_likers['source_page'] == post[0])
                                                      & (l_source_page_posts_likers['likers'] == liker)]) == 0:
                        l_source_page_posts_likers.loc[len(l_source_page_posts_likers.index)] = [post[0].strip(),
                                                                                                 post[1].strip(),liker.strip(),str(datetime.datetime.now())]
                print('Write in the f_user_list_to_follow and l_source_page_posts_likers files.')
                l_source_page_posts_likers.to_csv(Constant.c_home_directory + 'source_page_posts_likers.txt', index=False)
                f_user_list_to_follow.close()
            print('Finish fetching likers.')
        except Exception as e:
            print('Fetching Likers has an error... try again')
            print('Error Massage:' + str(e))

    def UpdateLikersByFollowers(self):
        # List of Variables

        try:
            print('Reading user_list_to_follow, followers and followers_unfollow Files ...')
            #Format file user_list_to_follow: username,follow_flag,date_insert,date_follow
            l_user_list_to_follow = pd.read_csv(Constant.c_home_directory + 'user_list_to_follow.txt')
            l_followers = pd.read_csv(Constant.c_home_directory + 'followers.txt')
            l_followers_unfollow = pd.read_csv(Constant.c_home_directory + 'followers_unfollow.txt')

            for i in l_user_list_to_follow.index:
                if (l_user_list_to_follow.values[i][0] in l_followers['username'].values) or (l_user_list_to_follow[i][0] in l_followers_unfollow['username'].values if len(l_followers_unfollow)>0  else False):
                    l_user_list_to_follow['follow_flag']._set_value(i,'1')
                    l_user_list_to_follow['date_follow']._set_value(i,str(datetime.datetime.now()))

            print('Write in the l_user_list_to_follow file.')
            l_user_list_to_follow.to_csv(Constant.c_home_directory + 'user_list_to_follow.txt', index=False)
            print('Finish Update Likers By Followers.')
        except Exception as e:
            print('Updating likers by followers has an error... try again')
            print('Error Massage:' + str(e))

    def SendMessage(self):
        # List of Variables
        bot = self.bot
        try:
            print('Reading l_user_list_to_follow File ...')
            # Format file user_list_to_follow: username,follow_flag,date_insert,date_follow
            l_user_list_to_follow = pd.read_csv(Constant.c_home_directory + 'user_list_to_follow.txt')
            f_usernames_send_message = open(Constant.c_home_directory + 'usernames_send_message.txt','a+')
            print('Extracting valid usernames ...')
            l_valid_usernames=l_user_list_to_follow.loc[l_user_list_to_follow['follow_flag']==0 , ['username']].values.tolist()
            try:
                print('Start sending messages ...')
                for i in range(0,Constant.c_number_of_message):
                    print(i)
                    bot.get('https://instagram.com/' + l_valid_usernames[i][0])
                    try:
                        message = bot.find_element_by_class_name('_862NM')
                    except:
                        continue
                    message.click()
                    time.sleep(1)
                    mbox = bot.find_element_by_tag_name('textarea')
                    mbox.send_keys(Constant.c_message_content)
                    mbox.send_keys(Keys.RETURN)
                    f_usernames_send_message.write(l_valid_usernames[i]+','+str(datetime.datetime.now())+'\n')
                    l_user_list_to_follow.loc[l_user_list_to_follow['username'] == l_valid_usernames[i], ['follow_flag']] = 1
                    l_user_list_to_follow.loc[l_user_list_to_follow['username'] == l_valid_usernames[i], ['date_follow']] = str(datetime.datetime.now())
            except:
                print('Write in the l_user_list_to_follow file with ERROR****.')
                f_usernames_send_message.close()
                l_user_list_to_follow.to_csv(Constant.c_home_directory + 'user_list_to_follow.txt', index=False)

            print('Write in the l_user_list_to_follow file')
            f_usernames_send_message.close()
            l_user_list_to_follow.to_csv(Constant.c_home_directory + 'user_list_to_follow.txt', index=False)
        except Exception as e:
            print('Sending Message to users has an error... try again')
            print('Error Massage:' + str(e))

    def FolloweLikers(self,num_of_follow=Constant.c_number_of_following):
        # List of Variables
        bot = self.bot
        try:
            print('Reading l_user_list_to_follow File ...')
            # Format file user_list_to_follow: username,follow_flag,date_insert,date_follow
            l_user_list_to_follow = pd.read_csv(Constant.c_home_directory + 'user_list_to_follow.txt')
            f_usernames_follow = open(Constant.c_home_directory + 'usernames_follow.txt','a+')
            print('Extracting valid usernames ...')
            l_valid_usernames=l_user_list_to_follow.loc[l_user_list_to_follow['follow_flag']==0 , ['username']].values.tolist()
            try:
                print('Start sending messages ...')
                for i in range(0,Constant.c_number_of_following):
                    print('number of following: '+str(i)+' *** Page name: '+l_valid_usernames[i][0])
                    bot.get('https://instagram.com/' + l_valid_usernames[i][0])
                    time.sleep(1)
                    try:
                        follow_button = bot.find_element_by_xpath("//button[contains(text(), 'Follow')]")
                    except:
                        continue
                    follow_button.click()
                    time.sleep(2)
                    f_usernames_follow.write(l_valid_usernames[i][0]+','+str(datetime.datetime.now())+'\n')
                    l_user_list_to_follow.loc[l_user_list_to_follow['username'] == l_valid_usernames[i][0], ['follow_flag']] = 1
                    l_user_list_to_follow.loc[l_user_list_to_follow['username'] == l_valid_usernames[i][0], ['date_follow']] = str(datetime.datetime.now())
            except:
                print('Write in the l_user_list_to_follow file with ERROR****.')
                f_usernames_follow.close()
                l_user_list_to_follow.to_csv(Constant.c_home_directory + 'user_list_to_follow.txt', index=False)

            print('Write in the l_user_list_to_follow file')
            f_usernames_follow.close()
            l_user_list_to_follow.to_csv(Constant.c_home_directory + 'user_list_to_follow.txt', index=False)
            print('Finish Following likers.')
        except Exception as e:
            print('Following likers has an error... try again')
            print('Error Massage:' + str(e))
