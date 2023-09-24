# Get user access_token in VK
Official docs: https://dev.vk.com/ru/api/access-token/authcode-flow-user

Variables: ![](<Screenshot 2023-09-24 at 15.30.21-1.png>)

1. Go to this side from user account: 
`https://oauth.vk.com/authorize?client_id={app_id}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,offline&response_type=code&v=5.154`

You will get this GET responce: 
`REDIRECT_URI?code=7a6fa4dff77a228eeda56603b8f53806c883f011c40b72630bb50df056f6479e52a`

2. Go to this link with new code above:

`https://oauth.vk.com/access_token?client_id={app_id}&client_secret={protected_key_from_app_settings}&redirect_uri=https://oauth.vk.com/blank.html&code=
7634eed941193a01b2`

