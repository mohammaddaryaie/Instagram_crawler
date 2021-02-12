# Instagram_crawler
I try to add some codes that gather Instagram data such as comments, likes, followers, following and so on.

Follow bellow instructions to initiate code:

1- You should download geckodriver.exe (win or linux) and copy its file to specific directory. And, set its directory in __init__ function of class.

2- In Constant class, you shoud add your directory in c_home_directory variable.Next, copy all text files in the directory.

3- In insta.py file, when you want create the object of InstagramBot you should enter your username and password.

4- You can run the code.

Functions:
Login: In this function you should enter your username and password, next, call it to login by your account in Instagram.

FindMyFollower: This Function extracts all your followers and returns them as a list.

FindMyFollowing: This Function extracts all your following list and returns them as a list.

UpdateMyFollowersFile: This function use the FindMyFollower function and write it in the followers.txt. Besides, it compares current followers list with previous one, then finds someones who unfollow you. Next,it writes them in the followers_unfollow.txt.

UpdateMyFollowingsFile: Here, the following.txt file is created and every time you call it, updates it. In this file, you can find your following list.

FetchSourcePagePostsLikers:

UpdateLikersByFollowers:

SendMessage:

FolloweLikers:
