from .features.timelog import timelogfun
from .features.tickets import ticket_func
from .features.covidcases import covidcasesfun
from .features.expense_managment import expense_management
from .features.token_generator import token_generator
import requests
import json
import urllib.parse

class mediatorCall:
    def __init__(self,msg):
        #Wit Api Integration
        self.msg = msg
        self.token = ''
        self.headers = {'Authorization':'Bearer '+self.token}

        tok_gen = token_generator()
        token_expense = tok_gen.expense()
        token_ticket = tok_gen.ticket()

        self.ticket_func = ticket_func(token_ticket['access_token'], token_ticket['organization_id'])
        self.expense_management = expense_management(token_expense['access_token'], token_expense['organization_id']);
        self.timelogfun = timelogfun(tok_gen.timelog())

    def run_query(self):
        ## Recognizing the Intent Out The Message ##
        url = 'https://api.wit.ai/message?v=20200617&q='+ urllib.parse.quote(self.msg)
        message_intent = ''
        message_entities = {}
        intents_list , entity_list = self.get_message(url)
        message_intent = intents_list[0]['name']
        message_intent = message_intent.split("_")
        for entity in entity_list :
            message_entities[entity['type']] = entity['word']
        temp = message_intent[0].lower()
        if(temp=="add"):
            output=self.command_add(message_intent,message_entities)
        elif(temp=="show"):
            output=self.command_show(message_intent,message_entities)
        elif(temp=="search"):
            output=self.command_search(message_intent,message_entities)
        elif(temp=="change"):
            output=self.command_change(message_intent,message_entities)
        elif(temp == "create"):
            output=self.command_create(message_intent,message_entities)
        elif(temp == "close"):
            output=self.command_close(message_intent,message_entities)
        elif(temp == "delete"):
            output=self.command_delete(message_intent,message_entities)
        return output

    def get_message(self,url):
        response = requests.get(url,self.headers)
        response_json = json.loads(response.text)
        #Getting Intents
        intents_list = response_json['intents']
        #Getting Entities
        entity_whole_list = []
        entity_type_list = list(response_json['entities'].keys())
        for entity_type in entity_type_list :
            entity_list = response_json['entities'][entity_type]
            for entity in entity_list :
                new_entity_dict ={}
                new_entity_dict['entity_id'] = entity['id']
                new_entity_dict['word'] = entity['body']
                new_entity_dict['type'] = entity['name']
                new_entity_dict['role'] = entity['role']
                try :
                    new_entity_dict['value'] = entity['value']
                except :
                    print("Missing Value Check Response")
                new_entity_dict['confidence'] = entity['confidence']
                entity_whole_list.append(new_entity_dict)
        return intents_list,entity_whole_list

    def command_add(self,intent,entities):
        if(intent.split()[1].lower()=='employee'):
            output = self.timelogfun.add_employee(entities['name_of_person'].split()[0],entities['name_of_person'].split()[1],entities['wit$email'],entities['employee_id'])
        elif(intent.split()[1].lower()=='job'):
            output = self.timelogfun.add_job(entities['wit$email'],entity['job_type'],entity['work_date'],entity['duration'])
        elif(intent.split()[1].lower()=='expense'):
            account_id = self.expense_managment.get_account_id(entities['account_name'])
            output = self.expense_management.create_expense(account_id,entities['date'],entities['amount'])
        return output

    def command_show(self,intent,entities):
        if(intent.split()[1].lower()=='employee'):
            output = self.timelogfun.all_employees()
        elif(intent.split()[1].lower()=='jobs'):
            output = self.timelogfun.all_jobs(entities['wit$email'])
        elif(intent.split()[1].lower()=='timelog'):
            output = self.timelogfun.get_timelog(entities['wit$email'],entities['from_time'],entities['to_time'])
        elif(intent.split()[1].lower()=='tickets'):
            output=self.ticket_func.show_tickets()
        elif(intent.split()[1].lower()=='departments'):
            output=self.ticket_func.show_departments()
        elif(intent.split()[1].lower()=='customers'):
            output=self.ticket_func.show_customers()
        elif(intent.split()[1].lower()=='covid' and intent.split()[2].lower()=='cases'):
            output=covidcasesfun.cases(entities['state'],entities['district'])
        elif(intent.split()[1].lower()=='expenses'):
            output=self.expense_management.list_expenses()
        elif(intent.split()[1].lower()=='expense'):
            output=self.expense_management.list_expense_history(entities['expense_id'])
        elif(intent.split()[1].lower()=='accounts'):
            output=self.expense_management.list_accounts()
        return output

    def command_search(self,intent,entities):
        if(intent.split()[1].lower()=='employee'):
            output = self.timelogfun.search_employee(entities['wit$email'])
        elif(intent.split()[1].lower()=='expense'):
            output=self.expense_management.get_expense(entities['expense_id'])
        return output

    def command_change(self,intent,entities):
        if(intent.split()[1].lower()=='job')
            output = self.timelogfun.change_job_status(entities['job_id'],entities['status'])
        elif(intent.split()[1].lower()=='expense'):
            account_id = self.expense_managment.get_account_id(entities['account_name'])
            output=self.expense_management.update_expense(entities['expense_id'],account_id,entities['date'],entities['amount'])
        return output

    def command_create(self,intent,entities):
        if(intent.split()[1].lower()=='ticket'):
            output = self.ticket_func.create_ticket(entities['customer_id'],entities['department_id'],entities['description'])
        return output

    def command_close(self,intent,entities):
        if(intent.split()[1].lower()=='ticket'):
            output = self.ticket_func.close_ticket(entities['ticket_id'])
        return output
            
    def command_delete(self,intent,entities):
        if(intent.split()[1].lower()=='expense'):
            output=self.expense_management.delete_expense(entities['expense_id'])
        return output