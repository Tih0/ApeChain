import asyncio, random
from utils.networks import Curtis
from utils.getBalance import getBalance, getBalanceForOne
from utils.client import Client, TokenAmount
from utils.transactions import Transactions
from config import mode, delay_min, delay_max, start_delay_max, start_delay_min, group_accounts, shuffle
from datetime import datetime, timezone, timedelta
from utils.tg import send_number, send_delay

address = []
clients = []
transactions = []
proxy = []
with open('proxy.txt') as f:
    proxy = f.readlines()

with open('addresses.txt') as f:
    address = f.readlines()


for i in range(len(address)):
    clients.append(Client(address[i].strip(), Curtis, proxy[i].strip()))
    transactions.append(Transactions(client=clients[i]))

count = len(address)
numbers = list(range(count))
if shuffle == True:
    random.shuffle(numbers)

async def main():
    k = 0
    if mode == 'Balance':
        getBalance(client_list=clients, num_clients=len(clients))
        return 0

    elif mode == 'TxYourself':
        b = 0
        while True:
            if b != 0:
                now = datetime.now(timezone.utc) + timedelta(hours=2)
                target_hour = random.randint(4, 15)
                target_time = datetime(now.year, now.month, now.day, target_hour, 0, 0, tzinfo=timezone.utc) - timedelta(
                    hours=2)
                if now >= target_time:
                    target_time += timedelta(days=1)
                delay_seconds = (target_time - now).total_seconds()
                print(f' Next run at: {target_time} (UTC+2)')
                send_delay(f'⏰🐵 Next run at: {target_time} (UTC+2)')
                await asyncio.sleep(delay_seconds)
                send_delay(f'🚀🐵 Start transactions of group: {group_accounts}..')
            mas_counter = [0] * len(address)
            current_count = 0
            while current_count <= max(mas_counter):
                tasks = []
                for i in range(len(address)):
                    if current_count == 0:
                        mas_counter[i] = random.randint(1, 4)
                    if current_count != mas_counter[i]:
                        tasks.append(
                            transactions[i].txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max))
                await asyncio.gather(*tasks)
                current_count += 1
                k += 1
                print(f'Current Circle: {current_count}')
            b+=1

    elif mode == 'Bridge':
        while True:
            send_delay(f'🚀🐵 Start Bridge ApeChain of group: {group_accounts}..')
            for i in numbers:
                amount = TokenAmount((random.randint(1,3) * (10 ** 17)), wei=True)
                await transactions[i].bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max)

            k += 1

    elif mode == 'DayMode':
        while True:

            for i in numbers:
                tasks = []
                amount = TokenAmount((random.randint(1, 3) * (10 ** 17)), wei=True)
                choice = random.randint(1,2)
                if choice == 1:
                    tasks.append(transactions[i].bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max))
                for j in range(random.randint(1,3)):
                    tasks.append(transactions[i].txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max))
                else:
                    tasks.append(transactions[i].bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max))
                await asyncio.gather(*tasks)
            k += 1

asyncio.run(main())
