import requests
import json
userIdQuery = '''
query GetUserId($username: String!) {
    User(name:$username){
      id
      name
    }
  }
'''

def getUserId(username):
    try:
        userIdQueryVars = {'username': username}
        userIdQueryResponse = requests.post('https://graphql.anilist.co', json={'query': userIdQuery, 'variables': userIdQueryVars}, timeout=5)
        userId = userIdQueryResponse.json()['data']['User']['id']
        return [userId, userIdQueryResponse.json()['data']['User']['name']]
    except:
        return None

def anilistActivity(userId):
    try:
        activityQuery = '''
        query ($type: ActivityType, $page: Int, $userId: Int) {
        Page(page: $page, perPage: 1) {
            activities(userId: $userId, type: $type, sort: ID_DESC) {
            ... on ListActivity {
                id
                status
                progress
                media {
                title {
                    english
                }
                id
                type
                id
                type
                status(version: 2)
                isAdult
                episodes
                title {
                    userPreferred
                }
                bannerImage
                coverImage {
                    large
                }
                }
            }
            }
        }
        }

        '''
        activityQueryVars = {'userId': userId}
        activityQueryResponse = requests.post('https://graphql.anilist.co', json={'query': activityQuery, 'variables': activityQueryVars}, timeout=5)
        return activityQueryResponse.json()['data']['Page']['activities'][0]
    except:
        return None

def loadJSON():
    with open("anilistUsers.json", 'r') as f:
        return json.load(f)

def writeJSON(data):
    with open("anilistUsers.json", 'w') as f:
        json.dump(data, f)