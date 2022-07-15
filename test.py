from datetime import date
import random

username = 'shivam'
application_number = 'GI/'+ str(date.today().year) +'/' + username[0:3].upper() + str(random.randrange(100000000, 1000000000))

print(application_number)