from models import Message


def get_unread_count():
    return Message.query.filter_by(is_read=False).count()