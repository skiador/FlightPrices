import configparser
import datetime
import os
import time

import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
    NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Set parameters for SQL Db connection
def connect_to_sql_db(host_name, user_name, user_password, db):
    dbconnection = None
    try:
        dbconnection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    cursor = dbconnection.cursor()

    return dbconnection, cursor


def configure_driver():
    # Set up the Chrome driver options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    # Set up the Chrome driver path relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(script_dir, "chromedriver.exe")

    # Create a new Chrome driver instance using options and a service object
    service = webdriver.chrome.service.Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def go_to_page(driver, departure, destination, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            driver.get("https://tickets.vueling.com//ScheduleSelectNew.aspx")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#onetrust-accept-btn-handler")))
            break  # Successful execution, exit the retry loop
        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # Cookies accept
    retries = 0
    while retries < max_retries:
        try:
            accept_cookies_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler")))
            accept_cookies_button.click()
            print('Cookies accepted')
            break
        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # One way trip selection
    retries = 0
    while retries < max_retries:
        try:
            one_way_trip_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'fieldset.elForm_radio--label:nth-child(2) > label:nth-child(2)')))
            one_way_trip_button.click()
            print('One way trip selected')
            break
        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # Origin airport selection
    retries = 0
    while retries < max_retries:
        try:
            origin_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#AvailabilitySearchInputSearchView_TextBoxMarketOrigin1')))
            origin_input.click()
            origin_input_text_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="stationsList"]/ul/li[contains(normalize-space(), "{departure}")]')))
            origin_input_text_field.click()
            print(f'Origin airport selected as {departure}')
            break
        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # Definition of a background element to click on
    retries = 0
    background_element = None
    while retries < max_retries:
        try:
            background_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#buscador > h2:nth-child(1)')))
            break
        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # Destination airport selection
    retries = 0
    while retries < max_retries:
        try:
            background_element.click()
            destination_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#AvailabilitySearchInputSearchView_TextBoxMarketDestination1')))
            destination_input.click()
            destination_input_text_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="stationsList"]/ul/li[contains(normalize-space(), "{destination}")]')))
            destination_input_text_field.click()
            print(f'Destination airport selected as {destination}')
            break

        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # Close date picker
    close_date = driver.find_element(By.ID, "datePickerTitleCloseButton")
    retries = 5
    for _ in range(retries):
        try:
            # Perform the desired action on the element
            close_date.click()
            print("Date picker closed")
            break
        except StaleElementReferenceException:
            print("Trying again to close date picker due to StaleElementReferenceException...")
            time.sleep(1)
            close_date = driver.find_element(By.ID, "datePickerTitleCloseButton")  # Re-locate the element
        except ElementClickInterceptedException:
            print("Trying again to close date picker due to ElementClickInterceptedException...")
            time.sleep(1)

    # Search button click
    retries = 0
    while retries < max_retries:
        try:
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#AvailabilitySearchInputSearchView_btnClickToSearchNormal')))
            search_button.click()
            print('Search started')
            break
        except Exception as e:
            print("An exception occurred:", e)
            retries += 1
            if retries == max_retries:
                print("Max retries exceeded")
                return None
            print("Retrying...")
            time.sleep(1)

    # After this we should see the flightcards page


# Retrieve information of the selected flight
def get_day_info(driver):
    # This code gets the date from the calendar picker in the web page and stores it in the database
    # flights_database.json

    # Day from element
    day_element = driver.find_element(By.CSS_SELECTOR,
                                      '.selected > button:nth-child(1) > span:nth-child(2) > span:nth-child(2)')
    day = day_element.text

    # Month from element
    months_dict = dict(ene='01', feb='02', mar='03', abr='04', may='05', jun='06', jul='07', ago='08',
                       sep='09', oct='10', nov='11', dic='12')
    month = months_dict[
        driver.find_element(By.CSS_SELECTOR, '.selected > button:nth-child(1) > span:nth-child(1)').text.lower()]

    # Year doesn't appear on website to we take the current year if month is higher than today's month, and we take
    # year + 1 if month is lower than today's month, which means that the flight is next year
    year = datetime.date.today().year + (1 if datetime.datetime.today().month > int(month.lstrip('0')) else 0)

    # Format date string (dd-mm-yyyy)
    flight_date_string = f"{year}-{month}-{day}"

    print(f"Date of flight: {flight_date_string}")

    # Get all flightcards in the current page
    flightcards = driver.find_elements(By.CSS_SELECTOR, 'div.trip-selector_item')

    return flight_date_string, flightcards


def get_flight_info(item, flight_date_string, driver):
    flight_info_list = []

    try:
        block_element = driver.find_element(By.CSS_SELECTOR, "#wrapper > div.blockUI.blockOverlay")
        if block_element.is_displayed():
            for _ in range(3):
                try:
                    close_button = driver.find_element(By.ID, "keepSessionAliveBtn")
                    close_button.click()
                    break  # Successful click, exit the loop
                except Exception as e:
                    print(e)
                    time.sleep(5)
            else:
                print("Failed to click the button after multiple retries")

    except NoSuchElementException:
        pass  # Blocking element not found, proceed with getting flight information

    # Use the find_element_by_css_selector method to locate the specific element within each item
    flightnumber = item.find_element(By.CSS_SELECTOR,
                                     'label:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) '
                                     '> ul:nth-child(1) > li:nth-child(1) > span:nth-child(1)').text
    departure_time = flight_date_string + " " + item.find_element(By.CSS_SELECTOR,
                                                                  'label:nth-child(2)  > div:nth-child(1) > '
                                                                  'div:nth-child(3) > div:nth-child('
                                                                  '2) > span:nth-child(1)').text + ":00"
    arrival_time = flight_date_string + " " + item.find_element(By.CSS_SELECTOR,
                                                                'label:nth-child(2) > div:nth-child(1) > '
                                                                'div:nth-child(3) > div:nth-child(4)'
                                                                '> span:nth-child(1)').text + ":00"
    departure_airport = item.find_element(By.CSS_SELECTOR,
                                          'label:nth-child(2) > div:nth-child(1) > div:nth-child(3) > '
                                          'div:nth-child(2) > span:nth-child(3) > span:nth-child(1)').text
    arrival_airport = item.find_element(By.CSS_SELECTOR,
                                        'label:nth-child(2) > div:nth-child(1) > div:nth-child(3) > '
                                        'div:nth-child(4) > span:nth-child(3) > span:nth-child(1)').text
    airline = ''
    for char in flightnumber:
        if char.isdigit():
            break
        airline += char
    try:
        price_prov = item.find_element(By.CSS_SELECTOR,
                                       'label:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child('
                                       '1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)').text
    except NoSuchElementException:
        price_prov = item.find_element(By.CSS_SELECTOR,
                                       'div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > '
                                       'span:nth-child(1)').text
    except ValueError:
        price_prov = item.find_element(By.CSS_SELECTOR,
                                       'label:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child('
                                       '1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)').text

    try:
        price_decimals = item.find_element(By.CSS_SELECTOR,
                                           'label:nth-child(2) > div:nth-child(2) > div:nth-child(1) > '
                                           'div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > '
                                           'span:nth-child(2)').text
    except NoSuchElementException:
        price_decimals = item.find_element(By.CSS_SELECTOR,
                                           'div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > '
                                           'span:nth-child(2)').text
    except ValueError:
        price_decimals = item.find_element(By.CSS_SELECTOR,
                                           'label:nth-child(2) > div:nth-child(2) > div:nth-child(2) > '
                                           'div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > '
                                           'span:nth-child(2)').text

    if price_prov and price_decimals:  # Check if strings are non-empty
        price = "{:,}.{}".format(int(price_prov), int(price_decimals))
    elif price_prov:
        price = "{:,}".format(int(price_prov))
    else:
        price = 0

    print(flightnumber, departure_airport, arrival_airport, departure_time, arrival_time, price, airline)

    flight_info_list.extend([flightnumber, departure_airport, arrival_airport,
                             departure_time, arrival_time, price, airline])

    return flight_info_list


def store_info_on_db(cursor, flight_info_list, today, connection, driver):
    try:
        insert_query = "INSERT INTO prices (airline_iata, flight_number, departure_airport_iata, " \
                       "destination_airport_iata, departure_datetime, arrival_datetime, price_date_time, price) " \
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(flight_info_list[6],
                                                                                      flight_info_list[0],
                                                                                      flight_info_list[1],
                                                                                      flight_info_list[2],
                                                                                      flight_info_list[3],
                                                                                      flight_info_list[4],
                                                                                      today, flight_info_list[5])

        cursor.execute(insert_query)
        connection.commit()
        print('Price added')
    except Exception as e:
        print('Error occurred while storing price:', e)
        driver.save_screenshot(f"screenshot{today}.png")


def next_page(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
        nextday = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".vy-date-tabs-selector_wrap > li:nth-child(5)")))
        nextday.click()

        # Wait for the next day element to become stale
        WebDriverWait(driver, 10).until(EC.staleness_of(nextday))

        # Wait for the new page content to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".vy-date-tabs-selector_wrap > li:nth-child(5)")))

        return True  # Indicate successful navigation to the next page

    except TimeoutException as e:
        print("Timeout occurred while navigating to the next page:", e)
        # Perform actions to handle the timeout error, such as refreshing the page or retrying
        driver.refresh()
    except StaleElementReferenceException as e:
        print("StaleElementReferenceException occurred while navigating to the next page:", e)
        # Perform actions to handle the stale element error, such as finding the element again or waiting before
        # proceeding
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vy-date-tabs-selector_wrap > "
                                                                                     "li:nth-child(5)"))).click()
    except NoSuchElementException:
        driver.refresh()
    except Exception as e:
        print("Error occurred while navigating to the next page:", e)
        # Perform general error handling actions

    return False  # Indicate failure to navigate to the next page


def __main__():
    today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # Import settings
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    host_name = config.get('SQL DB', 'host_name')
    user_name = config.get('SQL DB', 'user')
    user_password = config.get('SQL DB', 'passwd')
    database = config.get('SQL DB', 'database')

    routes = config.get('OPTIONS', 'airports_of_interest').split(', ')
    base_airport = config.get('OPTIONS', 'base_airport')

    # Connect to database
    cnx, cursor = connect_to_sql_db(host_name, user_name, user_password, database)

    for city1 in routes:
        for city2 in routes:
            if (city1 != city2) and (city1 == base_airport or city2 == base_airport):
                print(f"Getting info on combination {city1} - {city2}")

                # Initialize the driver
                driver = configure_driver()

                # Go to the flights page
                go_to_page(driver, city1, city2, max_retries=3)

                # Loop through days
                for i in range(260):
                    flight_date_string, flightcards = get_day_info(driver)
                    for item in flightcards:
                        flight_info_list = get_flight_info(item, flight_date_string, driver)
                        # Store data in database
                        store_info_on_db(cursor, flight_info_list, today, cnx, driver)
                        # Click on the next day button
                    next_page(driver)
                    i += 1
                driver.close()

    print("All done")


__main__()
