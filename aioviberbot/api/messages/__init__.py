from aioviberbot.api.errors import ViberValidationError
from aioviberbot.api.messages.contact_message import ContactMessage
from aioviberbot.api.messages.file_message import FileMessage
from aioviberbot.api.messages.picture_message import PictureMessage
from aioviberbot.api.messages.sticker_message import StickerMessage
from aioviberbot.api.messages.url_message import URLMessage
from aioviberbot.api.messages.video_message import VideoMessage
from aioviberbot.api.messages.message_type import MessageType
from aioviberbot.api.messages.text_message import TextMessage
from aioviberbot.api.messages.location_message import LocationMessage
from aioviberbot.api.messages.rich_media_message import RichMediaMessage
from aioviberbot.api.messages.keyboard_message import KeyboardMessage

MESSAGE_TYPE_TO_CLASS = {
    MessageType.URL: URLMessage,
    MessageType.LOCATION: LocationMessage,
    MessageType.PICTURE: PictureMessage,
    MessageType.CONTACT: ContactMessage,
    MessageType.FILE: FileMessage,
    MessageType.TEXT: TextMessage,
    MessageType.VIDEO: VideoMessage,
    MessageType.STICKER: StickerMessage,
    MessageType.RICH_MEDIA: RichMediaMessage,
    MessageType.KEYBOARD: KeyboardMessage
}


def get_message(message_dict):
    if 'type' not in message_dict:
        raise ViberValidationError("message data doesn't contain a type")

    if message_dict['type'] not in MESSAGE_TYPE_TO_CLASS:
        raise ViberValidationError(
            "message type '{0}' is not supported".format(message_dict['type']),
        )

    return MESSAGE_TYPE_TO_CLASS[message_dict['type']]().from_dict(message_dict)


__all__ = [
    'TextMessage', 'ContactMessage', 'FileMessage', 'LocationMessage',
    'PictureMessage', 'StickerMessage', 'URLMessage', 'VideoMessage',
    'RichMediaMessage', 'MessageType', 'KeyboardMessage', 'get_message',
]
