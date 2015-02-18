__author__ = 'vantani'
from bs4 import BeautifulSoup
import requests
def mobile_brands():
    found = mc.get('all_mobile_brands')

    if (found!=None):
        return found
    else:
        #execute raw SQL on PostgreSQL similarity
        sql_raw="SELECT name, img, top_brand from mobile_brands order by top_brand desc"
        sql = text(sql_raw)
        result = db.engine.execute(sql)
        brands=[]
        for row in result:
            if row:
                brand = {"name":row[0],"img":row[1], "top_brand":row[2]}
                brands.append(brand)

        mc.set('all_mobile_brands',brands)
        return brands

def mobile_models_from_brand(brand):
    found = mc.get('mobile_models_from_brand_{0}'.format(brand))

    if (found!=None):
        return found
    else:
        #execute raw SQL on PostgreSQL similarity
        sql_raw="SELECT name,img,top_mobile FROM mobile_models where maker = '{0}'".format(brand)
        sql = text(sql_raw)
        result = db.engine.execute(sql)
        brands=[]
        for row in result:
            if row:
                brand = {"name":row[0],"img":row[1], "top_mobile":row[2]}
                brands.append(brand)

        mc.set('mobile_models_from_brand_{0}'.format(brand),brands)
        return brands

def flipkart_best_selling_mobiles():
    url="http://www.flipkart.com/mobiles-accessories/~bestsellers/pr?sid=tyy"
    title_expr="div.pu-details.lastUnit div.pu-title.fk-font-13 a.fk-display-block"
    price_expr="div.pu-details.lastUnit div.pu-price div.pu-border-top div.pu-final span.fk-font-17.fk-bold"
    img_expr="div.product-unit.unit-4.browse-product div.pu-visual-section a.pu-image.fk-product-thumb img"

    found = mc.get('flipkart_best_selling_mobiles')

    if (found!=None):
        return found
    else:
        response=requests.get(url)
        soup=BeautifulSoup(response.content, 'lxml')
        items=[]
        titles=soup.select(title_expr)
        prices=soup.select(price_expr)
        imgs=soup.select(img_expr)

        for title, price, img in zip(titles, prices, imgs):
            img_src = img.get('data-src')
            if img_src is None:
                img_src=img.get('src')

            item={'title':title.text, 'price':price.text, 'img':img_src}
            items.append(item)
            print item
        mc.set('flipkart_best_selling_mobiles',items,time=84000)
        return items

def get_gsmarena_spec(title):

    #execute raw SQL on PostgreSQL similarity
    sql_raw="SELECT name, canonical_name, description, img, fields, similarity(name, '{0}') AS sml FROM mobile_models WHERE name % '{0}' ORDER BY sml DESC, name;".format(title)
    sql = text(sql_raw)
    result = db.engine.execute(sql)
    count=0
    mobile_models=[]
    row=[]
    for row in result:
        if count==0:
           break;
    if row:
        mobile_name = row[0]
        mobile_canonical_name = row[1]
        mobile_description = row[2]
        mobile_img = row[3]
        fields = row[4]
        flattened_field=''

        if fields:
            #mobile_obj=json.dumps(fields)
            mobile_obj=fields
            for key, value in mobile_obj.items():
                #Not a great idea to embed HTML in the payload but there is no other way
                flattened_field = flattened_field +'<table cellspacing="0"><tbody><tr><th scope="row" rowspan="'+str(len(mobile_obj))+'">'+ key + "</th>"
                for subkey, subvalue in value.items():
                    flattened_field = flattened_field + '<td class="ttl">' + subkey + '</td><td class="nfo">' + subvalue + "</td></tr>"
                flattened_field = flattened_field + "</tbody></table>"

        print mobile_name, mobile_canonical_name, mobile_description, mobile_img, flattened_field
        mobile_models.append({"name":mobile_name, "canonical_name":mobile_canonical_name, "description":mobile_description,
                              "img":mobile_img,"fields":flattened_field})
        return mobile_models
    else:
        return []

def get_gsmarena_link(name,url):

    found = mc.get('gsmarena_review_'+str(hashlib.md5(url).hexdigest()))
    ttl_expr="td.ttl a"
    nfo_expr="td.nfo"

    if (found!=None):
        return found
    else:
        response=requests.get(url)
        soup=BeautifulSoup(response.content, 'lxml')
        items=[]
        titles=soup.select(ttl_expr)
        info=soup.select(nfo_expr)
        for title,info in zip(titles,info):
            item={'title':title.text, 'info':info.text}
            items.append(item)

        mc.set('gsmarena_review_'+str(hashlib.md5(url).hexdigest()),items)
        return items