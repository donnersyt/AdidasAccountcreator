# ADIDAS Account Creator v0.1
# Made by Donners
# https://github.com/donnersyt/AdidasAccountCreator

### Dependencies 
# Requests
# BS4
acceptedRegions = ["GB"]  # ,"US"

print("\n" * 20)
version = "v0.1"
print(version + str(" Adidas Account Creator"))
from datetime import datetime
import requests
import configparser
import random
import errno
import time

try:
    import bs4
except:
    import BeautifulSoup
import json
import os

if "nt" in os.name:
    windows = True
else:
    windows = False


def log(event):
    print(str(datetime.now().strftime("%H:%M:%S")) + str(" -- " + str(event)))


config = configparser.ConfigParser()
if windows:
    file = os.path.isfile("/config.cfg")
    path = "/config.cfg"
elif not windows:
    file = os.path.isfile("./config.cfg")
    path = "./config.cfg"
if not file:
    log("config.cfg not found!")
elif file:
    config.read(path)
    region = config.get("setup", 'region').upper()
    sleep = config.get("setup", "sleep")
    email = config.get("setup", "emailtouse")
    mailparse = email.split('@')
    mailprefix = mailparse[0]
    mailsuffix = mailparse[1]
    password = config.get("setup", "passwordtouse")
    firstName = config.get("setup", "firstname")
    lastName = config.get("setup", "lastname")
    if region not in acceptedRegions:
        log("Region " + str(region) + " is not currently supported :(")
        exit()
    print("Region = " + str(region))

def outputLogins(emailsused):
    outputdict = {}
    kount = 0
    for email in emailsused:
        outputdict[kount] = {"email":email, "password":password}
        kount += 1
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        os.open('accounts.json', flags)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

    with open('accounts.json',"w") as r:
        json.dump(outputdict, r, indent=2)
    print(json.dumps(outputdict,indent=2))


def gbrequestdata():
    postheaders = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, br",
	"Accept-Language":"en-GB,en-US;q=0.8,en;q=0.6",
	"Cache-Control":"no-cache",
	"Connection":"keep-alive",
	"Content-Type":"application/x-www-form-urlencoded",
	"Host":"cp.adidas.co.uk",
	"Origin":"https://cp.adidas.co.uk",
	"Pragma":"no-cache",
	"Referer":"https://cp.adidas.co.uk/web/eCom/en_GB/loadcreateaccount",
	"Upgrade-Insecure-Requests":"1",
	"Cookie":"""JSESSIONID=532ED571539337DDB4EE6EE6AE46AEA4; TS0180ed99=01b0ab2260afadd84144bf430a687c22c80d33f7674a6bd2f45b39999304258210dae935d4504d946ad8fd9059e1198c029ad9196e; us_criteo_sociomantic_split=criteo; __adi_rt_DkpyPh8=CTRLH2H; __CT_Data=gpv=5&apv_452_www06=5&cpv_452_www06=4; __troRUID=50dc89af-5bb8-43b6-b0ff-083a34c23785; BVBRANDID=15a80316-2ac5-477a-b999-d4c02fe5a3c2; RES_TRACKINGID=94190487356804948; __CT_Data=gpv=16&apv_452_www06=16&cpv_452_www06=14; __cq_bc=%7B%22aagl-adidas-GB%22%3A%5B%7B%22id%22%3A%22BB1234%22%2C%22sku%22%3A%22%22%2C%22type%22%3A%22%22%2C%22alt_id%22%3A%22%22%7D%2C%7B%22id%22%3A%22BA7519%22%2C%22sku%22%3A%22%22%2C%22type%22%3A%22%22%2C%22alt_id%22%3A%22%22%7D%2C%7B%22id%22%3A%22BY9143%22%2C%22sku%22%3A%22%22%2C%22type%22%3A%22%22%2C%22alt_id%22%3A%22%22%7D%2C%7B%22id%22%3A%22BB4677%22%2C%22sku%22%3A%22%22%2C%22type%22%3A%22%22%2C%22alt_id%22%3A%22%22%7D%2C%7B%22id%22%3A%224001985_W%22%2C%22sku%22%3A%22%22%2C%22type%22%3A%22%22%2C%22alt_id%22%3A%22%22%7D%2C%7B%22id%22%3A%22BA7748%22%2C%22sku%22%3A%22%22%7D%2C%7B%22id%22%3A%22BA9797%22%2C%22sku%22%3A%22%22%7D%2C%7B%22id%22%3A%22S79168%22%2C%22sku%22%3A%22%22%7D%2C%7B%22id%22%3A%22BA7326%22%2C%22sku%22%3A%22%22%7D%5D%7D; __troSYNC=1; lastVisitedProducts=BB1234%2CBA7519%2C4001985_W; AMCVS_7ADA401053CCF9130A490D4C%40AdobeOrg=1; AMCV_7ADA401053CCF9130A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C17194%7CMCMID%7C64096305499244714382035404502382216156%7CMCAAMLH-1485558075%7C6%7CMCAAMB-1486142270%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1485544670s%7CNONE%7CMCAID%7CNONE; notice_preferences=2:; BIGipServer~Prod~pf.adidas.com_8031_Upgrade=!gSCAhCBJJG3/CQcy7LzUXQLf8XEHqxterk0/95ymQHpvY6RTV/NNY2M5LH0LzyRCuaOUED/STAKQiPE=; SSOInfo=eCom|en_GB|cp.adidas.co.uk|null; PF=PYMD4PiwtMKPdGwrVJB50CHJKTo7OfvmqZJCtotaywyd; wishlist=%5B%5D; persistentBasketCount=0; userBasketCount=0; restoreBasketUrl=""; euci_persisted=PBMG660FSFWE18CC; pagecontext_customer_first_name=""; pagecontext_customer_last_name=""; pagecontext_logged_in=""; pagecontext_geo_country=GB; pagecontext_customer_id=abIupBjECSK16jooaWfugwWSg3; optimizelyEndUserId=oeu1484940863699r0.4651866922240868; LastPageUpdateTimestamp=1485539639906; onesite_language=en; onesite_country=GB; onesite_market=UK; s_sess=%5B%5BB%5D%5D; ResonanceSegment=1; RES_SESSIONID=13035403590863558; __cq_uuid=4acef570-da68-11e6-9ae6-7b2c3b37c248; __cq_seg=; s_cc=true; _ga=GA1.3.1308863951.1484940865; QSI_HistorySession=; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en_GB; utag_main=v_id:0159bd5f6ecf0000fcc79794d22305078005107000838$_sn:7$_ss:0$_st:1485541986718$_pn:32%3Bexp-session$ses_id:1485536809166%3Bexp-session; geo_country=GB; TS01556934=01b0ab2260230b33690f04837f02ffbc6edecc0d82987970964c2823bd9524112da2b9b768e02b02191ab2563c4f2f350d53982422727de061a8f6410d30132b3a7d9a99366ec584dc3a0f1cb4535fd4df32830bc2bdbfba6cf69c7ca6590dda2c469695a56a1838d68aa76dc609ae956e887dc5211a795f646f5a90a7d9f62cfc4a20ce23b94752a679574881ce8c1d4118c2a3dd2b5141c34ff86622ef475fc2a06bab35; ak_bmsc=EBC886F6A6091DE73691766AB836DB261743FF64815E0000267E8B589FA19B07~plXjstfruk7zvEWIRvDu930G2A11DPpkvzKDnt66KNVbvOL8QS94fym7E8Hug18X3/30hvvf1FP1SydgvfgeRqGzgCG0oEHiNvXU4Zd2vx/AKxpGHQGHpVXFUVl57oBkdfqpkMvw8HPoxSz6fcQGJWZ27+tnLuKBeAEPrqe2TE9WiXCiPaa1f2JjdU5qwbV5MDDgaSt0f5HbQSRP8fwCgD5CHTh32L5VqelKRhqlR2jZ4AHSOfXPQDL3VcCoFO2EfL; s_tps=383; s_pvs=434; s_pers=%20s_vnum%3D1485907200428%2526vn%253D5%7C1485907200428%3B%20pn%3D6%7C1488131640748%3B%20v56%3D%255B%255B%2527SITE%252520NAVIGATION%2527%252C%25271485539640762%2527%255D%255D%7C1643306040762%3B%20c4%3DACCOUNT%257CCREATE%2520PROFILE%7C1485542369162%3B%20s_visit%3D1%7C1485542369166%3B%20s_invisit%3Dtrue%7C1485542369170%3B; s_sq=ag-adi-global-prod%252Cag-adi-uk-prod%252Cag-adi-eu-prod%3D%2526pid%253DACCOUNT%25257CCREATE%252520PROFILE%2526pidt%253D1%2526oid%253Daccount.createaccount%2526oidt%253D3%2526ot%253DSUBMIT; RT="sl=1&ss=1485540073340&tt=2430&obo=0&sh=1485540187829%3D1%3A0%3A2430&dm=adidas.co.uk&si=dc50d603-59a9-416e-baa0-4bc1bf6721bb&bcn=%2F%2F364bf5fa.mpstat.us%2F&ld=1485540187829&nu=&cl=1485540569220'""",
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    }

    postdata = {
    "firstName":firstName,
	"lastName":lastName,
	"day":"1",
	"month":"1",
	"year":"1983",
	"password":str(password),
	"confirmPassword":str(password),
	"_amf":"on",
	"terms":"true",
	"_terms":"on",
	"metaAttrs[pageLoadedEarlier]":"true",
	"app":"eCom",
	"locale":"en_GB",
	"domain":"",
	"consentData1":"I would like to stay up to date with adidas",
	"consentData2":"I agree to receiving personalised marketing messages about adidas products, events and promotions (including offers and discounts). adidas may contact me through the channels I select, such as email, SMS or post. <b><u>What does this mean?</u></b>",
	"consentData3":"""We, <a target="_blank" href="https://www.adidas.co.uk/help-topics-imprint.html">adidas International Trading B.V.</a>, or third parties on our behalf, may contact you with messages about adidas products, events and promotions or to ask your opinions when we conduct research. In order to provide you with the best personalised experience and to anticipate which of our products and services you might be interested in, we will create a profile based on the information we hold about you. To create this profile, we will store and analyse the personal data we have collected about you, including:
	- your name, date of birth and e-mail address. We may also store your telephone number or postal address  if you choose to be contacted by post or SMS;
	- your preferences and interests that either you have actively shared with us through your adidas account or accounts or those that we have inferred through your registered interactions with adidas websites and apps (for which we may use cookies ); and
	- your shopping history, both online and offline.
	We will keep the profiles we create secure and we will not share them with any third parties other than those that we engage to provide services on our behalf. 
	You are in charge, meaning we may contact you only through the channels selected by you, such as email, telephone, apps, SMS or post. If you wish to unsubscribe or to opt out of a particular channel, please follow the steps contained in the particular message or contact <a target="_blank" href="https://www.adidas.co.uk/help">Customer Service</a>. For more information, including on how to exercise your rights in relation to the personal data we hold about you, please read our <a target="_blank" href="https://www.adidas.co.uk/help-topics-privacy_policy.html">Privacy Statement</a>.""",
        }
    return postheaders, postdata


def setUrl():
    if region == "GB":
        domain = "co.uk"
        lang = "en_GB"
    elif region == "US":
        domain = "com"
        lang = "en_US"
    CSRFurl = "https://cp.adidas.{}/web/eCom/{}/loadcreateaccount".format(domain, lang)
    POSTurl = "https://cp.adidas.{}/web/eCom/{}/accountcreate".format(domain, lang)
    return CSRFurl, POSTurl


def runCreation():
    if region == "GB":
        datatouse = gbrequestdata()
    else:
        a = 0
    # US and other regions -  datatouse = otherrequestdata()
    postheaders = datatouse[0]
    postdata = datatouse[1]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    }
    if region == "GB":
        postdata["CSRFToken"] = "ba1ad256-e406-4ac6-a8f4-71878e6f1bfc"
    elif region == "US":
        postdata["CSRFToken"] = "4bb87e73-7f53-40a0-b050-bc694382c4cc"
    intused = []
    emailsused = []
    for i in range(numberOfAccounts):
        session = requests.session()
        randomint = random.randint(1, 999)
        randomint = randomint ** 2
        while randomint in intused:
            randomint = random.randint(1, 999)
            randomint = randomint ** 2
        intused.append(randomint)
        mailpre = mailprefix + str(randomint)
        email = mailpre + "@" + mailsuffix
        postdata["email"] = email
        create = session.post(url[1], headers=postheaders, data=postdata)
        emailsused.append(email)
        time.sleep(int(sleep))

    return emailsused


if __name__ == "__main__":
    numberOfAccounts = 10
    """
	numberOfAccounts = int(input("Please Enter the total number of accounts to make: "))
	if numberOfAccounts >= 200:
		log("You can not make more than 200 accounts as of now.")
	"""
    url = setUrl()
    emailsused = runCreation()
    outputLogins(emailsused)
