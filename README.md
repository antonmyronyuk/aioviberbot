# Viber Python Bot Async API

This is async version of [viberbot](https://github.com/Viber/viber-bot-python) package. Fully compatible with sync package version.
Use this library to develop a bot for Viber platform.

The library is available on [GitHub](https://github.com/antonmyronyuk/aioviberbot) as well as a package on [PyPI](https://pypi.org/project/aioviberbot/).

This package can be imported using pip by adding the following to your `requirements.txt`:

```python
aioviberbot==0.1.3
```

## License

This library is released under the terms of the Apache 2.0 license. See [License](https://github.com/antonmyronyuk/aioviberbot/blob/main/LICENSE.md) for more information.

## Library Prerequisites

1. python >= 3.6.0
1. An Active Viber account on a platform which supports Public Accounts/ bots (iOS/Android). This account will automatically be set as the account administrator during the account creation process.
1. Active Public Account/bot - Create an account [here](https://partners.viber.com/account/create-bot-account).
1. Account authentication token - unique account identifier used to validate your account in all API requests. Once your account is created your authentication token will appear in the account’s “edit info” screen (for admins only). Each request posted to Viber by the account will need to contain the token.
1. Webhook - Please use a server endpoint URL that supports HTTPS. If you deploy on your own custom server, you'll need a trusted (ca.pem) certificate, not self-signed. Read our [blog post](https://developers.viber.com/blog/2017/05/24/test-your-bots-locally) on how to test your bot locally.

## Contributing

If you think that there's a bug or there's anything else needed to be changed and you want to change it yourself, you can always create a new Pull request.  
Please make sure that your change doesn't break anything and all the unit tests passes.  
Also, please make sure that the current tests cover your change, if not please add tests.  
  
We are using pytest, so if you want to run the tests from the commandline just follow the relevant steps after cloning the repo and creating your branch:  


```
# installing the dependencies:  
python setup.py develop

# run the unit tests
pytest tests/
``` 

## Let's get started!


### Installing

Creating a basic Viber bot is simple:

1. Install the library with pip `pip install aioviberbot`
2. Import `aioviberbot.api` library to your project
3. Create a Public Account or bot and use the API key from [https://developers.viber.com](https://developers.viber.com)
4. Configure your bot as described in the documentation below
5. Start your web server
6. Call `set_webhook(url)` with your web server url

## A simple Echo Bot

### Firstly, let's import and configure our bot

```python
from aioviberbot import Api
from aioviberbot.api.bot_configuration import BotConfiguration

bot_configuration = BotConfiguration(
    name='PythonSampleBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token='YOUR_AUTH_TOKEN_HERE',
)
viber = Api(bot_configuration)
```

### Create an HTTPS server

Next thing you should do is starting a https server.
and yes, as we said in the prerequisites it has to be https server. Create a server however you like, for example with `aiohttp`:

```python
from aiohttp import web


async def webhook(request: web.Request) -> web.Response:
    request_data = await request.read()
    logger.debug('Received request. Post data: %s', request_data)
    # handle the request here
    return web.json_response({'ok': True})


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('POST', '/webhook', webhook),
    web.run_app(app)
```

### Setting a webhook

After the server is up and running you can set a webhook.
Viber will push messages sent to this URL. web server should be internet-facing.

```python
await viber.set_webhook('https://mybotwebserver.com:443/')
```

### Logging

This library uses the standard python logger. If you want to see its logs you can configure the logger:

```python
logger = logging.getLogger('aioviberbot')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### Do you supply a basic types of messages?
Well, funny you ask. Yes we do. All the Message types are located in `aioviberbot.api.messages` package. Here's some examples:

```python
from aioviberbot.api.messages import (
    TextMessage,
    ContactMessage,
    PictureMessage,
    VideoMessage,
)
from aioviberbot.api.messages.data_types.contact import Contact

# creation of text message
text_message = TextMessage(text='sample text message!')

# creation of contact message
contact = Contact(name='Viber user', phone_number='0123456789')
contact_message = ContactMessage(contact=contact)

# creation of picture message
picture_message = PictureMessage(text='Check this', media='http://site.com/img.jpg')

# creation of video message
video_message = VideoMessage(media='http://mediaserver.com/video.mp4', size=4324)
```

Have you noticed how we created the `TextMessage`? There's all bunch of message types you should get familiar with.

* [Text Message](#TextMessage)
* [Url Message](#UrlMessage)
* [Contact Message](#ContactMessage)
* [Picture Message](#PictureMessage)
* [Video Message](#VideoMessage)
* [Location Message](#LocationMessage)
* [Sticker Message](#StickerMessage)
* [Rich Media Message](#RichMediaMessage)
* [Keyboard Message](#KeyboardMessage)

Creating them is easy! Every message object has it's own unique constructor corresponding to it's API implementation, click on them to see it!
Check out the full API documentation for more advanced uses.

### Let's add it all up and reply with a message!

```python
from aiohttp import web

from aioviberbot import Api
from aioviberbot.api.bot_configuration import BotConfiguration
from aioviberbot.api.messages.text_message import TextMessage
from aioviberbot.api.viber_requests import ViberConversationStartedRequest
from aioviberbot.api.viber_requests import ViberMessageRequest
from aioviberbot.api.viber_requests import ViberSubscribedRequest

viber = Api(BotConfiguration(
    name='PythonSampleBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token='YOUR_AUTH_TOKEN_HERE'
))


async def webhook(request: web.Request) -> web.Response:
    request_data = await request.read()
    signature = request.headers.get('X-Viber-Content-Signature')
    if not viber.verify_signature(request_data, signature):
        raise web.HTTPForbidden

    viber_request = viber.parse_request(request_data)
    if isinstance(viber_request, ViberMessageRequest):
        # echo message
        await viber.send_messages(
            viber_request.sender.id,
            [viber_request.message],
        )
    elif isinstance(viber_request, ViberSubscribedRequest):
        await viber.send_messages(
            viber_request.user.id,
            [TextMessage(text='Thanks for subscribing!')],
        )
    elif isinstance(viber_request, ViberConversationStartedRequest):
        await viber.send_messages(
            viber_request.user.id,
            [TextMessage(text='Thanks for starting conversation!')],
        )

    return web.json_response({'ok': True})


async def set_webhook_signal(app: web.Application):
    await viber.set_webhook('https://mybotwebserver.com/webhhok')


if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(set_webhook_signal)
    app.router.add_route('POST', '/webhook', webhook),
    web.run_app(app)
```

As you can see there's a bunch of `Request` types here's a list of them.

## Viber API

### Api class

`from aioviberbot import Api`

* Api
    * [init(bot\_configuration, client\_session)](#new-Api())
    * [.set\_webhook(url, webhook_events)](#set_webhook) ⇒ `List of registered event_types`
    * [.unset\_webhook()](#unset_webhook) ⇒ `None`
    * [.get\_account_info()](#get_account_info) ⇒ `object`
    * [.verify\_signature(request\_data, signature)](#verify_signature) ⇒ `boolean`
    * [.parse\_request(request\_data)](#parse_request) ⇒ `ViberRequest`
    * [.send\_messages(to, messages)](#send_messages) ⇒ `list of message tokens sent`
    * [.get\_online(viber\_user\_ids)](#get_online) ⇒ `dictionary of users status`
    * [.get\_user_details(viber\_user\_id)](#get_user_details) ⇒ `dictionary of user's data`
    * [.post\_messages\_to\_public\_account(to, messages)](#post_to_pa) ⇒ `list of message tokens sent`

<a name="new-Api()"></a>

### New Api()

| Param              | Type     | Description                                                                                 |
|--------------------|----------|---------------------------------------------------------------------------------------------|
| bot\_configuration | `object` | `BotConfiguration`                                                                          |
| client\_session    | `object` | Optional `aiohttp.ClientSession`, pass if you want to use your own session for api requests |

<a name="set_webhook"></a>

### Api.set\_webhook(url)

| Param | Type | Description |
| --- | --- | --- |
| url | `string` | Your web server url |
| webhook\_events | `list` | optional list of subscribed events |

Returns `List of registered event_types`. 

```python
event_types = await viber.set_webhook('https://example.com/webhook')
```

<a name="unset_webhook"></a>

### Api.unset\_webhook()

Returns `None`. 

```python
await viber.unset_webhook()
```

<a name="get_account_info"></a>

### Api.get\_account\_info()

Returns an `object` [with the following JSON](https://developers.viber.com/docs/api/rest-bot-api/#get-account-info). 

```python
account_info = await viber.get_account_info()
```

<a name="verify_signature"></a>

### Api.verify\_signature(request\_data, signature)

| Param | Type | Description |
| --- | --- | --- |
| request\_data | `string` | the post data from request |
| signature | `string` | sent as header `X-Viber-Content-Signature` |


Returns a `boolean` suggesting if the signature is valid. 

```python
if not viber.verify_signature(await request.read(), request.headers.get('X-Viber-Content-Signature')):
    raise web.HTTPForbidden
```

<a name="parse_request"></a>

### Api.parse\_request(request\_data)

| Param | Type | Description |
| --- | --- | --- |
| request\_data | `string` | the post data from request |

Returns a `ViberRequest` object. 

There's a list of [ViberRequest objects](#ViberRequest)

```python
viber_request = viber.parse_request(await request.read())
```

<a name="send_messages"></a>

### Api.send\_messages(to, messages)

| Param | Type | Description |
| --- | --- | --- |
| to | `string` | Viber user id |
| messages | `list` | list of `Message` objects |

Returns `list` of message tokens of the messages sent. 

```python
tokens = await viber.send_messages(
    to=viber_request.sender.id,
    messages=[TextMessage(text='sample message')],
)
```

<a name="post_to_pa"></a>

### Api.post\_messages\_to\_public\_account(to, messages)

| Param | Type | Description |
| --- | --- | --- |
| sender | `string` | Viber user id |
| messages | `list` | list of `Message` objects |

Returns `list` of message tokens of the messages sent. 

```python
tokens = await viber.post_messages_to_public_account(
    sender=viber_request.sender.id,
    messages=[TextMessage(text='sample message')],
)
```

<a name="get_online"></a>

### Api.get\_online(viber\_user\_ids)

| Param | Type | Description |
| --- | --- | --- |
| viber\_user\_ids | `array of strings` | Array of Viber user ids |

Returns a `dictionary of users`.

```python
users = await viber.get_online(['user1id', 'user2id'])
```

<a name="get_user_details"></a>

### Api.get\_user\_details(viber\_user\_id)

| Param | Type | Description |
| --- | --- | --- |
| viber\_user\_ids | `string` | Viber user id |

The `get_user_details` function will fetch the details of a specific Viber user based on his unique user ID. The user ID can be obtained from the callbacks sent to the account regarding user's actions. This request can be sent twice during a 12 hours period for each user ID.

```python
user_data = await viber.get_user_details('userId')
```

<a name="ViberRequest"></a>

### Request object

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | according to `EventTypes` enum |
| timestamp | `long` | Epoch of request time |

* ViberRequest
    * .event\_type ⇒ `string `
    * .timestamp ⇒ `long`

<a name="ConversationStarted"></a>

#### ViberConversationStartedRequest object

Inherits from [ViberRequest](#ViberRequest)

Conversation started event fires when a user opens a conversation with the Public Account/ bot using the “message” button (found on the account’s info screen) or using a [deep link](https://developers.viber.com/docs/tools/deep-links).

This event is **not** considered a subscribe event and doesn't allow the account to send messages to the user; however, it will allow sending one "welcome message" to the user. See [sending a welcome message](#SendingWelcomeMessage) below for more information. 

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.CONVERSATION_STARTED` |
| message\_token | `string` | Unique ID of the message |
| type | `string` | The specific type of `conversation_started` event. |
| context | `string` | Any additional parameters added to the deep link used to access the conversation passed as a string |
| user | `UserProfile` | the user started the conversation [UserProfile](#UserProfile) |
| subscribed | `boolean` | Indicates whether a user is already subscribed |

* ViberConversationStartedRequest
    * message\_token ⇒ `string`
    * type ⇒ `string`
    * context ⇒ `string`
    * user ⇒ `UserProfile`

#### ViberDeliveredRequest object

Inherits from [ViberRequest](#ViberRequest)

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.DELIVERED` |
| message\_token | `string` | Unique ID of the message |
| user\_id | `string` | Unique Viber user id |

* ViberDeliveredRequest
    * message\_token ⇒ `string`
    * user\_id ⇒ `string`

#### ViberFailedRequest object

Inherits from [ViberRequest](#ViberRequest)

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.FAILED` |
| message\_token | `string` | Unique ID of the message |
| user\_id | `string` | Unique Viber user id |
| desc | `string` | Failure description |

* ViberFailedRequest
    * message\_token ⇒ `string`
    * user\_id ⇒ `string`
    * desc ⇒ `string`

#### ViberMessageRequest object

Inherits from [ViberRequest](#ViberRequest)

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.MESSAGE` |
| message\_token | `string` | Unique ID of the message |
| message | `Message` | `Message` object |
| sender | `UserProfile` | the user started the conversation [UserProfile](#UserProfile) |

* ViberMessageRequest
    * message\_token ⇒ `string`
    * message ⇒ `Message`
    * sender ⇒ `UserProfile`

#### ViberSeenRequest object

Inherits from [ViberRequest](#ViberRequest)

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.SEEN` |
| message\_token | `string` | Unique ID of the message |
| user\_id | `string` | Unique Viber user id |

* ViberSeenRequest
    * message\_token ⇒ `string`
    * user\_id ⇒ `string`

#### ViberSubscribedRequest object

Inherits from [ViberRequest](#ViberRequest)

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.SUBSCRIBED` |
| user | `UserProfile` | the user started the conversation [UserProfile](#UserProfile) |

* ViberSubscribedRequest
    * user ⇒ `UserProfile`

#### ViberUnsubscribedRequest object

Inherits from [ViberRequest](#ViberRequest)

| Param | Type | Notes |
| --- | --- | --- |
| event\_type | `string` | always equals to the value of `EventType.UNSUBSCRIBED` |
| user\_id | `string` | Unique Viber user id |

* ViberUnsubscribedRequest
    * get\_user\_id() ⇒ `string`

<a name="UserProfile"></a>

### UserProfile object

| Param | Type | Notes |
| --- | --- | --- |
| id | `string` | --- |
| name | `string` | --- |
| avatar | `string` | Avatar URL |
| country | `string` | **currently set in `CONVERSATION_STARTED` event only** |
| language | `string` | **currently set in `CONVERSATION_STARTED` event only** |

<a name="MessageObject"></a>

### Message Object

**Common Members for `Message` interface**:

| Param | Type | Description |
| --- | --- | --- |
| timestamp | `long` | Epoch time |
| keyboard | `JSON` | keyboard JSON |
| trackingData | `JSON` | JSON Tracking Data from Viber Client |

**Common Constructor Arguments `Message` interface**:

| Param | Type | Description |
| --- | --- | --- |
| optionalKeyboard | `JSON` | [Writing Custom Keyboards](https://developers.viber.com/docs/tools/keyboards) |
| optionalTrackingData | `JSON` | Data to be saved on Viber Client device, and sent back each time message is received |

<a name="TextMessage"></a>

#### TextMessage object

| Member | Type
| --- | --- |
| text | `string` |

```python
message = TextMessage(text='my text message')
```

<a name="UrlMessage"></a>

#### URLMessage object

| Member | Type | Description |
| --- | --- | --- |
| media | `string` | URL string |

```python
message = URLMessage(media='http://my.siteurl.com')
```

<a name="ContactMessage"></a>

#### ContactMessage object

| Member | Type
| --- | --- |
| contact | `Contact` |

```python
from aioviberbot.api.messages.data_types.contact import Contact

contact = Contact(name='Viber user', phone_number='+0015648979', avatar='http://link.to.avatar')
contact_message = ContactMessage(contact=contact)
```

<a name="PictureMessage"></a>

#### PictureMessage object

| Member | Type | Description |
| --- | --- | --- |
| media | `string` | url of the message (jpeg only) |
| text | `string` |  |
| thumbnail | `string` |  |

```python
message = PictureMessage(media='http://www.thehindubusinessline.com/multimedia/dynamic/01458/viber_logo_JPG_1458024f.jpg', text='Viber logo')
```

<a name="VideoMessage"></a>

#### VideoMessage object

| Member | Type | Description |
| --- | --- | --- |
| media | `string` | url of the video |
| size | `int` |  |
| thumbnail | `string` |  |
| duration | `int` |  |

```python
message = VideoMessage(media='http://site.com/video.mp4', size=21499)
```

<a name="LocationMessage"></a>

#### LocationMessage object

| Member | Type
| --- | --- |
| location | `Location` |

```python
from aioviberbot.api.messages.data_types.location import Location

location = Location(lat=0.0, lon=0.0)
location_message = LocationMessage(location=location)
```

<a name="StickerMessage"></a>

#### StickerMessage object

| Member | Type
| --- | --- |
| sticker\_id | `int` |

```python
message = StickerMessage(sticker_id=40100)
```

<a name="FileMessage"></a>

#### FileMessage object

| Member | Type
| --- | --- |
| media | `string` |
| size | `long` |
| file\_name | `string` |

```python
message = FileMessage(media=url, size=size_in_bytes, file_name=file_name)
```

<a name="RichMediaMessage"></a>

#### RichMediaMessage object

| Member | Type
| --- | --- |
| rich\_media | `string` (JSON) |

```python
SAMPLE_RICH_MEDIA = """{
  "BgColor": "#69C48A",
  "Buttons": [
    {
      "Columns": 6,
      "Rows": 1,
      "BgColor": "#454545",
      "BgMediaType": "gif",
      "BgMedia": "http://www.url.by/test.gif",
      "BgLoop": true,
      "ActionType": "open-url",
      "Silent": true,
      "ActionBody": "www.tut.by",
      "Image": "www.tut.by/img.jpg",
      "TextVAlign": "middle",
      "TextHAlign": "left",
      "Text": "<b>example</b> button",
      "TextOpacity": 10,
      "TextSize": "regular"
    }
  ]
}"""

SAMPLE_ALT_TEXT = 'upgrade now!'

message = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, alt_text=SAMPLE_ALT_TEXT)
```

<a name="KeyboardMessage"></a>

#### KeyboardMessage object

| Member | Type
| --- | --- |
| keyboard | `JSON` |
| tracking_data | `JSON` |

```python
message = KeyboardMessage(tracking_data=tracking_data, keyboard=keyboard)
```

<a name="SendingWelcomeMessage"></a>

### Sending a welcome message

The Viber API allows sending messages to users only after they subscribe to the account. However, Viber will allow the account to send one “welcome message” to a user as the user opens the conversation, before the user subscribes.

The welcome message will be sent as a response to a `conversation_started` callback, which will be received from Viber once the user opens the conversation with the account. To learn more about this event and when is it triggered see [`Conversation started`](#ConversationStarted) in the callbacks section.

#### Welcome message flow

Sending a welcome message will be done according to the following flow:

1. User opens 1-on-1 conversation with account.
2. Viber server send `conversation_started` even to PA’s webhook.
3. The account receives the `conversation_started` and responds with an HTTP response which includes the welcome message as the response body.

The welcome message will be a JSON constructed according to the send_message requests structure, but without the `receiver` parameter. An example welcome message would look like this:

```python
async def webhook(request: web.Request) -> web.Response:
    request_data = await request.read()
    viber_request = viber.parse_request(request_data)

    if isinstance(viber_request, ViberConversationStartedRequest):
        await viber.send_messages(
            viber_request.user.id,
            [TextMessage(text='Welcome!')],
        )

    return web.json_response({'ok': True})
```

## Community

Join the conversation on **[Gitter](https://gitter.im/viber/bot-python)**.
