# Instagram_crawler
I try to add some codes that gather Instagram data such as comments, likes, followers, following and so on.

Follow bellow instructions to initiate code:

1- You should download geckodriver.exe (win or linux) and copy its file to specific directory. And, set its directory in __init__ function of class.

2- In Constant class, you shoud add your directory in c_home_directory variable.Next, copy all text files in the directory.

3- In insta.py file, when you want create the object of InstagramBot you should enter your username and password.

4- You can run the code.

Functions of InstagramBot.py:
Login: In this function you should enter your username and password, next, call it to login by your account in Instagram.

FindMyFollower: This Function extracts all your followers and returns them as a list.

FindMyFollowing: This Function extracts all your following list and returns them as a list.

UpdateMyFollowersFile: This function use the FindMyFollower function and write it in the followers.txt. Besides, it compares current followers list with previous one, then finds someones who unfollow you. Next,it writes them in the followers_unfollow.txt.

UpdateMyFollowingsFile: Here, the following.txt file is created and every time you call it, updates it. In this file, you can find your following list.

FetchSourcePagePosts:Between files, there is the source_page.txt file. In this file, you can list the pages which have large number followers or are well-known. This function read source_page.txt and fetch the first posts, you can specify the nymber of fetched posts as an input 'postnumber'. Finally, you can see the result in the source_page_posts.txt file.

FetchSourcePagePostsLikers: This function reads the source_page_posts.txt. Next, extracts all pages what like the pages' posts,. Afterwards, it writes them in the source_page_posts_likers.txt and user_list_to_follow.txt. If the page name is in the user_list_to_follow.txt, it goes by it.

UpdateLikersByFollowers: To prevent of following pages who follow your page, you should update your user_list_to_follow.txt. In this file you can find list of pages that you want follow them. The pages which their follow_flag field is one, have been followed in the past.

SendMessage: This function send message to different pages what are in the user_list_to_follow.txt. And, it recods the log in to usernames_send_message.txt file.
You can specify the message content in Constant.py file in the c_message_content variable.

FolloweLikers: This function reads the pages' names, then follows them. You can set the nimber of following as a function input.

Constant.py: it contains variables what are useed in functions.

c_attemp_number=5 --> In functions 5 time try to get information. For example, in fetching followers, if number of followers list does not increase after 5 times scrolling, it stops trying.

c_home_directory='C:\\'

c_big_number=100000000

c_login_wait=5 --> if you have slow Internet, you can increase it.

c_number_of_posts=5  --> The number of posts what you want to extract.

c_scroll_waiting=1

c_number_of_message=500  --> It is the limitation of sending message every day.

c_message_content=''Follow our page ...'

c_number_of_following=30 --> It is the limitation of following pages every day.
