import threading

from sqlalchemy import Column, String

from Tianabot.modules.sql import BASE, SESSION


class MerissaChats(BASE):
    __tablename__ = "merissa_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


MerissaChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_merissa(chat_id):
    try:
        chat = SESSION.query(MerissaChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_merissa(chat_id):
    with INSERTION_LOCK:
        merissachat = SESSION.query(MerissaChats).get(str(chat_id))
        if not merissachat:
            merissachat = MerissaChats(str(chat_id))
        SESSION.add(merissachat)
        SESSION.commit()


def rem_merissa(chat_id):
    with INSERTION_LOCK:
        merissachat = SESSION.query(MerissaChats).get(str(chat_id))
        if merissachat:
            SESSION.delete(merissachat)
        SESSION.commit()


def get_all_merissa_chats():
    try:
        return SESSION.query(MerissaChats.chat_id).all()
    finally:
        SESSION.close()
