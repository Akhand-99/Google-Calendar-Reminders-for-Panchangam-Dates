from bs4 import BeautifulSoup
import requests
from datetime import *

# import smtplib
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
py_date_list = []


def convert_date_text_to_py_date(date_text_param):
    month_dictionary_num_string = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
                                   'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
                                   'November': '11', 'December': '12'}

    date_of_month = date_text_param.split()[2].split(',')[0]
    month = date_text_param.split()[1]
    month_num_string = month_dictionary_num_string[month]
    year = date_text_param.split()[-1]

    return date(int(year), int(month_num_string), int(date_of_month))


def panchanga_date_converter():
    global py_date_list
    date_text_list = []
    maasa_dict = {'01': 'Chaitra', '02': 'Vaishakha', '03': 'Jyeshtha', '04': 'Ashadha', '05': 'Shravana',
                  '06': 'Bhadrapada', '07': 'Ashvija', '08': 'Kartik', '09': 'Margashira', '10': 'Pushya',
                  '11': 'Magha', '12': 'Phalguna'}
    paksha_dict = {'01': 'Shuklapaksha', '02': 'Krishnapaksha'}
    padya_bidige_dict = {'01': 'Padya', '02': 'Bidige', '03': 'Tadige', '04': 'Chauthi', '05': 'Panchami',
                         '06': 'Shashti', '07': 'Saptami', '08': 'Ashtami', '09': 'Navami', '10': 'Dashami',
                         '11': 'Ekadashi', '12': 'Dwadashi', '13': 'Trayodashi', '14': 'Chaturdashi',
                         '15': ['Hunnime', 'Amavasya']}

    print('Type "01" for Chaitra month\nType "02" for Vaishakha month\nType "03" for Jyeshtha month\nType "04" for '
          'Ashadha month')
    print('Type "05" for Shravana month\nType "06" for Bhadrapada month\nType "07" for Ashvija month\nType "08" for '
          'Kartik month')
    print('Type "09" for Margashira month\nType "10" for Pushya month\nType "11" for Magha month\nType "12" for '
          'Phalguna month')
    print('We request you to strictly type in a 2 digit number like "01" or "02" instead of 1 digit number like "1" '
          'or "2"\n')

    panchanga_month_choice = input('Your input: ')
    print(f'Your month input = {panchanga_month_choice}\n')

    paksha_choice = input('Type "01" for Shuklapaksha or Type "02" for Krishnapaksha: ')
    print(f'Your paksha input = {paksha_choice}\n')

    print('Type "01" for Padya\nType "02" for Bidige\nType "03" for Tadige\nType "04" for Chauthi\nYou get the drill('
          'till Hunnime/Amavasya for which you type "15")')
    padya_bidige_tadige_choice = input('Your input: ')
    print(f'Your day input = {padya_bidige_tadige_choice}\n')

    if paksha_choice == '01':
        panchanga_dd = padya_bidige_tadige_choice
    else:
        panchanga_dd = str(int(padya_bidige_tadige_choice) + 15)
    print(f'Panchanga dd = {panchanga_dd}\n')

    today = date.today()
    if int(panchanga_month_choice) > 7:
        shaka_year = today.year - 79
        url1 = 'https://www.drikpanchang.com/kannada/panchangam/kannada-month-panchangam.html?lunar-date=' + panchanga_dd + '/' + panchanga_month_choice + '/' + str(
            shaka_year)
        html_text = requests.get(url1).text
        soup = BeautifulSoup(html_text, 'lxml')
        date_text = soup.find('h2', class_='dpCardTitle dpLeftGridTitle').text

        converted_py_date = convert_date_text_to_py_date(date_text)

        if converted_py_date < today:
            shaka_year = today.year - 78
            url1 = 'https://www.drikpanchang.com/kannada/panchangam/kannada-month-panchangam.html?lunar-date=' + panchanga_dd + '/' + panchanga_month_choice + '/' + str(
                shaka_year)
            html_text = requests.get(url1).text
            soup = BeautifulSoup(html_text, 'lxml')
            date_text = soup.find('h2', class_='dpCardTitle dpLeftGridTitle').text

            converted_py_date = convert_date_text_to_py_date(date_text)
    else:
        shaka_year = today.year - 78
        url1 = 'https://www.drikpanchang.com/kannada/panchangam/kannada-month-panchangam.html?lunar-date=' + panchanga_dd + '/' + panchanga_month_choice + '/' + str(
            shaka_year)
        html_text = requests.get(url1).text
        soup = BeautifulSoup(html_text, 'lxml')
        date_text = soup.find('h2', class_='dpCardTitle dpLeftGridTitle').text

        converted_py_date = convert_date_text_to_py_date(date_text)

    py_date_list.append(converted_py_date)
    date_text_list.append(date_text)

    print(f'The Panchanga date you entered coincides with the Gregorian date: {date_text_list[0]}\nPlease check if '
          f'this is correct\n')

    count = 1
    while count < 30:
        url = 'https://www.drikpanchang.com/kannada/panchangam/kannada-month-panchangam.html?lunar-date=' + panchanga_dd + '/' + panchanga_month_choice + '/' + str(
            shaka_year + count)
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        date_text = soup.find('h2', class_='dpCardTitle dpLeftGridTitle').text
        converted_py_date = convert_date_text_to_py_date(date_text)
        py_date_list.append(converted_py_date)
        date_text_list.append(date_text)
        count += 1

    selected_maasa_name = maasa_dict[panchanga_month_choice]
    selected_paksha_name = paksha_dict[paksha_choice]

    if padya_bidige_tadige_choice == '15':
        if paksha_choice == '01':
            selected_dina_name = 'Hunnime'
        else:
            selected_dina_name = 'Amavasya'
    else:
        selected_dina_name = padya_bidige_dict[padya_bidige_tadige_choice]
    message = f'Hare Krishna. {selected_maasa_name} {selected_paksha_name} {selected_dina_name} for the next 30 years ' \
              f'will occur on the following dates {date_text_list}.\n'
    print(message)


def set_gcal_reminders():
    recur_date_str = ''
    first_py_date_list = py_date_list.pop(0)
    for date_item in py_date_list:
        date_str = date.isoformat(date_item)
        recur_date_str += date_str.replace('-', '') + 'T100000,'
    recur_date_str = recur_date_str.rstrip(',')
    py_date_list.insert(0, first_py_date_list)

    reminder_title = input("Enter the title of the reminder: ")

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('cred.json.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open('token.json', 'w') as token:
        #    token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        event_details = {
            'summary': reminder_title,
            'start': {
                'dateTime': f'{py_date_list[0]}T10:00:00',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': f'{py_date_list[0]}T12:00:00',
                'timeZone': 'Asia/Kolkata',
            },
            "recurrence": [
                f"RDATE;TZID=Asia/Kolkata:{recur_date_str}"  ## Important: No spaces allowed in this line.
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 7 * 24 * 60},
                    {'method': 'popup', 'minutes': 7 * 24 * 60},
                    {'method': 'email', 'minutes': 2 * 24 * 60},
                    {'method': 'popup', 'minutes': 2 * 24 * 60},
                    {'method': 'popup', 'minutes': 18 * 60},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event_details, sendUpdates='all').execute()
        print('\nEvent created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('\nAn error occurred: %s' % error)


def main():
    print('Welcome! This is a Panchanga date to Gregorian date converter!\n')
    panchanga_date_converter()
    y_or_n = input('Do you want to set reminder for the dates mentioned above? Type "y" for yes or "n" for no: ')
    if y_or_n == 'y':
        set_gcal_reminders()
    elif y_or_n == 'n':
        print("Thanks for using this app! Shutting down. Don't wait, just close the app.")
    else:
        print("Invalid input! Restart the app!")


if __name__ == '__main__':
    main()
