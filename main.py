from fastapi import FastAPI
import requests
import json
app = FastAPI()
infoFile = open('info.txt', 'w')

def searchQuery(productParams,page,withPages):
    if withPages:
        url = f"https://stockx.com/api/browse?_search={productParams}&page={page}"
    url = f"https://stockx.com/api/browse?_search={productParams}"
    headers={
        'accept': 'application/json',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-GB,en;q=0.9',
        'app-platform': 'Iron',
        'app-version': '2022.08.14.05',
        'referer': 'https://stockx.com/en-gb',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    productHtmlPage = requests.get(url = url, headers =headers) 
    return productHtmlPage


def checkLastPageAmount(productParams):
    pageAmount = 0
    pageAmountJSON = json.dumps(searchQuery(productParams,1,False).json())
    productAmountData = json.loads(pageAmountJSON)
    lastPageInformation = productAmountData['Pagination']['lastPage']
    lastPageInformation = lastPageInformation.split('&')
    for keyword in lastPageInformation:
        if 'page' in keyword:
            pageAmount = keyword.split('page=')
    return int(pageAmount[1])


def jsonFileFormatter(jsonFile):
    return json.dumps(jsonFile)

def loadAllProductJson(productParams):
    products = []
    for i in range(checkLastPageAmount(productParams) - 1):
        productJson = jsonFileFormatter(searchQuery(productParams, i, True).json())
        for product in json.loads(productJson)['Products']:
            products.append(product)
    return products


# Method to only return first product
def scrapeProductInformation(productParams):
    productJson = json.dumps(searchQuery(productParams, 1, True).json())
    productData = json.loads(productJson)
    productInfo = productData['Products'][0] 
    return productInfo

def writeInfoOnTxt(productParams):
    for product in loadAllProductJson(productParams):
        productSeperator = "------------------------------------" + '\n'
        productTitle = product['title']
        productHasAsks = product['market']['hasAsks']
        productLowestAsk = f"{product['market']['lowestAsk']} & lowest ask size: {product['market']['lowestAskSize']}"
        lastSale = f"{product['market']['lastSale']} & last sale size: {product['market']['lastSaleSize']}"

        infoFile.write(productSeperator)
        infoFile.write(productTitle) 
        infoFile.write(str(productHasAsks))
        infoFile.write(productLowestAsk)
        infoFile.write(lastSale) 
        infoFile.write(productSeperator)

scrapeProductInformation("dunk")