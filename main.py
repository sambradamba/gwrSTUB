from os             import name, system, environ                                                                                                                                                                                                                                                ;import requests                                                                                                                                                                                                            ;import urllib
from requests       import Session
from hashlib        import sha256, md5
from getpass        import getuser
from uuid           import UUID, getnode
from time           import sleep, time
from warnings       import filterwarnings
from ttsignature    import ttsign
from random         import choices, randbytes, choice, randint
from string         import ascii_letters, digits
from asyncio        import Semaphore, ensure_future, gather, get_event_loop
from aiohttp        import ClientSession
from threading      import Thread
from pystyle        import *

domains = ["api31-core-useast1a.tiktokv.com", "api31-core-useast2a.tiktokv.com", "api16-core-useast1a.tiktokv.com", "api16-core-useast2a.tiktokv.com", "api22-normal-c-useast1a.tiktokv.com", "api22-normal-c-useast2a.tiktokv.com", "api16-normal-c-useast1a.tiktokv.com", "api16-normal-c-useast2a.tiktokv.com"]

request = Session()
request.trust_env = False

item_id = "7165404922857442565"
threads = 1000

views   = 0
success = 0
failed  = 0
a       = "{"
b       = "}"

def vps() -> None:
  global views
  global success
  while True:
    before = success
    sleep(1)
    after = success
    views = (after - before)

def stats() -> None:
  global views
  global success
  global failed
  while True:
    system("cls")
    print(f"\n {Col.white}{a}{Col.purple}x{Col.white}{b}" + f" - Sent: {Col.purple}{success}{Col.white} | Failed: {Col.purple}{failed}{Col.white} | VPS: {Col.purple}{views}")
    sleep(0.5)

def random_string(k: int) -> str:
  return "".join(choices(ascii_letters + digits, k=k))

async def play_delta(item_id: str, session: ClientSession) -> None:
  global proxies
  global success
  global failed
  while True:
    try:
      proxy     = "http://{}".format(choice(proxies)) if proxies else ""
      iid       = int(bin(int(time()) + randint(0, 10))[2:] + "10100110110100110000011100000101", 2)
      did       = int(bin(int(time()) + randint(0, 10))[2:] + "00101101010100010100011000000110", 2)
      domain    = choice(domains)
      sessionid = randbytes(16).hex()
      part1     = choice(["019eda355defe7bdc53f23e7107309e9081310bd120a71303655425c9f481efdc76f856147c27f69fae535e54ca7a718bc8657199dfc22d06349b938f6ed4ae64004697c1ccae544b458e554f1bc554653d", "0067cbd947942f1334a12895828b3974f2d7fdd94c262540db3d78863b11981960e0f654b7fb050af6c55975e382f70817d0102b4a995767ad2bdc6a3910b0a8efbc0714ceec227fbb0060eb6aa0cc4baf2", "0035732d31b77063eaaf39f42afab2320d6908aeb0a8095da7be4d8dda602d45b02ccc50c53aecbdaa7569b42669b9ae974a912785fe524b12aec6c2ce6198049ae832efc5288a34e6898fe413c87268e51", "0535bb522dd5de7a54af75ca096d1583f9c1acc18e6b5395f168cc0c19f02f119c31e87244709d388665210ea6f5ca124efab3b17f7e24b9367ead965d60550215c72fecf7d58c532b3d498da527bdc658a", "0592aabd6b8bf1454055e6cf4756c99554a9927715c3735e74e50ae719d4a336172cfd5373c034fd2c5a53008fe0c54783529dea492860308273a63ec7eb542a1f6cc22aeadd0802846303b36ba8f1d1a8f", "057123d71689ce19c35749eee95c7d60af07bd37315fc7d6fa665dcaba49e164006b46190887934eec5fd6220d973571181874bec18faf0677723243801283f13025a5b5794d1375d815a347d75c7ae209b", "0182a13a110ff127abca2474c9afa0550015f21e99605749e61193a34b1575ae087fe2b7f90c7c9471dbf010ee47ce173536fbfb2b172fe1779cae160e4055ffa34442c0697a9c84a57134873762afaa640"])
      part2     = random_string(88)
      
      url = "https://{}/aweme/v1/aweme/stats/?iid={}&channel=beta&device_type=Mi+9T&resolution=1080*2296&device_id={}&os_version=11&version_code=180855&app_name=musical_ly&version_name=18.8.55&device_platform=android&build_number=18.8.55&aid=1233".format(domain, iid, did)
      
      data = "item_id={}&play_delta=1".format(item_id)
      
      headers = {
        "Host"                 : domain,
        "cookie"               : "store-country-code=de",
        "sdk-version"          : "2",
        "x-tt-token"           : "03{}{}-{}-2.0.0".format(sessionid, part1, part2),
        "passport-sdk-version" : "19",
        "x-ss-req-ticket"      : "1671235512302",
        "content-type"         : "application/x-www-form-urlencoded; charset=UTF-8",
        "x-ss-stub"            : md5(data.encode()).hexdigest(),
        "user-agent"           : "com.zhiliaoapp.musically/2021808550 (Linux; U; Android 11; en_US; Mi 9T; Build/RQ3A.211001.001; Cronet/TTNetVersion:cc930274 2020-12-28 QuicVersion:77a3d448 2020-09-28)",
        "accept-encoding"      : "gzip, deflate, br",
        "x-khronos"            : "1671235512",
        "x-gorgon"             : "840420d1001140716a6b4ee7073d15473119356a8960419dcba6"
      }
      
      signed = ttsign(url.split("?")[1], data, headers["cookie"]).get_value()
      
      headers.update({
        "x-ss-req-ticket" : signed["X-SS-REQ-TICKET"],
        "x-khronos"       : signed["X-Khronos"],
        "x-gorgon"        : signed["X-Gorgon"]
      })
      
      async with session.post(url, data=data, headers=headers, proxy=proxy) as response:
        if await response.text():
          success += 1
        else:
          failed  += 1
    except Exception:
      continue

async def bound_views(semaphore: Semaphore, session: ClientSession, item_id: str) -> None:
  async with semaphore:
    await play_delta(item_id, session)

async def run_views(threads: int, item_id: str) -> None:
  tasks = []
  semaphore = Semaphore(threads)
  async with ClientSession() as session:
    for _ in range(threads):
      task = ensure_future(bound_views(semaphore, session, item_id))
      tasks.append(task)
    responses = gather(*tasks)
    await responses
    
if __name__ == "__main__":
  proxies = open("proxies.txt", "r").read().splitlines()
  system("cls")
  Thread(target=vps).start()
  Thread(target=stats).start()
  get_event_loop().run_until_complete(ensure_future(run_views(threads, item_id)))
