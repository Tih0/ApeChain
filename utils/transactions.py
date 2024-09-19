import random
import time
from utils.client import Client, TokenAmount
from web3.exceptions import TransactionNotFound
import asyncio, string
class Transactions:
    def __init__(self, client: Client):
        self.client = client

    async def txYourself(self,  k, delay_min, delay_max, start_delay_min, start_delay_max, retry = 0):
        if k != 0 and k != -1:
            delay = random.randint(delay_min, delay_max)
            print(f'Delay: {delay}')
            await asyncio.sleep(delay)

        elif k == 0:
            delay = random.randint(start_delay_min, start_delay_max)
            print(f'Start delay:{delay}')
            await asyncio.sleep(delay)

        print(f'{self.client.address} | txYourself')
        try:
            tx = self.client.send_transaction(
                to=self.client.address,
                value= self.client.w3.eth.get_balance(self.client.address) - (random.randint(1, 3) * 10**17)
            )
            await asyncio.sleep(5)
            verify = self.client.verif_tx(tx)
            if verify == False:
                retry += 1
                if retry < 5:
                    print(f"{self.client.address} | Error. Try one more time {retry} / 5")
                    print('Time sleep 20 seconds')
                    await asyncio.sleep(20)
                    k = -1
                    await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
                else:
                    print(f"ERROR txYourself")
                    return 0

        except TransactionNotFound:
            print(f'{self.client.address} | The transaction has not been remembered for a long period of time, trying again')
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)

        except ConnectionError:
            print(f'{self.client.address} | Internet connection error or problems with the RPC')
            await asyncio.sleep(120)
            print('Time sleep 120 seconds')
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)

        except Exception as error:
            print(f"{self.client.address} | Unknown Error:  {error}")
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.txYourself(k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)


    async def bridge(self, amount: TokenAmount, k, delay_min, delay_max, start_delay_min, start_delay_max, retry = 0):
        if k != 0 and k != -1:
            delay = random.randint(delay_min, delay_max)
            print(f'Delay: {delay}')
            await asyncio.sleep(delay)

        elif k == 0:
            delay = random.randint(start_delay_min, start_delay_max)
            print(f'Start delay:{delay}')
            await asyncio.sleep(delay)

        print(f'{self.client.address} | Bridge to Arbitrum Sepolia')
        contract_address = '0x0000000000000000000000000000000000000064'
        try:
            tx = self.client.send_transaction(
                to=contract_address,
                value=amount.Wei,
                data=f'0x25e16063000000000000000000000000{self.client.address[2:]}',
            )
            await asyncio.sleep(5)
            verify = self.client.verif_tx(tx)
            if verify == False:
                retry += 1
                if retry < 5:
                    print(f"{self.client.address} | Error. Try one more time {retry} / 5")
                    print('Time sleep 20 seconds')
                    await asyncio.sleep(20)
                    k = -1
                    await self.bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
                else:
                    print(f"{self.client.address} | ERROR Bridge")
                    return 0

        except TransactionNotFound:
            print(f'{self.client.address} | The transaction has not been remembered for a long period of time, trying again')
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
        except ConnectionError:
            print(f'{self.client.address} | Internet connection error or problems with the RPC')
            await asyncio.sleep(120)
            print('Time sleep 120 seconds')
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)
        except Exception as error:
            print(f"{self.client.address} | Unknown Error:  {error}")
            print('Time sleep 120 seconds')
            await asyncio.sleep(120)
            retry += 1
            if retry > 5:
                return 0
            k = -1
            await self.bridge(amount, k, delay_min, delay_max, start_delay_min, start_delay_max, retry=retry)

