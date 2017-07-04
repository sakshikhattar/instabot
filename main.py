import requests

APP_ACCESS_TOKEN = '1408840836.24852af.7b742b11b27445bd95aa824ebc150881'
#Token Owner : khattarsakshi
#Sandbox Users : insta.mriu.test.04, raman_bidhuri2222, mahak_sachdeva, aanchal_arora_, snehabhuyan

BASE_URL = 'https://api.instagram.com/v1/' #common for all the Instagram API endpoints

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
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



#method to get the recent post of the token owner
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    my_post = requests.get(request_url).json()
    if my_post['meta']['code'] == 200:
        if len(my_post['data']):
            status = my_post['data'][0]['caption']['text']
            print status
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
        print '4.Get the recent post of the user'
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
        else:
            print "wrong choice"
            show_menu = False


#calling the method
start_app()
