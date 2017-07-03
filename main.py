import requests

APP_ACCESS_TOKEN = '1408840836.24852af.7b742b11b27445bd95aa824ebc150881'
#Token Owner : khattarsakshi
#Sandbox Users : 14rashi, raman_bidhuri2222, mahak_sachdeva, aanchal_arora_, snehabhuyan

BASE_URL = 'https://api.instagram.com/v1/'

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


#calling of the methods
self_info()
get_user_info('14rashi')
