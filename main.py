from dotenv import load_dotenv
import os
import telebot
import yfinance as yf

load_dotenv()

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["start"])
def handle_start(message):
  bot.send_message(message.chat.id, """\
Halo, gua joyboy.
command yang tersedia:
/wsb = untuk mendapatkan informasi harga saham TESLA, APPLE, DAN META dalam 1 bulan terakhir
/joyboy = untuk blablabalablabalabalabalabalabalbla
price (name of stock you wanna check) = it'll give you information of a certain stock
""")
  
  
@bot.message_handler(commands=["wsb"])
def get_stock(message):
  response = ""
  stocks = ["TSLA", "AAPL", "META"]
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period="1mo")
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ["stock"]
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row["Close"], 2)
      format_date = row["Date"].strftime("%d/%m")
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  bot.send_message(message.chat.id, response)
  
  
@bot.message_handler(commands=["joyboy"])
def handle_joyboy(message):
  bot.send_message(message.chat.id, "blablabalablabalabalabalabalabalbla")
  

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True
  
@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period="1d")
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data["Date"].dt.strftime("%d/%m %I:%M %p")
    data.set_index("format_date", inplace=True)
    bot.send_message(message.chat.id, data["Close"].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data?!")


bot.polling(none_stop=True, interval=0)