
## What's this
Cloudygram-api-server is a basic web server which sole purpose is to serve telethon's basic functionalities.
this way any desired programming language gains access to MTProto Telegram's features, via a fast and reliable python module.

For more info about telethon visit [telethon's repo.](https://github.com/LonamiWebs/Telethon)

## Cloning and running
```bash
$ git clone https://github.com/skurob/cloudygram-api-server
$ cd cloudygram-api-server
$ pip3 install -r requirements.txt
$ python3 main.py

```

Before actually running the application make sure to create a keys.json file in the root folder, containing the following:

```json
{
    "api_id": <your_api_id>,
    "api_hash": <your_api_hash>
}
```
To get your api keys simply go to [my.telegram.org](https://my.telegram.org/auth?to=apps)

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
