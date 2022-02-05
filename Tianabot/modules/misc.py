from Tianabot.modules.helper_funcs.chat_status import user_admin
from Tianabot.modules.disable import DisableAbleCommandHandler
from Tianabot import dispatcher

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode, Update
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext, Filters, CommandHandler

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

• <code>_italic_</code>: wrapping text with '_' will produce italic text
• <code>*bold*</code>: wrapping text with '*' will produce bold text
• <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
• <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
<b>Example:</b><code>[test](example.com)</code>

• <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
<b>Example:</b> <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@run_async
@user_admin
def echo(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    else:
        message.reply_text(
            args[1], quote=False, parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    message.delete()


def markdown_help_sender(update: Update):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see, and Use #test!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )


@run_async
def markdown_help(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.effective_message.reply_text(
            "Contact me in pm",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Markdown help",
                            url=f"t.me/{context.bot.username}?start=markdownhelp",
                        )
                    ]
                ]
            ),
        )
        return
    markdown_help_sender(update)


__help__ = """
*Available commands:*
*Markdown:*
 ❍ /markdownhelp*:* quick summary of how markdown works in telegram - can only be called in private chats
*Paste:*
 ❍ /paste*:* Saves replied content to `nekobin.com` and replies with a url
*Gps:*
 ❍ /gps <location>*:* Get gps location.
*Github:* 
 ❍ /github <username>*:* Get information about a GitHub user.
*Country:*
 ❍ /country <country name>: Gathering info about given country.
*React:*
 ❍ /react*:* Reacts with a random reaction 
*Urban Dictonary:*
 ❍ /ud <word>*:* Type the word or expression you want to search use
*Wikipedia:*
 ❍ /wiki <query>*:* wikipedia your query
*Wallpapers:*
 ❍ /wall <query>*:* get a wallpaper from wall.alphacoders.com
*Json*
 ❍ /json*:* Get Detailed info about any message
*Knowledge:*
 ❍ /define <text>*:* Type the word or expression you want to search\nFor example /define kill
 ❍ /spell*:* while replying to a message, will reply with a grammar corrected version
 *Wikipedia:*
 ❍ /wiki : For serching wikipedia.
*Telegraph:*
 ❍ /tm :Get Telegraph Link Of Replied Media
 ❍ /txt :Get Telegraph Link of Replied Text
*Translate:* 
 ❍ /tr or /tl (language code) as reply to a long message
*Example:* 
 ❍ /covid - To Get Global Stats of Covid.
 ❍ /covid <COUNTRY> - To Get Stats of A Single Country.
*Text to Speach:*
 ❍ /tts <lang code>*:* Reply to any message to get text to speech output
 ❍ /stt*:* Type in reply to a voice message(support english only) to extract text from it.
*Currency converter:* 
 ❍ /cash*:* currency converter
Example:
 `/cash 1 USD INR`  
      _OR_
 `/cash 1 usd inr`
Output: `1.0 USD = 75.505 INR`
*Language Codes*
`af,am,ar,az,be,bg,bn,bs,ca,ceb,co,cs,cy,da,de,el,en,eo,es,
et,eu,fa,fi,fr,fy,ga,gd,gl,gu,ha,haw,hi,hmn,hr,ht,hu,hy,
id,ig,is,it,iw,ja,jw,ka,kk,km,kn,ko,ku,ky,la,lb,lo,lt,lv,mg,mi,mk,
ml,mn,mr,ms,mt,my,ne,nl,no,ny,pa,pl,ps,pt,ro,ru,sd,si,sk,sl,
sm,sn,so,sq,sr,st,su,sv,sw,ta,te,tg,th,tl,tr,uk,ur,uz,
vi,xh,yi,yo,zh,zh_CN,zh_TW,zu`

"""

ECHO_HANDLER = DisableAbleCommandHandler("echo", echo, filters=Filters.group)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help)

dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)

__mod_name__ = "Exᴛʀᴀs"
__command_list__ = ["id", "echo"]
__handlers__ = [
    ECHO_HANDLER,
    MD_HELP_HANDLER,
]
