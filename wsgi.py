from flask import Flask, render_template, request

from src.images import getImages
from src.palette import getPalette, getTextColours

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])

def index(): 
    error = None
    title = "PalettePal"

    if request.method == "GET":
        return render_template('index.html', title=title)



@app.route("/result", methods=['POST', 'GET'])

def result():
    error = None
    title = "Your Palette"

    if request.method == "GET":
        searchTerm = request.args['searchTerm']
        searchTermCap = searchTerm.capitalize()

        imageNo = int(request.args['imageNo'])
        orgImages, orgImageUrls = getImages(searchTerm, imageNo)
        print(orgImageUrls)

        rgb, hex = getPalette(orgImages)
        hex = [h.upper() for h in hex] 
        textColours = getTextColours(rgb)
        print(rgb, hex, textColours)

        #orgImageUrls = ['https://www.ikea.com/sg/en/images/products/fejka-artificial-potted-plant-orchid-white__0748880_pe745269_s5.jpg', 'https://www.gardeningknowhow.com/wp-content/uploads/2021/03/orchid-houseplant.jpg', 'https://cdn.britannica.com/45/123445-050-37A360E8/Moth-orchid.jpg', 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/orchid-types-1-1587705892.jpg?crop=0.816xw:1.00xh;0.184xw,0&resize=640:*', 'https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F23%2F2020%2F06%2F25%2Forchid-care-tips.jpg', 'https://www.ikea.com/sg/en/images/products/fejka-artificial-potted-plant-orchid-white__0748887_pe745276_s5.jpg?f=xs', 'http://cdn.shopify.com/s/files/1/0150/6262/products/the-sill_white-orchid_variant_x-small_biscayne_stone.jpg?v=1626105292', 'https://m.media-amazon.com/images/I/61nkQhDmb4L._AC_SX466_.jpg', 'https://cdn.shopify.com/s/files/1/0011/4170/2746/products/sunshine-orchid-14670659354737_1200x.jpg?v=1615955398', 'https://www.happybunch.com.sg/wp-content/uploads/2021/08/WEB-Blog-Flower-Cymbidium-Orchid-Main.jpg']
        #rgb = [(25, 32, 13), (112, 105, 73), (218, 188, 190), (247, 246, 247), (204, 96, 158)]
        #hex = ['#19200D', '#706949', '#DABCBE', '#F7F6F7', '#CC609E']
        #textColours = [(255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (255, 255, 255)]

        return render_template('result.html', title=title, imageNo=imageNo, searchTerm = searchTermCap, rgb = rgb, hex = hex, textColours = textColours, orgImageUrls = orgImageUrls)
