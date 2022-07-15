from rmsystem.packages import * 

admin= Blueprint('admin', __name__)

def now_time():
    return datetime.datetime.now()


@admin.route('/register', methods=['POST'])
def register_admin():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    admin_db = mongo.db.admin
    jsonobject=request.json
    now = now_time()
    hashpass = generate_password_hash(jsonobject['password'], method='sha256')  #Generates hashed password
    account=admin_db.find_one({'email' :jsonobject['email']})
    if account is None:
        mongo.db.admin.insert_one({"full_name": jsonobject['full_name'],
                            "email" : jsonobject['email'],
                            "password":hashpass,
                            "registration_date":now,
                            "phone_number":jsonobject['phone_number'],
                            # "restaurantname":jsonobject['restaurant_name'],
                            })
        ret = {"success":True,"message":"succuessfully registered"}
    else:
        ret = {"success":False,"message":"ALready registered"}
    return ret

@admin.route('/login', methods=['POST'])
def login():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    admin_db = mongo.db.admin
    jsonobject=request.json
    now = now_time()
    email=jsonobject['email']
    password=jsonobject['password']
    account=admin_db.find_one({'email' :email})
    if account is not None:
        password_matched= check_password_hash(account['password'],password)
        if password_matched  :
            ret = {"message" : "logged-in.","success" : True}
            session["admin"] = email
        else:
            ret = {"message" : " check username/pass","success" : False}
    else:
        ret = {"message" : " check username/pass","success" : False}
        
    return ret


@admin.route('/hotel/add', methods=['POST'])   #edit by id , #delete by id , # get by id
def add_hotel():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    hotel_db = mongo.db.hotel
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    if admin_sess:
        present_hotel=hotel_db.find_one({'hotel_name' :jsonobject['hotel_name']})
        if present_hotel is None:
            mongo.db.hotel.insert_one({"hotel_name": jsonobject['hotel_name'],
                            "location" : jsonobject['location'],
                            "email":"email",
                            "creation_date":now,
                            "phone_number":jsonobject['phone_number'],
                            "admin":admin_sess
                            })
            ret ={"success":True, "message":"inserted"}
        else:
            ret = {"message" : "select diff name","success" : False}
    else:
        ret = {"success":False, "message":"plz login"}
        
    return ret



@admin.route('/hotel/view', methods=['GET'])   #edit by id , #delete by id , # get by id
def view_hotel():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    hotel_db = mongo.db.hotel
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    print(admin_sess)
    if admin_sess is not None:
        present_hotel=hotel_db.find_one({'admin' :admin_sess})
        ret = json.loads(json_util.dumps(present_hotel))
        
    else:
        ret = {"success":False, "message":"plz login"}
        
    return ret




@admin.route('/hotel/category/add', methods=['POST'])   #edit by id , #delete by id , # get by id , # get all
def add_category():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    category_db = mongo.db.category
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    present_hotel=mongo.db.hotel.find_one({'admin' :admin_sess})

    if admin_sess and present_hotel is not None:

        present_category=category_db.find_one({'category_name' :jsonobject['category_name']})
        if present_category is None:
            # status - if they want to enable or disable based on availabilty
            # category_name - starter / main course / desserts
            category_db.insert_one({"category_name": jsonobject['category_name'],  
                            "status" : jsonobject['status'], 
                            "admin":admin_sess
                            })
            ret ={"success":True, "message":"inserted"}
        else:
            ret = {"message" : "already there","success" : False}
    else:
        ret = {"success":False, "message":"plz login / create hotel"}  # can make diff condition for login and checking hotel
        
    return ret



@admin.route('/hotel/item/add', methods=['POST'])   #edit by id , #delete by id , # get by id , # get all
def add_item():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    item_db = mongo.db.item
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    present_hotel=mongo.db.hotel.find_one({'admin' :admin_sess})

    if admin_sess and present_hotel is not None:

        present_category=mongo.db.category.find_one({'category_name' :jsonobject['category_name']})  # better to go with category id due to time constraint here i am choosing name
        if present_category is not None:
            item_db.insert_one({"item_name": jsonobject['item_name'],  
                            "item_price": jsonobject['item_price'],
                            "category_name":jsonobject['category_name'],  
                            "admin":admin_sess,
                            "status" : jsonobject['status'], 
                            })
            ret ={"success":True, "message":"inserted"}
        else:
            ret = {"message" : "invalid category_name","success" : False}
    else:
        ret = {"success":False, "message":"plz login / create hotel"}  # can make diff condition for login and checking hotel
        
    return ret


@admin.route('/hotel/table/add', methods=['POST'])   #edit by id , #delete by id , # get by id , # get all
def add_table():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    table_db = mongo.db.table
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    present_hotel=mongo.db.hotel.find_one({'admin' :admin_sess})

    if admin_sess and present_hotel is not None:

        present_table=table_db.find_one({'table_name' :jsonobject['table_name']})
        if present_table is None:
            table_db.insert_one({"table_name": jsonobject['table_name'],  
                            "admin":admin_sess,
                            "capacity":jsonobject['capacity'],
                            "occupied":False,
                            "status" : jsonobject['status'],  # if they want to enable or disable based on availabilty
                            }) # haven't handled multiple same items insertion error
            ret ={"success":True, "message":"inserted"}
        else:
            ret = {"message" : "already present","success" : False}
    else:
        ret = {"success":False, "message":"plz login / create hotel"}  # can make diff condition for login and checking hotel
        
    return ret


#create orders based on tables
@admin.route('/hotel/orders/add', methods=['POST'])   #edit by id , #delete by id , # get by id , # get all
def add_orders():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    orders_db = mongo.db.orders
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    present_hotel=mongo.db.hotel.find_one({'admin' :admin_sess})

    if admin_sess and present_hotel is not None:

        orders_db.insert_one({"order_no":jsonobject['order_no'],  #now i have take it as input , later can be made as random int/char using library uuid
                            "table_name": jsonobject['table_name'],  
                            "ordered_list": jsonobject['ordered_list'],
                            "customer_name":None,
                            "customer_phone":None,
                            "waiter_name":jsonobject['waiter_name'],
                            "admin":admin_sess,
                            "date":now,
                            "occupied":True, 
                            # "customer_feedback":jsonobject['customer_feedback']  #better to create diff table for rating /feedback
                            "status" : jsonobject['status'],  # if they want to enable or disable based on availabilty
                            })
        ret ={"success":True, "message":"inserted"}
        
    else:
        ret = {"success":False, "message":"plz login / create hotel"}  # can make diff condition for login and checking hotel
        
    return ret

#here we can update anything related to orders , but here we have to pass all the parameters and order no. 
@admin.route('/hotel/orders/update', methods=['POST'])   
def update_orders():
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    orders_db = mongo.db.orders
    jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    present_hotel=mongo.db.hotel.find_one({'admin' :admin_sess})
    present_order=mongo.db.orders.find_one({'order_no' :jsonobject['order_no']})
    if admin_sess and present_hotel is not None:
        if present_order is not None:
            myquery = {"order_no":jsonobject['order_no']}
            dict_another = jsonobject
            del dict_another['order_no']
            newvalues = { "$set":  dict_another  }
            mongo.db.orders.update_one(myquery, newvalues)
            ret ={"success":True, "message":"updated"}
        else:
             ret = {"success":False, "message":"order no. invalid"}
        
    else:
        ret = {"success":False, "message":"plz login / create hotel"}  # can make diff condition for login and checking hotel
        
    return ret

#limit - if they want top 5 / top 3 / top 10 items
@admin.route('/hotel/items/top/<limit>', methods=['GET'])   
def top_items(limit):
    ret = {"success":False,"message":"An unexpected error has occurred, please try again later"}
    orders_db = mongo.db.orders
    # jsonobject=request.json
    now = now_time()
    admin_sess = session.get('admin')
    present_hotel=mongo.db.hotel.find_one({'admin' :admin_sess})

    if admin_sess and present_hotel is not None:

        output = orders_db.aggregate([
                                { "$unwind": "$ordered_list" },
                                {
                                    "$group": {
                                        "_id": "$ordered_list.item_name",
                                        "count": { "$sum": 1 }
                                    }
                                },
                                { "$sort": { "count": -1 } },
                                { "$limit": int(limit) } ,
                                { "$project": {  
                                    "_id": 0,
                                    "item_name": "$_id",
                                    "count": 1
                                }
                                }
                            ])
        final_out = []
        for i in output:
            final_out.append(i)
        ret = final_out
        
    else:
        ret = {"success":False, "message":"plz login / create hotel"}  # can make diff condition for login and checking hotel
        
    return jsonify(ret)

@admin.route('/logout', methods=['GET'])
def LogoutHandler():
    session.pop('admin', None)
    ret = {"success":True,"message":'Logged Out Successful.'}
    return jsonify(ret)


