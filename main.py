import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '1408840836.24852af.7b742b11b27445bd95aa824ebc150881'
#Token Owner : khattarsakshi
#Sandbox Users : insta.mriu.test.04, raman_bidhuri2222, mahak_sachdeva, aanchal_arora_, snehabhuyan

BASE_URL = 'https://api.instagram.com/v1/' #common for all the Instagram API endpoints


def download_user_image(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    print user_media
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            if user_media['data']['type'] == "image":
                image_name = user_media['data']['id'] + '.jpeg'
                image_url = user_media['data']['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print 'Your image has been downloaded!'
            else:
                print 'The post is not an image'
    else:
        print 'Status code other than 200 received!'





#method to delete the negative comments using TextBlob library
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                print blob.sentiment
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


#method to comment on the post of a user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#method to like the post of a user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


#method to get the id of a post
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


#method to get the recent post of a user
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist.'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_post = requests.get(request_url).json()    #using JSON decoder
    if user_post['meta']['code'] == 200:
        if len(user_post['data']):
            status = user_post['data'][0]['caption']['text']
            print status
        else:
            print 'post does not exist'
    else:
        print 'Status code other than 200 received!'



#method to get the recent post of the token owner
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    my_post = requests.get(request_url).json()
    if my_post['meta']['code'] == 200:
        if len(my_post['data']):
            status = my_post['data'][1]['caption']['text']
            print status
            image_name = my_post['data'][1]['id'] + '.jpeg'
            image_url = my_post['data'][1]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


#method to get information about the token owner
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    print user_info
    if user_info['meta']['code'] == 200:  #HTTP 200 means transmission is OK
        print 'Username: %s' % (user_info['data']['username'])
        print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
        print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
        print 'Status code other than 200 received!'



#method to get the user id
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:  #HTTP 200 means transmission is OK
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'


#method to get the information about the user
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    else:
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()

        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                print 'Username: %s' % (user_info['data']['username'])
                print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
                print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
                print 'No. of posts: %s' % (user_info['data']['counts']['media'])
            else:
                print 'There is no data for this user!'
        else:
            print 'Status code other than 200 received!'


#method to show the menu to the user
def start_app():
    show_menu = True
    while show_menu:
        print 'Hey! Welcome to instaBot!'
        print 'What do you want to do?'
        print '1.Get your own details\n'
        print '2.Get details of a user\n'
        print '3.Get your own post\n'
        print '4.Get the recent post of a user\n'
        print '5.Like post of a user\n'
        print '6.Comment on the post of a user\n'
        print '7.Delete negative comments\n'
        print '8.Download the post of a user\n'
        choice = int(raw_input('Enter you choice: '))
        if choice == 1:
            self_info()
        elif choice == 2:
            insta_username = raw_input('Enter the username of the user: ')
            get_user_info(insta_username)
        elif choice == 3:
            get_own_post()
        elif choice == 4:
            insta_username = raw_input('Enter the username of the user: ')
            get_user_post(insta_username)
        elif choice == 5:
            insta_username = raw_input('Enter the username of the user: ')
            like_a_post(insta_username)
        elif choice == 6:
            insta_username = raw_input('Enter the username of the user: ')
            post_a_comment(insta_username)
        elif choice == 7:
            insta_username = raw_input('Enter the username of the user: ')
            delete_negative_comment(insta_username)
        elif choice == 8:
            insta_username = raw_input('Enter the username of the user: ')
            download_user_image(insta_username)

        else:
            print "wrong choice"
            show_menu = False


#calling the method
start_app()

