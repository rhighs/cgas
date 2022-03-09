## What's this
Cloudygram-api-server is a basic web server which sole purpose is to serve telethon's basic functionalities.
Think of it as a microservice with a much bigger picture in mind.

For more info about telethon visit [telethon's repo.](https://github.com/LonamiWebs/Telethon)

## Cloning and running
```bash
$ git clone https://github.com/skurob/cloudygram-api-server
$ cd cloudygram-api-server
$ pip3 install -r requirements.txt
$ mkdir sessions
$ python3 main.py
```

Before actually running the application make sure to create a keys.json file in the project root, containing the following:
```json
{
    "api_id": <your_api_id>,
    "api_hash": <your_api_hash>
}
```
To get your api keys simply go to [my.telegram.org](https://my.telegram.org/auth?to=apps)

# Getting started
When running the server for the first time, make sure to create a sessions/ folder in the project root directory, this is where telethon will place all the session files for each account you are going to log in.

## Receive a code
Path: `/sendCode?phoneNumber=<international_formatted_number>`\
Calling the path above via GET method you will receive a json response as follows:
```json
{
    "isSuccess": true,
    "phoneCodeHash": "<hash_here>"
}
```
along with an official telegram message indicating the received confirmation code to use in the next step.

## Validating your code
Path: `/signin`\
All you need to do now is calling via the api via POST method, passing a json body as follows:
```json
{
    "phoneNumber": "<international_formatted_number>",
    "phoneCode": "<the_received_code>",
    "phoneCodeHash": "<from_the_previous_request>"
}
```
If everything ran smoothly you will receive a positive response and a telegram notification, telling you successfully logged via the cloudygram-api-server.

## Getting user informations
Path: `/user/<international_formatted_number>/userInfo`\
Just a simple GET request

js example:
```js
const url = "http://127.0.0.1:5000/user/+393421323295/userInfo";
const getUserInfo = (url) => fetch(url, { method: "GET" })
                           .then(res => res.json());

console.log(await get_user_info(url));

/*
{
    "userId": 12314,
    "username": "foobar",
    "firstName": "foo",
    "lastName": "bar",
    "phoneNumber": +393421323295
}
*/
```
## Getting messages in a chat
Path: `/user/<international_formatted_number>/messages/getMessages`\
This api call requires you to already have a chat-id from which you want to fetch its messages, there are few ways to do this but none are provided by this application.\
To get a chat-id possible solutions are:

- Getting it using telethon message events.
- Using a [tdlib](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1search_public_chats.html) function which will search for chats given a username.

When successfully called this method, you will then receive a response like so:
```json
{
    "isSuccess": true,
    "data": [
        {
            "message object": "containing info"
        },
        {
            "another message object": "containing info"
        }
    ]
}
```

## Session management
Whichever usecase you will face, it might happen that your sessions are no longer valid, this can
happen after a manual deletion of the cloudygram device via the telegram app, to avoid getting
yourself into annoying errors, I've provided two api calls in which you can check the
state of a session, and eventually clean all the non-valid sessions handled by the server.
To do this you can use the following resources.

`GET /user/<international_formatted_number>/sessionValid` "is this session valid?".\
`DELETE /cleanSessions` deletes all non-valid sessions.

These resources always return a json object with a bool field `isSuccess`.

## Contributing
This project does NOT aim at becoming a 1:1 Telethon API but rather aims at the essentials only, if you have any suggestion
pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

```
MIT License

Copyright (c) 2021 Roberto Montalti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
