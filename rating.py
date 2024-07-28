from pyppeteer import launch
import config
import asyncio
import google.generativeai as genai
import os
import random
from fake_useragent import UserAgent


os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_TRACE'] = ''
api_key = os.getenv(config.API_KEY)
genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

name = input( "\n" + "Please enter the name of your professor: ")
async def urlBuilder(name):
    ua = UserAgent()
    user_agent = ua.random
    
    curr = "https://www.ratemyprofessors.com/search/professors/1255?q=" + name
    names = []  
    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})
    check = True
    page = await browser.newPage()
    #await page.setUserAgent(user_agent)
    await page.setViewport({"width":800, "height":3200})
    await page.goto(curr, timeout=120000)
    try:
        await page.waitForSelector(".dLJIlx", timeout=5000)
    except:
        await browser.close()
        return "timeout"
    
    profNames = await page.querySelectorAll(".dLJIlx")
    if profNames:
        for profs in profNames:
            await page.waitForSelector(".cJdVEK")
            snippet = await profs.querySelector(".cJdVEK")
            text = await page.evaluate("selected => selected.textContent", snippet)
            if text.lower() == name.lower():
                href = await page.evaluate('(link) => link.href', profs)
                await browser.close()
                return href

        await browser.close()
        return "timeout"
    else:
        await browser.close()
        return "timeout"

asyncio.get_event_loop().run_until_complete(urlBuilder(name))


async def scrape_reviews(url):
    ua = UserAgent()
    user_agent = ua.random
    if url == "timeout":
        return "timeout"
    print( "\n" + "Your professor has been found, comprehensive review is being generated..." + "\n")
    revs = []  
    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})
    check = True
    page = await browser.newPage()
    #await page.setUserAgent(user_agent)
    await page.setViewport({"width":800, "height":3200})
    await page.goto(url, timeout=120000)

    while check:
        try:
            await page.waitForSelector(".glImpo")
            more = await page.querySelector(".glImpo")
            if more is None:
                check = False
            await page.evaluate("button => button.click()", more)
            await page.waitFor(500)
        except:
            pass
            break

    await page.waitForSelector('.jcIQzP')
    comments = await page.querySelectorAll('.jcIQzP')
    for comms in comments:
        await page.waitForSelector(".gRjWel")
        snippet = await comms.querySelector(".gRjWel")
        text = await page.evaluate("selected => selected.textContent", snippet)
        revs.append(text)
    await browser.close()
    print("Almost done...")
    return revs
    
def summary(reviews, model):
    if reviews == "timeout":
        print("This professor does not exist at this university.")
    else:    
        prompt = "I am a college student looking for a good professor: based on the reviews given give me all the necessary details/pros and cons as well as a rating out of 10:"
        for rev in reviews:
            prompt += "\n" + rev
        response = model.generate_content(prompt)
        print("\n" + response.text)

reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(asyncio.get_event_loop().run_until_complete(urlBuilder(name))))
summary(reviews, model)