class LoInFunc(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'demos/log_in_func.html')
    def post(self, request, *args, **kwargs):   
        loc = request.POST.get("loc", False)
        os = request.POST.get("os", False)
        brow = request.POST.get("brow", False)
        dev = request.POST.get("dev", False)
        time_d = request.POST.get("time", False)
        # drug_category_name = request.POST.get("drug_category_name", False)
        print("loc")
        print(loc)
        print("os")
        print(os)
        print("brow")
        print(brow)
        print("dev")
        print(dev)
        print("time_d")
        print(time_d)
        dd = datetime.now()
        time = dd.strftime("%d:%m:%Y,%H:%M:%S")
        # url = "https://100003.pythonanywhere.com/event_creation"
        username = "dowellFeedback"
        password = "DOWELL@qrcode2022"
        otp="opt"
        ip="192.168.0.41"
        conn="random"
        #  ["otp","loc",dev,"os","brow","time","ip","conn","username","password"]
        url="https://100014.pythonanywhere.com/api/login/"
        userurl="http://100014.pythonanywhere.com/api/user/"
        payload = {"otp": otp, "loc": loc, "dev": dev,
            "os": os, "brow": brow,"time":time,
            "ip": ip, "conn": conn,"username":username, 
            "password": password
            }

        # r = requests.post(url, json=data)
        # print("=============================Login respomsze======================")
        # print(r.text)
        with requests.Session() as s:
            p=s.post(url, data=payload)
            if "Username" in p.text:
                print("p.text")
                print(p.text)
                return p.text
            else:
                user=s.get(userurl)
                print("user.text")
                print(user.text)
                return user.text
        # return r.text








###Add  and update continents to Local Db
    # print("Africa twp re")
    # print(re)
    # eventId_rectifier()
    # locDowellMasterDf = pd.read_csv(BASE_DIR / 'city_master.csv')
    # locContinentMatcher =  pd.read_csv(BASE_DIR / 'continent_match.csv')
    # locCountryCodes =  pd.read_csv(BASE_DIR / 'country_codes.csv')
    # print("locDowellMasterDf")
    # print(locDowellMasterDf.columns)
    # print(locDowellMasterDf.head())
    # print("locContinentMatcher")
    # print(locContinentMatcher.columns)
    # print(locContinentMatcher.head())
    # continent_list = locContinentMatcher['continent'].to_list()
    # country_list_dowell = locDowellMasterDf['Country'].to_list()
    # country_list_matcher = locContinentMatcher['country'].to_list()
    # country_codes_list = locCountryCodes['country'].to_list()

    # print("country_codes_list")
    # print(set(country_codes_list))
    # absentDf_coed = set(country_list_dowell).difference(set(country_codes_list)) 
    # print("country_list absentDf_coed")
    # print(absentDf_coed)
    # print("country_list dowell set")
    # print(set(country_list_dowell))
    # print("country_list match set")
    # print(set(country_list_matcher))
    # absentDf = set(country_list_dowell).difference(set(country_list_matcher)) 
    # print("country_list absent in master")
    # print(absentDf)
    
    # absent_soln = {'Srilanka':'Sri Lanka','England':'United Kingdom of Great Britain and Northern Ireland','Czech Republic':'Czechia','Vietnam':'Viet Nam','UAE':'United Arab Emirates','South Korea':"Democratic People's Republic of Korea",'San Francisco':'United States of America'}
    # absent_soln_codes = {'Srilanka':'Sri Lanka','England':'United Kingdom','UAE':'United Arab Emirates','San Francisco':'United States', 'United States of America':'United States'}

    # absent_soln = {'Srilanka':'Asia','England':'Europe','Czech Republic':'Europe','Vietnam':'Asia','UAE':'Asia','South Korea':'Asia','San Francisco':'North America'}
    # continentsMongoIds = {"Asia": "62bc10cd64ec6bd2250a8a10",  "Europe": "62bc117d64ec6bd2250a8a1a",  "Antarctica": "62bc118264ec6bd2250a8a1e",  "South America": "62bc118864ec6bd2250a8a22",  "Oceania": "62bc118d64ec6bd2250a8a26",  "Africa": "62bc1193c77438eb140a8981",  "North America": "62bc119964ec6bd2250a8a2a"}
    # {"isSuccess": false, "error": "document must be an instance of dict, bson.son.SON, bson.raw_bson.RawBSONDocument, or a type that inherits from collections.MutableMapping"}
    # {"isSuccess": true, "inserted_id": "62bc0ea864ec6bd2250a8a06"}
    # Continent: Asia --> insert Id: 62bc10cd64ec6bd2250a8a10
# Continent: Europe --> insert Id: 62bc117d64ec6bd2250a8a1a
# Continent: Antarctica --> insert Id: 62bc118264ec6bd2250a8a1e
# Continent: South America --> insert Id: 62bc118864ec6bd2250a8a22
# Continent: Oceania --> insert Id: 62bc118d64ec6bd2250a8a26
# Continent: Africa --> insert Id: 62bc1193c77438eb140a8981
# Continent: North America --> insert Id: 62bc119964ec6bd2250a8a2a
### Add Continents to Mongo Db
    # for continent in set(continent_list):
    #     if continent != 'Asia':
    #         result = mongo_create('continent',{"name":str(continent)})
    #         if result["isSuccess"]:
    #             print("Continent: "+str(continent)+" --> insert Id: "+str(result["inserted_id"]))
    #         else:
    #             print("Continent: "+str(continent)+" --> error : "+str(result["error"]))
###Add  and update continents to Local Db
    # for c in continentsMongoIds:
        
    #     # cont = Continent(name = c,  mongo_id = continentsMongoIds[c])
    #     event_id = ""
    #     if continentsMongoIds[c] == '62bc119964ec6bd2250a8a2a':
    #         print("Hit the continenc 62bc119964ec6bd2250a8a2a if statement ")
    #         event_id = 'FB1010000000165657602259221966'
    #     else:
    #         event_id = get_event_id()
    #     print("For continent : "+c+" ---> event id ="+str(event_id))
    #     print(event_id)
    #     # data_u = {
    #     #     "event_id":'FB1010000000165657602259221966'
    #     # }
    #     data_u = {
    #         "event_id":event_id
    #     }
    # # FB1010000000165657602259221966
    #     re = mongo_update('continent',continentsMongoIds[c], data_u)
    #     print("rererererer")
    #     print(re)
    #     if re["isSuccess"]:
    #         print("Continent: "+str(c)+" --> insert Id: ")
    #         cont = Continent.objects.get(mongo_id=continentsMongoIds[c])
    #         cont.event_id = event_id
    #         cont.save()
    #     else:
    #         print("Continent: "+str(c)+" --> error : "+str(re["error"]))
    # countries  = Countries.objects.all()
    # for c in countries:
    #     print("Country name")
    #     print(c.name)
    #     # event_id = get_event_id()
    #     # event_id = "o"
    #     edit_name = c.name+"_Error"
    #     print("For continent : "+c.name+" ---> event id ="+str(edit_name))
    #     print(c.name+"Error")
    #     # data_u = {
    #     #     "event_id":'FB1010000000165657602259221966'
    #     # }
    #     data_u = {
    #         # "event_id":event_id,
    #         "name":edit_name
    #     }
        
    #     re = mongo_update('country',c.mongo_id, data_u)
    #     print("rererererer")
    #     print(re)
    #     if re["isSuccess"]:
    #         print("Continent: "+str(c.name)+" --> insert name: "+str(edit_name))
    #         c.name = edit_name
    #         c.save()
    #     else:
    #         print("Continent: "+str(c.name)+" --> error : "+str(re["error"]))

    # for c in continentsMongoIds:
        
    #     # cont = Continent(name = c,  mongo_id = continentsMongoIds[c])
    #     event_id = ""
    #     if continentsMongoIds[c] == '62bc119964ec6bd2250a8a2a':
    #         print("Hit the continenc 62bc119964ec6bd2250a8a2a if statement ")
    #         event_id = 'FB1010000000165657602259221966'
    #     else:
    #         event_id = get_event_id()
    #     print("For continent : "+c+" ---> event id ="+str(event_id))
    #     print(event_id)
    #     # data_u = {
    #     #     "event_id":'FB1010000000165657602259221966'
    #     # }
    #     data_u = {
    #         "event_id":event_id
    #     }
    # # FB1010000000165657602259221966
    #     re = mongo_update('continent',continentsMongoIds[c], data_u)
    #     print("rererererer")
    #     print(re)
    #     if re["isSuccess"]:
    #         print("Continent: "+str(c)+" --> insert Id: ")
    #         cont = Continent.objects.get(mongo_id=continentsMongoIds[c])
    #         cont.event_id = event_id
    #         cont.save()
    #     else:
    #         print("Continent: "+str(c)+" --> error : "+str(re["error"]))
        
        
## Add countries to Mongo
    # temp_dict = {"ggg":"hdhdhd","hhhh":"jdjdj","gsgsg":"jsjsjs","gsfsffs":"sgcvvv"}
    # result = mongo_create("country", temp_dict)
    # if result["isSuccess"]:
    #     print("Continent: "+str("temp_name")+" --> insert Id: "+str(result["inserted_id"]))
    # else:
    #     print("Continent: "+str("temp_name")+" --> error : "+str(result["error"]))

    # re = mongo_read("continent", "62bc119964ec6bd2250a8a2a")
    
    # count = 0
    # for country in set(country_list_dowell):
    #     temp_continent = ""
    #     temp_name = country
    #     temp_country_code = ""
    #     temp_country_short = ""
    #     temp_mongo_id =""
    #     event_id = get_event_id()
    #     print("Count "+str(count)+" for "+temp_name+" in Subject")
    #     if len(event_id) > 40:
    #         print("Greater than 40")
    #         print(event_id)
    #         raise Exception("Error in Created Event Id ")

    #     if country in country_list_matcher:
    #         print('Preseint in matcher')
    #         temp_continent =list(locContinentMatcher.loc[locContinentMatcher['country']==country]['continent'].values)[0]
    #         temp_country_short = list(locContinentMatcher.loc[locContinentMatcher['country']==country]['country_short'].values)[0]
            
    #     else:
    #         print('Absent in matcher------------------------------------------------------------------------------------------------------------------------------------------------')

    #         temp_continent =list(locContinentMatcher.loc[locContinentMatcher['country']==absent_soln[country]]['continent'].values)[0]
    #         temp_country_short = list(locContinentMatcher.loc[locContinentMatcher['country']==absent_soln[country]]['country_short'].values)[0]
            
    #     if country in country_codes_list:
    #         print('Preseint in country codes')

    #         temp_country_code = list(locCountryCodes.loc[locCountryCodes['country']==country]['country_code'].values)[0]

    #     else:
    #         print('Absent  in Country codes++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    #         temp_country_code = list(locCountryCodes.loc[locCountryCodes['country']==absent_soln_codes[country]]['country_code'].values)[0]

        
    #     temp_dict = {"continent":continentsMongoIds[temp_continent],"name":temp_name,"country_code":temp_country_code,"country_short":temp_country_short, "event_id":event_id}
    #     print("Temps dict DO")
    #     print(temp_dict)
    #     count+=1
    #     result = mongo_create("country", temp_dict)
    #     if result["isSuccess"]:
    #         print("Continent: "+str(temp_name)+" --> insert Id: "+str(result["inserted_id"]))
    #         temp_mongo_id= result["inserted_id"]
    #         continent = Continent.objects.get(name = temp_continent)
    #         country = Countries(continent = continent,name = temp_name,  mongo_id = temp_mongo_id,
    #          country_code= temp_country_code, country_short = temp_country_short, event_id= event_id)
    #         country.save()
    #     else:
    #         print("Continent: "+str(temp_name)+" --> error : "+str(result["error"]))
    #         raise Exception("Error occured in mongo insertion for "+str(temp_name))



# country
# name
# lat_lon
# city_code
# city_area
# mongo_id
# event_id
###### Insert City
    # print("locDowellMasterDf 'Area of city in sq km' is null")
    # print(locDowellMasterDf['Area of city in sq km'].isnull().sum())
    # for index, row in locDowellMasterDf.iterrows():
    #     temp_country_name = row['Country']
    #     temp_city_name = row['city']
    #     temp_lat_lon = row['Latitude_Longitude']
    #     temp_city_code = row['city_code']
    #     temp_city_area = str(row['Area of city in sq km'])
    #     country = Countries.objects.get(name = temp_country_name)
    #     error_f=False

    #     temp_mongo_id =""
    #     event_id = get_event_id()
    #     if len(event_id) > 40:
    #         print("Greater than 40")
    #         print(event_id)
    #         raise Exception("Error in Created Event Id ")

    #     print("lerngth of area")
    #     print(len(str(temp_city_area)))
    #     temp_dict = {"name":temp_city_name,
    #     "lat_lon":temp_lat_lon,"city_code":temp_city_code,"city_area":temp_city_area, "eventId":event_id, "country":country.mongo_id}
    #     print("temp_dict dowell")
    #     print(temp_dict)
    #     error_fix ={0:"62bdc4c2193e4e0b85993dcc", 1: "62bdc4dd8ef9304ec49940e0", 2: "62bdc9748ef9304ec499411d"}
    #     if index== 0 or index==1 or index==2:
    #         print("Error to fix ==========================================")
    #         data_u = {
    #         "country":country.mongo_id
    #     }
    # # # FB1010000000165657602259221966
    #         result = mongo_update('region',error_fix[index], data_u)
    #         # 'FB1010000000016566050395329531',
    #         if index==2:
                
    # # # FB1010000000165657602259221966
    #             region = Regions(country=country,name=temp_city_name,lat_lon=temp_lat_lon,city_code=temp_city_code,
    #             city_area= temp_city_area, mongo_id = error_fix[index],event_id='FB1010000000016566050395329531')
    #             region.save()
    
    #     else:
    #         error_f=True
    #         result = mongo_create("region", temp_dict)
    #     if result["isSuccess"]:
    #         if error_f:
    #             print("Country: "+str(temp_country_name)+" for City: "+str(temp_city_name)+" --> insert Id: "+str(result["inserted_id"]))
    #             temp_mongo_id= result["inserted_id"]
    #             region = Regions(country=country,name=temp_city_name,lat_lon=temp_lat_lon,city_code=temp_city_code,
    #             city_area= temp_city_area, mongo_id = temp_mongo_id,event_id=event_id)
    #             region.save()
    #         else:
    #             print("Country: "+str(temp_country_name)+" for City: "+str(temp_city_name)+" --> insert Id: ")
                
                
            
            
    #     else:
    #         print("Country: "+str(temp_country_name)+" for City: "+str(temp_city_name)+" --> Error: "+str(result["error"]))
    #         raise Exception("Error occured in mongo insertion for Country: "+str(temp_country_name)+" City: "+str(temp_city_name))
    #     print("===============================================Except==================================================")



    # Loop in dowellCountries
    # check cpuntry is not in absent_soln
    # get country continent from pandas
    # print("test get continent")
    # df.loc[df['shield'] > 35] = 0
    # print(list(locContinentMatcher.loc[locContinentMatcher['country']=='Czech Republic']['continent'].values)[0])


