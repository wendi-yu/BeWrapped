import argparse
import api
import process_photos

berealApi = api.BerealAPI()
splicer = process_photos.MemorySplicer()

parser = argparse.ArgumentParser()

parser.add_argument("--phone", "-p")
parser.add_argument("--token", "-t")
parser.add_argument("--start", "-s")
parser.add_argument("--end", "-e")

args = parser.parse_args()

token = args.token
if args.token is None:
    phone = args.phone
    token = berealApi.login(phone)
    print(token)

memories = berealApi.get_memfeed(token)[:365]
image_urls = [mem["secondary"]["url"] for mem in memories]
splicer.download_photos(image_urls)
splicer.create_video()



