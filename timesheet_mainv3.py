import telebot
from telebot import types
import requests
from datetime import *

#def bop(x,y):
def bot():

    api_token = "1846505493:AAE-jdoGQn2HgOtCj1t1m6zgo_XxTTENuLU" #Test007

    #api_token = "1906415266:AAECXN-sEfmLaVIn-4lcN7HtGke-4O0nra8" #Quandle

    bot = telebot.TeleBot(api_token)

    print(bot.get_me())    

    #today = str(date.today().strftime("%d/%m/%Y"))
    #today shows the Date in format 13/10/1995

    #------------------------------------------------------
    
    @bot.message_handler(commands='start')
    def start(message):

        #first_name = str(message.from_user.first_name)

        #bot.reply_to(message,"Hello "+first_name)

        markup = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        markup.add('Date','Working Hours Status','Fill Timesheet','Fill Timesheet - Manual')
        msg = bot.send_message(chat_id=message.chat.id,text="Choose One Option ",reply_markup=markup)
        #msg = bot.reply_to(message,"Choose One Option ",reply_markup=markup)
        
        # st1 = str(msg.text)
        # print("str1 "+st1)

        bot.register_next_step_handler(msg,job)    

    def job(reply):
        st = str(reply.text)     

        print("st "+st)

        today = str(date.today().strftime("%d/%m/%Y"))

        #msg = bot.reply_to(reply, "Message : "+st)

        if st=="Working Hours Status":
            status(reply)

        if st=="Date":
            #date1(reply,today)
            bot.send_message(chat_id=reply.chat.id,text="Date is : "+today)
        
        if st=="Fill Timesheet":
            timesheet_status(reply,today)

        if st=="Fill Timesheet - Manual":
            msg = bot.send_message(chat_id=reply.chat.id,
                            text="Please send Date for Timesheet to be filled \n Format : 13/10/1995"
                            )
            bot.register_next_step_handler(msg,timesheet_manual)

            #timesheet_manual(reply)

    def status(message):
        #bot.send_message(chat_id=message.chat.id,text="I am Working...") 

        month = str(date.today().strftime("%m"))
        year = str(date.today().strftime("%Y"))

        url = "https://acpl.qandle.com/timesheet/tracker/01-"+month+"-"+year+"/30-"+month+"-"+year

        accesst = login()

        bearer = "Bearer "

        headers = { "Authorization": bearer+accesst }

        response = requests.get(url,headers=headers)

        print("Status Code : ", response.status_code)
        #print("Response :", response.json())

        response_json = response.json()
        res_data = response_json["data"]
        res = res_data["overall"]
        #print("Access Token : ", res_data["accessToken"])

        for x in res:
            msg = x+" : "+res[x]
            bot.send_message(chat_id=message.chat.id,text=msg)


    #====Functions===============================================================

    #@bot.message_handler(commands='timesheet')
    def timesheet_manual(message):

        today = str(message.text)            
        accesst = login()
        tm = str(timesheetm(accesst,today))
        #a = at
        #b = str(tm)
        #print("Before message at :",a)        

        message_final = "Access Token : \n"+accesst+"\n\nTimesheet Status for "+today+" : \n"+tm
            
        bot.send_message(
            chat_id = message.chat.id,
            text = message_final
            )
        
    def timesheet_status(message,today):
                  
        accesst = login()
        tm = str(timesheet(accesst))
        #a = at
        #b = str(tm)
        #print("Before message at :",a)        

        message_final = "Access Token : \n"+accesst+"\n\nTimesheet Status for "+today+" : \n"+tm
            
        bot.send_message(
            chat_id = message.chat.id,
            text = message_final
            )

    bot.infinity_polling()

#===Login=====================================================================  

def login():
    url = "https://acpl.qandle.com/auth/login"

    parm =  {
            "password":"@ashu4635",
            "email":"ashishsingh@acpl.co.in"
            }

    response = requests.post(url, data=parm)

    #print("Login Status Code : ", response.status_code)
    #print("Response :", response.json())

    response_json = response.json()
    res_data = response_json["data"]

    accesstoken = res_data["accessToken"]

    #print("Access Token : ",accesstoken )

    return accesstoken

#===Timesheet=====================================================================

def timesheetm (accessT,today):

    url = "https://acpl.qandle.com/timesheet/fill/5f0ff7fa4e7e6ec130ae4fd7"

    #headers = { "Authorization": "Bearer sWpjUNzQKMC0QL3cL9csOwKCG5siUj4vgepHMSxk" }

    #today = str(date.today().strftime("%d/%m/%Y"))
    #today shows the tin in format 13/10/1995

    print(today)

    bearer = "Bearer "

    headers = { "Authorization": bearer+accessT }

    #print("Headers : ",headers)

    parm = {
            #"timesheet_start_date": "11/09/2021", 
            "timesheet_start_date": today,
            "timesheet_end_date": "", 
            "timesheet_start_time": "13:00", 
            "timesheet_end_time": "23:00", 
            "timesheet_description": "skybox work , daily and weekly reports , analysis , R&D", 
            "product_name": "", 
            "product_2": "", 
            "product_3": "", 
            "customer_name": "", 
            "working_day_status": "5f0ffb724e7e6e3a35ae4fdd", 
            "activity_1": "5f1005af4e7e6eed48ae4fdd", 
            "customer_1": "5f1009394e7e6ee04eae4fdb", 
            "customer_1_if_not_in_the_list": "", 
            "technology_1": "", 
            "technology_1_if_not_in_list": "Skybox", 
            "product1": "", 
            "product1_if_not_in_list": "Skybox", 
            "time_spent_in_hours": "8+hrs", 
            "activity_2": "", 
            "customer_2": "", 
            "customer_2_if_not_in_the_list": "", 
            "technology_2": "", 
            "technology_2_if_not_in_list": "", 
            "product2": "",
            "product_2_if_not_in_list": "", 
            "time_spent_in_hours_2": "", 
            "activity_3": "", 
            "customer_3": "", 
            "customer_3_if_not_in_the_list": "",
            "technology_3": "", 
            "technology_3_if_not_in_list": "", 
            "product3": "", 
            "product_3__if_not_in_list": "", 
            "time_spent_in_hours_3": "", 
            "activity_4": "", 
            "activity_4_if_not_in_list": "", 
            "customer_4": "", 
            "customer_4_if_not_in_list": "", 
            "technology_4": "", 
            "technology_4_if_not_in_list": "",
            "product_4": "", 
            "product_4_if_not_in_list": "", 
            "time_spent_in_hours_4": "", 
            "description_activity_1": "", 
            "description__activity_2": "", 
            "description__activity_3": "", 
            "description_activity_4": "", 
            "customer_5": "", 
            "technology_5": "", 
            "product_5": "", 
            "description_5": "", 
            "time_spent_in_hours_5": "", 
            "any_other_remark": ""
            }

    response = requests.post(url, headers=headers, data=parm)

    #print("Status Code : ", response.status_code)

    response_json = response.json()
    #print(response_json["message"])

    timesheet_message = response_json["message"]
    return timesheet_message

def timesheet (x):

    url = "https://acpl.qandle.com/timesheet/fill/5f0ff7fa4e7e6ec130ae4fd7"

    #headers = { "Authorization": "Bearer sWpjUNzQKMC0QL3cL9csOwKCG5siUj4vgepHMSxk" }

    today = str(date.today().strftime("%d/%m/%Y"))
    #today shows the tin in format 13/10/1995

    #print(today)

    bearer = "Bearer "

    headers = { "Authorization": bearer+x }

    #print("Headers : ",headers)

    parm = {
            #"timesheet_start_date": "11/09/2021", 
            "timesheet_start_date": today,
            "timesheet_end_date": "", 
            "timesheet_start_time": "13:00", 
            "timesheet_end_time": "23:00", 
            "timesheet_description": "skybox work , daily and weekly reports , analysis , R&D", 
            "product_name": "", 
            "product_2": "", 
            "product_3": "", 
            "customer_name": "", 
            "working_day_status": "5f0ffb724e7e6e3a35ae4fdd", 
            "activity_1": "5f1005af4e7e6eed48ae4fdd", 
            "customer_1": "5f1009394e7e6ee04eae4fdb", 
            "customer_1_if_not_in_the_list": "", 
            "technology_1": "", 
            "technology_1_if_not_in_list": "Skybox", 
            "product1": "", 
            "product1_if_not_in_list": "Skybox", 
            "time_spent_in_hours": "8+hrs", 
            "activity_2": "", 
            "customer_2": "", 
            "customer_2_if_not_in_the_list": "", 
            "technology_2": "", 
            "technology_2_if_not_in_list": "", 
            "product2": "",
            "product_2_if_not_in_list": "", 
            "time_spent_in_hours_2": "", 
            "activity_3": "", 
            "customer_3": "", 
            "customer_3_if_not_in_the_list": "",
            "technology_3": "", 
            "technology_3_if_not_in_list": "", 
            "product3": "", 
            "product_3__if_not_in_list": "", 
            "time_spent_in_hours_3": "", 
            "activity_4": "", 
            "activity_4_if_not_in_list": "", 
            "customer_4": "", 
            "customer_4_if_not_in_list": "", 
            "technology_4": "", 
            "technology_4_if_not_in_list": "",
            "product_4": "", 
            "product_4_if_not_in_list": "", 
            "time_spent_in_hours_4": "", 
            "description_activity_1": "", 
            "description__activity_2": "", 
            "description__activity_3": "", 
            "description_activity_4": "", 
            "customer_5": "", 
            "technology_5": "", 
            "product_5": "", 
            "description_5": "", 
            "time_spent_in_hours_5": "", 
            "any_other_remark": ""
            }

    response = requests.post(url, headers=headers, data=parm)

    #print("Status Code : ", response.status_code)

    response_json = response.json()
    #print(response_json["message"])

    timesheet_message = response_json["message"]
    return timesheet_message


def main():

    bot()


if __name__ == "__main__":

    main()

