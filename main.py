import telebot
from telebot import types
from yandex_music import Client
tok_yan='y0_AgAAAAB3mDMcAAG8XgAAAAEMZsquAAAaSyWxvkhK-r7fhDdq3Wr_aViZFg'
bot=telebot.TeleBot('6791586849:AAE87uxZEtQv9r2vdI0I4QWiZbERaQQ2qus')
client = Client(tok_yan).init()
@bot.message_handler(commands=['start'])
def st(message):
    mrkp=types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton('Запустить🚀',switch_inline_query_current_chat='/start')
    mrkp.row(btn1)
    bot.reply_to(message, f'Привет,{message.from_user.first_name}! Ботик работает и в inline режиме!',reply_markup=mrkp)
@bot.inline_handler(lambda query: len(query.query)==0)
def loh_query(query):
    hint = "Введите запрос!"
    f='https://papik.pro/grafic/uploads/posts/2023-04/1682737564_papik-pro-p-nedovolnii-smail-odnoklassniki-png-21.jpg'
    try:
        r = types.InlineQueryResultArticle(
                id='1',
                title="Кажется, вы ничего не ввели",
                description=hint,
                input_message_content=types.InputTextMessageContent(
                message_text="Эх, зря я не ввёл запрос :("),
                thumbnail_url=f,
                thumbnail_width=48,
                thumbnail_height=48
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)
@bot.inline_handler(lambda query: query.query=="/start")
def loh_query(query):
    hint = "Введи название трека вместо /start!"
    f='https://papik.pro/uploads/posts/2022-01/1643607217_48-papik-pro-p-muzikalnii-logotip-51.png'
    try:
        r = types.InlineQueryResultArticle(
                id='1',
                title="Начни пользоваться ботом!",
                description=hint,
                input_message_content=types.InputTextMessageContent(
                message_text="Эх, зря я не ввёл запрос :("),
                thumbnail_url=f,
                thumbnail_width=48,
                thumbnail_height=48
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)
cnt=20
def search_tracks(query):
    try:
        search_result = client.search(text=query)
        tracks=search_result.tracks.results
        resul = []
        for track in tracks[:min(len(tracks), cnt)]:  # Ограничиваем результаты до cnt
            buf=""
            for j in range(len(track.artists)):
                buf+=track.artists[j].name
                if j!=len(track.artists)-1:
                    buf+=' & '
            result = {
                'type': 'audio',
                'id': track.id,
                'title': track.title,
                'audio_url': track.get_download_info()[0].get_direct_link(),
                'audio_duration': track.duration_ms // 1000,
                'performer':buf,
                'cover_uri': track.cover_uri[:-2] + '200x200',
                'track_id': track.trackId,
                'lyrics':track.lyrics_available
            }
            resul.append(result)
        return resul
    except Exception as e:
        print(e)
@bot.inline_handler(lambda query: len(query.query) > 0 and query.query.find("/dbi")==-1 and query.query.find("/start")==-1 and query.query.find("/lyr")==-1)
def query_text(query):
    results = search_tracks(query.query)
    resu=[]
    try:
        for i in range(min(cnt, len(results))):
            mrkp = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("🎵Скачать",
                                              switch_inline_query_current_chat=f'/dbi {results[i]["track_id"]}')
            mrkp.row(btn1)
            if 1:
                btn2=types.InlineKeyboardButton("Текст песни",switch_inline_query_current_chat=f'/lyr {results[i]["track_id"]}')
                mrkp.row(btn2)
            single_msg = types.InlineQueryResultArticle(
                id=f"{i}", title=results[i]["title"],
                description=results[i]["performer"],
                input_message_content=types.InputTextMessageContent(
                    message_text=results[i]["performer"] + '  -  ' + results[i]["title"]),
                reply_markup=mrkp,
                thumbnail_url=results[i]["cover_uri"],
                thumbnail_height=60,
                thumbnail_width=60
            )
            resu.append(single_msg)
        bot.answer_inline_query(query.id, resu)
    except Exception as e:
        print(e)
@bot.inline_handler(lambda query: query.query.find("/dbi")!=-1)
def query_text(query):
    tex=query.query
    tex=tex[tex.find("/dbi")+5:]
    res=client.tracks(tex)
    res=res[0]
    single_msg = types.InlineQueryResultAudio(
        id="1", title=res.title,audio_url=res.get_download_info()[0].get_direct_link(),
        performer=res.artists[0].name)
    rs=[]
    rs.append(single_msg)
    bot.answer_inline_query(query.id,rs)
@bot.inline_handler(lambda query: query.query.find("/lyr")!=-1)
def query_text(query):
    tex=query.query
    tex=tex[tex.find("/lyr")+5:]
    fu = client.tracks(tex)
    fu = fu[0]
    buf = ""
    for j in range(len(fu.artists)):
        buf += fu.artists[j].name
        if j != len(fu.artists) - 1:
            buf += ' & '
    try:
        res = client.tracks_lyrics(tex)
        res = res.fetch_lyrics()
    except Exception as e:
        msg=types.InlineQueryResultArticle(id="1",title="Извините, на эту песню ещё нет текста :(",description="Попробуйте запросить позже",input_message_content=types.InputTextMessageContent(
                    message_text="Ой, произошла ошибка("))
        rs=[]
        rs.append(msg)
        bot.answer_inline_query(query.id,rs)
        return
    single_msg = types.InlineQueryResultArticle(
        id="1",title=fu.title,
                description=buf,
                input_message_content=types.InputTextMessageContent(
                    message_text="```\n"+buf + '  -  ' + fu.title +'\n'+res+"```",parse_mode="Markdown"),
                thumbnail_url=fu.cover_uri[:-2] + '200x200',
                thumbnail_height=60,
                thumbnail_width=60)
    rs=[]
    rs.append(single_msg)
    bot.answer_inline_query(query.id,rs)
@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    print(callback.data)
   # bot.send_audio(callback.message.chat.id,audio=callback.data)

while True:
        bot.polling(none_stop=True, timeout=18000)