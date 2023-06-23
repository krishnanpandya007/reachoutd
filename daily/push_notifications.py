'''
Currently Accepted push notification types:
new_follower {..., 'follower_id': STR} [X],
social_tap:2H {..., 'tapper_id': STR} [X],
link_social(GENERAL):10D: Link XYZ social, cause getting more click nowadays.
add touchUps(GENERAL):10D: Link your bio to get recognised who you are.

'''


import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('reachout_firebase_creds.json')
firebase_admin.initialize_app(cred)

# Create a message
# message = messaging.Message(
#     notification=messaging.Notification(
#         title='Krishnan Pandya followed you!',
#         body='Tap to view their profile.'
#     ),
#     token='dfCZq7fPSteFTtCydzDcas:APA91bHKJkyvXc3w_zDjls-9pKE4YB1G6tnL5zGPADw5p4AheL2OTPUpfZs8NdMBQ1TpfL0jAVxvrnzXtvY3SUEFWQOLm0lRP6XlBsl4ZTNRtXzLmAiJ8d1MB7UTEewa4utDBrTrA0lf',
#     data={'type': 'new_follower', 'follower_id': '4', 'click_action': 'FLUTTER_NOTIFICATION_CLICK'}
# )

# # Send the message
# response = messaging.send(message)

# print('Notification sent successfully:', response)
'''
Task to manage:
No redundant notifications
spam-proof
'''
messages = [
    messaging.Message(
        notification=messaging.Notification(
            title='Notification Title',
            body='Notification Body'
        ),
        token='dfCZq7fPSteFTtCydzDcas:APA91bHKJkyvXc3w_zDjls-9pKE4YB1G6tnL5zGPADw5p4AheL2OTPUpfZs8NdMBQ1TpfL0jAVxvrnzXtvY3SUEFWQOLm0lRP6XlBsl4ZTNRtXzLmAiJ8d1MB7UTEewa4utDBrTrA0lf',
        data={'click_action': 'FLUTTER_NOTIFICATION_CLICK'}
    ),
    messaging.Message(
        notification=messaging.Notification(
            title='Notification Title',
            body='Notification Body'
        ),
        token='device_token_2',
        data={'click_action': 'FLUTTER_NOTIFICATION_CLICK'}
    ),
    # Add more messages as needed
]

# Send the batch of messages
response = messaging.send_all(messages)

# Check the individual responses
for individual_response in list(response.responses):
    print('Notification sent successfully:', individual_response)

print('Batch notification sent successfully.')