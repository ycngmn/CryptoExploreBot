from bscscan import BscScan
import telepot,time,telepot.loop,pprint,requests,random,json,re
from telepot.namedtuple import InlineKeyboardButton,InlineKeyboardMarkup
from decimal import *


#vars
api = "" # Binance Api
token = "" # Bot token
btoken = "" # Blockcypher API token..
ethpl = "" # ETHPlorer API..
bot = telepot.Bot(token)
bsc = BscScan(api)
step = {}
textx = {}

keyx = [
	[InlineKeyboardButton(text="🔰 Generate ERC20 Balances ",callback_data='erc20')]
	]
key = InlineKeyboardMarkup(inline_keyboard=keyx)

def handle(msg):
	global step,textx,t,l
	pprint.pprint(msg)
	user = msg["from"]["id"]
	try:
		text = msg["text"]
	except KeyError:
		text = textx
	
	if ("data" in msg.keys()) and (user in step.keys()) and (user in textx.keys()):
		if msg["data"]=="erc20" and step[user]==2 :
			texty = textx[user].decode()
			rx = requests.get('https://api.ethplorer.io/getAddressInfo/'+texty+f'?apiKey={ethpl}')
			r = rx.json()
			t = ""
			try:
				l = r['tokens']
			except KeyError:
				bot.sendMessage(user,"No ERC tokens found in your address !")
				
			for xd in l:
				try:
					name = xd['tokenInfo']['name']
					balance = round(xd['balance']/10**18,4)
					if balance == 0.0:
						continue
					symbol = xd['tokenInfo']['symbol']
					address = xd['tokenInfo']['address']
				except KeyError:
					pass
				if len(name)>18:
					name = name[:18]+'...'
				else:
					pass
				link = f"<a href='https://etherscan.io/token/{address}'>⤻</a>"
				text = f"🔸 {name}{link}  —<code>{balance}</code> {symbol}"
				t += text+'\n'
				
			if len(t) <= 4000:
				bot.sendMessage(user,f'<b>✅ Your ERC-20 Tokens Balance :</b>\n\n{t}',parse_mode='HTML',disable_web_page_preview=True)
			else:
				st = t[:4000]
				nt = st.rfind('\n')
				ft = t[:nt]
				bot.sendMessage(user,f'<b>✅ Your ERC-20 Tokens Balance :</b>\n\n{ft}',parse_mode='HTML',disable_web_page_preview=True)
				bot.sendMessage(user,"It's nice you got too many tokens\nBut I can't load all 🤪 ")
				
	if text.startswith("/start"):
		bot.sendMessage(user,"Send any crypto address you like:") 
		
	elif text.startswith("0x") and len(text)==42:
		#ETH price
		eth = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
		dumpe = json.loads(eth.content)
		ethp = float(dumpe['price'].strip("0"))
		#bnb price 
		bnb = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT")
		dumpbn = json.loads(bnb.content)
		bnbp = float(dumpbn['price'].strip("0"))
		# Eth balance
		balanceReturn = requests.get('https://api.blockcypher.com/v1/eth/main/addrs/' + text + '/balance?token=' + btoken)
		if (balanceReturn.status_code == 400) or (balanceReturn.status_code == 404)or (balanceReturn.status_code == 429):
			bot.sendMessage(user,"Unknown error ooccured!\n Try re-checking the wallet address?"  )
		else:
			# bnb balance
			bnbbx = int(bsc.get_bnb_balance(address=text))/1000000000000000000
			bnbb = round(bnbbx,4)
			ethbx = float(Decimal(balanceReturn.json()["balance"]) / Decimal(1000000000000000000))
			ethb = round(ethbx,4) 
			
			ethu = round(ethbx*ethp,2)
			bnbu = round(bnbbx*bnbp,2)
			# Bot functions
			ethtext = f"🔥 <b>Your current ETH balance is :</b>\n\n—  <code>{ethb}</code> ETH <code>({ethu}$)</code>\n\n✅ <b>Your current BNB balance is :</b>\n\n— <code>{bnbb}</code> BNB <code>({bnbu}$)</code>"
			bot.sendMessage(user,ethtext,parse_mode="HTML",reply_markup=key) 
			step[user]=2
			textx[user] = text.encode()
	
	elif text.startswith(('1','3','bc1')) and 26<=len(text)<=42:
		# Btc price 
		btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
		dumpb = json.loads(btc.content)
		btcp = float(dumpb['price'].strip("0"))
		# BTC Balance
		balanceReturn = requests.get('https://api.blockcypher.com/v1/btc/main/addrs/' + text + '/balance?token=' + btoken)
		if (balanceReturn.status_code == 400) or (balanceReturn.status_code == 404)or (balanceReturn.status_code == 429):
			bot.sendMessage(user,"Couldn't load your wallet Balance.\nAre you Sure about this address ?")
		else:
			btcbx = float(Decimal(balanceReturn.json()["balance"]) / Decimal(100000000))
			btcb = round(btcbx,6)
			btcu = round(btcbx*btcp,2)
			btc_text = f"🔥 <b>Your current BTC balance is :</b>\n\n—  <code>{btcb}</code> ₿TC <code>({btcu}$)</code>"
			bot.sendMessage(user,btc_text,parse_mode='HTML')
			
	elif text.startswith(('L','M','l','m')) and 26<=len(text)<=43:
		ltc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT")
		dumpl = json.loads(ltc.content)
		ltcp = float(dumpl['price'].strip("0"))
		balanceReturn = requests.get('https://api.blockcypher.com/v1/ltc/main/addrs/' + text + '/balance?token=' + btoken)
		if (balanceReturn.status_code == 400) or (balanceReturn.status_code == 404)or (balanceReturn.status_code == 429):
			bot.sendMessage(user,"Couldn't load your wallet Balance.\nAre you Sure about this address ?")
		else:
			ltcbx = float(Decimal(balanceReturn.json()["balance"]) / Decimal(100000000))
			ltcb = round(ltcbx,4)
			ltcu = round(ltcbx*ltcp,2)
			ltc_text = f"🔥 <b>Your current LTC balance is :</b>\n\n—  <code>{ltcb}</code> LTC <code>({ltcu}$)</code>"
			bot.sendMessage(user,ltc_text,parse_mode='HTML')
			
	elif text.startswith("D") and len(text)==34:
		doge = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT")
		dumpd = json.loads(doge.content)
		dogep = float(dumpd['price'].strip("0"))
		balanceReturn = requests.get('https://api.blockcypher.com/v1/doge/main/addrs/' + text + '/balance?token=' + btoken)
		if (balanceReturn.status_code == 400) or (balanceReturn.status_code == 404)or (balanceReturn.status_code == 429):
			bot.sendMessage(user,"Am sure this isn't a valid address ..\nWhat do you think ?")
		else:
			dogebx = float(Decimal(balanceReturn.json()["balance"]) / Decimal(100000000))
			dogeb = round(dogebx,2)
			dogeu = round(dogebx*dogep,2)
			doge_text = f"🔥 <b>Your current DOGE balance is :</b>\n\n—  <code>{dogeb}</code> ÐOGE <code>({dogeu}$)</code>"
			bot.sendMessage(user,doge_text,parse_mode='HTML')
			
	elif text.startswith('X') and len(text)==34 :
		dash = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=DASHUSDT")
		dumpda = json.loads(dash.content)
		dashp = float(dumpda['price'].strip("0"))
		balanceReturn = requests.get('https://api.blockcypher.com/v1/dash/main/addrs/' + text + '/balance?token=' + btoken)
		if (balanceReturn.status_code == 400) or (balanceReturn.status_code == 404)or (balanceReturn.status_code == 429):
			bot.sendMessage(user,"Am sure this isn't a valid address ..\nWhat do you think ?")
		else:
			dashbx = float(Decimal(balanceReturn.json()["balance"]) / Decimal(100000000))
			dashb = round(dashbx,4)
			dashu = round(dashbx*dashp,2)
			dash_text = f"🔥 <b>Your current DASH balance is :</b>\n\n—  <code>{dashb}</code> DASH <code>({dashu}$)</code>"
			bot.sendMessage(user,dash_text,parse_mode='HTML')
			
	elif text.startswith("r") and 25<=len(text)<=35:
		xrp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
		xrpx = float(xrp['price'].strip("0"))
		xrpp = round(xrpx,2)
		re = requests.get('https://data.ripple.com/v2/accounts/'+text+'/balances?currency=XRP&method=balances')
		if re.status_code==200:
			r = float(re.json()['balances'][0]['value'])
			xrpb = round(r,3)
			xrpu = round(r*xrpp,2)
			dash_text = f"🔥 <b>Your current XRP balance is :</b>\n\n—  <code>{xrpb}</code> XRP <code>({xrpu}$)</code>"
			bot.sendMessage(user,dash_text,parse_mode='HTML')
		else:
			bot.sendMessage(user,"Couldn't load your wallet Balance.\nAre you Sure about this address ?")


telepot.loop.MessageLoop(bot,handle).run_as_thread()
while 1:
    time.sleep(40)
