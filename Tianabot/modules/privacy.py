from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update, Bot
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CommandHandler, CallbackQueryHandler, run_async

from Tianabot import dispatcher, DRAGONS, DEV_USERS

PRIVACY_P_TEXT = """
* Our contact details * \n*Name*: TianaBot \n*Telegram*: https://t.me/TianaxSupport
\n\nThe bot has been made to *protect* and preserve *privacy* as best as possible. \nThe proper functioning of the bot is defined as the data required for all the commands in the /help to work as expected.
\n\nOur privacy policy may change from time to time. If we make any material changes to our policies, we will place a prominent notice on https://t.me/TianaxUpdates.
"""

PRIVACY_STRING = """Select one of the below options for more information about how the bot handles your privacy."""

CANCEL_STRING = """Privacy deletion request cancelled."""

@run_async
def privacy(update, context):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            PRIVACY_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="Privacy Policy", callback_data="policy_")
                  ],
                 [
                    InlineKeyboardButton(text="Retrieve data", callback_data="policy_data"),
                    InlineKeyboardButton(text="Delete data", callback_data="policy_datadel")
                  ],
                 [
                    InlineKeyboardButton(text="Cancel", callback_data="cancel_")
                 ] 
                ]
            ),
        )

    else:
        try:
            bot.send_message(
                user.id,
                PRIVACY_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "This command can only used in private!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in pm for privacy information."
            )

@run_async
def greyson_policy_callback(update, context):
    query = update.callback_query
    if query.data == "policy_":
        query.message.edit_text(
            text=""" * Our contact details * \n*Name*: Tianabot \n*Telegram*: https://t.me/TianaxSupport
\nThe bot has been made to *protect* and preserve *privacy* as best as possible. \nThe proper functioning of the bot is defined as the data required for all the commands in the /help to work as expected.
\nOur privacy policy may change from time to time. If we make any material changes to our policies, we will place a prominent notice on https://t.me/TianaxSupport.""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="What information we collect", callback_data="policy_wiwc")
                  ],
                 [
                    InlineKeyboardButton(text="Why we collect it", callback_data="policy_wwci")
                  ],
                 [
                    InlineKeyboardButton(text="What we do", callback_data="policy_wwd")
                  ],
                 [
                    InlineKeyboardButton(text="What we DO NOT do", callback_data="policy_wwdnd")
                  ],
                 [
                    InlineKeyboardButton(text="Rights to process", callback_data="policy_rtp")
                 ] 
                ]
            ),
        )
    elif query.data == "policy_wiwc":
        query.message.edit_text(
            text=f"* The type of personal information we collect *"
            f"\n\nWe currently collect and process the following information:"
            f"\n  • Telegram UserID, firstname, lastname, username _(Note:_ These are your public telegram details. We do not know your *real* details.)"
            f"   • Chat memberships (The list of all chats you have been seen interacting in) \n  • Settings or configurations as set through any commands (For example, welcome settings, notes, filters, etc)"
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="• What information we collect •", callback_data="policy_wiwc")
                  ],
                 [
                    InlineKeyboardButton(text="Why we collect it", callback_data="policy_wwci")
                  ],
                 [
                    InlineKeyboardButton(text="What we do", callback_data="policy_wwd")
                  ],
                 [
                    InlineKeyboardButton(text="What we DO NOT do", callback_data="policy_wwdnd")
                  ],
                 [
                    InlineKeyboardButton(text="Rights to process", callback_data="policy_rtp")
                  ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="policy_")
                 ] 
                ]
            ),
        )
    elif query.data == "policy_wwci":
        query.message.edit_text(
            text=f"* How we get the personal information and why we have it *"
            f"\n\nMost of the personal information we process is provided to us directly by you for one of the following reasons:"
            f"\n    • You've messaged the bot directly. This can be to read the complete a CAPTCHA, read the documentation, etc."
            f"\n    • You've opted to save your messages through the bot. \n\nWe also receive personal information indirectly, from the following sources in the following scenarios: \n    • You're part of a group, or channel, which uses this bot."
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="What information we collect", callback_data="policy_wiwc")
                  ],
                 [
                    InlineKeyboardButton(text="• Why we collect it •", callback_data="policy_wwci")
                  ],
                 [
                    InlineKeyboardButton(text="What we do", callback_data="policy_wwd")
                  ],
                 [
                    InlineKeyboardButton(text="What we DO NOT do", callback_data="policy_wwdnd")
                  ],
                 [
                    InlineKeyboardButton(text="Rights to process", callback_data="policy_rtp")
                  ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="policy_")
                 ] 
                ]
            ),
        )
    elif query.data == "policy_wwd":
        query.message.edit_text(
            text=f"* What we do with the personal information *"
            f"\n\nWe use the information that you have given us in order to support various bot features. This can include:"
            f"\n    • User ID/username pairing, which allows the bot to resolve usernames to valid user ids."
            f"\n    • Chat memberships, which allows for federations to know where to ban from, and determine which bans are of importance to you. \n    • Storing certain messages that have been explicitly saved. (eg through notes, filters, welcomes, etc)"
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="What information we collect", callback_data="policy_wiwc")
                  ],
                 [
                    InlineKeyboardButton(text="Why we collect it", callback_data="policy_wwci")
                  ],
                 [
                    InlineKeyboardButton(text="• What we do •", callback_data="policy_wwd")
                  ],
                 [
                    InlineKeyboardButton(text="What we DO NOT do", callback_data="policy_wwdnd")
                  ],
                 [
                    InlineKeyboardButton(text="Rights to process", callback_data="policy_rtp")
                  ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="policy_")
                 ] 
                ]
            ),
        )
    elif query.data == "policy_wwdnd":
        query.message.edit_text(
            text=f"* What we DO NOT do with the personal information *"
            f"\n\nWe *DO NOT*:"
            f"\n    • store any messages, unless explicitly saved (eg through notes, filters, welcomes etc). \n    • use technologies like beacons or unique device identifiers to identify you or your device."
            f"\n    • knowingly contact or collect personal information from children under 13. If you believe we have inadvertently collected such information, please contact us so we can promptly obtain parental consent or remove the information. \n    • share any sensitive information with any other organisations or individuals."
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="What information we collect", callback_data="policy_wiwc")
                  ],
                 [
                    InlineKeyboardButton(text="Why we collect it", callback_data="policy_wwci")
                  ],
                 [
                    InlineKeyboardButton(text="What we do", callback_data="policy_wwd")
                  ],
                 [
                    InlineKeyboardButton(text="• What we DO NOT do •", callback_data="policy_wwdnd")
                  ],
                 [
                    InlineKeyboardButton(text="Rights to process", callback_data="policy_rtp")
                  ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="policy_")
                 ] 
                ]
            ),
        )
    elif query.data == "policy_rtp":
        query.message.edit_text(
            text=f"* Rights to process *"
            f"\n\nUnder the General Data Protection Regulation (GDPR), the lawful bases we rely on for processing this information are:"
            f"\n    • Your consent. You are able to remove your consent at any time. You can do this by using the tools provided to delete your data, which will delete any data that isnt critical to bot functionality. \n    • We need it to perform a public task. Namely, allowing group or channel admins to protect their chats."
            f"\n    • We have a legitimate interest: The data collected and retained is essential to the functioning of the bot. Admins add this bot to protect their chats, and certain data is required to guarantee this."
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="What information we collect", callback_data="policy_wiwc")
                  ],
                 [
                    InlineKeyboardButton(text="Why we collect it", callback_data="policy_wwci")
                  ],
                 [
                    InlineKeyboardButton(text="What we do", callback_data="policy_wwd")
                  ],
                 [
                    InlineKeyboardButton(text="What we DO NOT do", callback_data="policy_wwdnd")
                  ],
                 [
                    InlineKeyboardButton(text="• Rights to process •", callback_data="policy_rtp")
                  ],
                 [
                    InlineKeyboardButton(text="Back", callback_data="policy_")
                 ] 
                ]
            ),
        )
    elif query.data == "policy_datadel":
        query.message.edit_text(
            text="""Are you sure you want to delete your data?

Note that this will:
- delete all notes/filters you have saved to your private chat.
- delete your federation.
- remove your admin status in other federations.
- remove all your approvals from all chats.

This action **CANNOT** be undone.""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                  [
                    InlineKeyboardButton(text="Yes, delete all my data.", callback_data="policy_del")
                  ],
                 [
                    InlineKeyboardButton(text="No, I changed my mind!", callback_data="cancel_")
                  ]
                ]
            ),
        )
    elif query.data == "policy_del": 
        query.message.edit_text(
            text="""Your data has been deleted.""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
          )
    elif query.data == "policy_data": 
        query.message.edit_text(
            text="""These feature coming soon.""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
          )


@run_async
def greyson_cancel_callback(update, context):
    query = update.callback_query
    if query.data == "cancel_": 
        query.message.edit_text(
            text=""" Privacy deletion request cancelled.""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
          )

__mod_name__ = "Pʀɪᴠᴀᴄʏ"

__help__ = """
The privacy module allows you to see the bot privacy policy, as well as view and delete the data the bot stores about you.

*The single command which can only be used in PM:*
- /privacy: Provides all the tools relating to privacy, such as listing the privacy policy, retrieving, and deleting your data.
"""

policy_callback_handler = CallbackQueryHandler(greyson_policy_callback, pattern=r"policy_")
cancel_callback_handler = CallbackQueryHandler(greyson_cancel_callback, pattern=r"cancel_")

privacy_handler = CommandHandler("privacy", privacy)

dispatcher.add_handler(privacy_handler)
dispatcher.add_handler(cancel_callback_handler)
dispatcher.add_handler(policy_callback_handler)
