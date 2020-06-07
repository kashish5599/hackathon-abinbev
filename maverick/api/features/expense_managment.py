import requests
import pandas as pd
import json
import os 

class expense_management:
    def _init(self):
        self.baseurl = 'https://books.zoho.in/api/v3'
        self.orgid = '60004824857'
        self.token = '1000.ef49f2e68b65d2f573a2f337c0af5b03.d4b1362bbbf99530bd4f279d7872fc8c'
        self.headers = {'Authorization':'Zoho-oauthtoken '+self.token}
    
    def create_expense(self,account_id,date,amount):
        data = {'account_id':account_id,'date': date,'amount':amount}
        response = requests.post(self.url+'/expenses?organization_id='+self.orgid,json=data,headers=self.headers)
        output = {'msg':json.loads(response.text)['message'],'data':None}
        return output
    
    def update_expense(self,expense_id,account_id,date,amount):
        data = {'account_id':account_id,'date': date,'amount':amount}
        response = requests.put(self.url+'/expenses/'+str(expense_id)+'?organization_id='+self.orgid,json=data,headers=self.headers)
        output = {'msg':json.loads(response.text)['message'],'data':None}
        return output
        
    def get_expense(self,expense_id):
        response = requests.get(self.url+'/expenses/'+str(expense_id)+'?organization_id='+self.orgid,headers=self.headers)
        expense_json = json.loads(response.text)['expense'] 
        data = pd.DataFrame([[expense_json['account_name'],str(expense_json['total']),expense_json['date']]],columns=['Expense Type','Amount','Date of Expense'])
        output = {'msg':None,'data':data}
        return output
    
    def list_expenses(self):
        response = requests.get(self.url+'/expenses/?organization_id='+self.orgid,headers=self.headers)
        expense_list = []
        for instance in json.loads(response.text)['expenses']:
            expense_list.append([instance['account_name'],str(instance['total']),instance['date']])
        data = pd.DataFrame(expense_list,columns=['Expense Type','Amount','Date of Expense'])
        output = {'msg':None,'data':data}
        return output
    
    def delete_expense(self,expense_id):
        response = requests.delete(self.url+'/expenses/'+str(expense_id)+'?organization_id='+self.orgid,headers=self.headers)
        output = {'msg':json.loads(response.text)['message'],'data':None}
        return output
    
    def list_expense_history(self,expense_id):
        response = requests.get(self.url+'/expenses/'+str(expense_id)+'/comments?organization_id='+self.orgid,headers=self.headers)
        comments = [] 
        for comment in json.loads(response.text)['comments']:
            comments.append([comment['comment_id'],comment['description'],comment['date_description']])
        data = pd.DataFrame(comments,columns=['Comment_Id','Description','Date_of_Description'])
        output = {'msg':None ,'data':data}
        return output