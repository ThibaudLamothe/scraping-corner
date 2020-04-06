import json
import time
import logzero
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from logzero import logger

def get_identifiants(path):
    with open(path, 'r') as pfile:
        credentials = json.load(pfile)
    sncf = credentials['SNCF']
    return sncf['user'], sncf['password'], sncf['prenom']        

class BookSNCF():

    def __init__(self, user, password, prenom, path='/Users/thibaud/Downloads/chromedriver'):
        self.driver = webdriver.Chrome(path)
        self.url = 'https://www.oui.sncf/'
        self.user = user
        self.prenom_sncf = prenom
        self.password = password
        self.original_window = None
        
    def close_driver(self):
        logger.warning('Exit navigation.')
        self.driver.quit()
    
    def scroll_to_element(self, elmt):
        y = elmt.location['y']
        logger.debug('scrolling to y={}'.format(y))
        y = y -150
        self.driver.execute_script("window.scrollTo(0, {})".format(y))
        logger.debug('Wait 1s') ; time.sleep(0.7)

    def get_url(self):
        logger.warning('Connect to desired application')
        logger.debug(self.url)

        self.driver.get(self.url)
        self.original_window =  self.driver.window_handles[0]
        logger.debug('Wait 7s') ; time.sleep(7.14)


    def login(self):
        logger.warning('Start login procedure')

        # Click connect
        logger.info('Click on connect button')
        btn = self.driver.find_element_by_link_text('Me connecter')
        btn.click()
        logger.debug('Wait 5s') ; time.sleep(5.1) 

        # Give mail
        logger.info('Add email adress')
        sbox = self.driver.find_element_by_id('ccl-email')
        sbox.send_keys(self.user)
        sbox.send_keys(Keys.ENTER)
        logger.debug('Wait 9s') ;  time.sleep(9.3)

        # Start second window interaction
        logger.info('Go to opened window')
        new_window = self.driver.window_handles[1]
        self.driver.switch_to_window(new_window)

        # Give password
        logger.info('Write password')
        sbox = self.driver.find_element_by_id('password')
        sbox.send_keys(self.password[::-1])
        logger.debug('Wait 2s') ; time.sleep(1.9)

        # Validate
        logger.info('Click on validation button')
        btn = self.driver.find_elements_by_class_name('input_row')
        bt = btn[-1]
        bt.click()
        logger.debug('Wait 11s') ;  time.sleep(11.1)

        # Get back to inital page
        logger.info('Get Back to main page')
        self.driver.switch_to_window(self.original_window)
        time.sleep(1)

    def check_login(self):
        test = self.driver.find_elements_by_class_name('first-name')
        if len(test) > 0:
            if self.prenom_sncf.lower() in test[0].text.lower():
                logger.error('Welcome {}'.format(self.prenom_sncf))
                return True
        return False

    def make_search(self, origin='Paris', destination='Bordeaux', jour='08', mois='04', annee='2020'):
        logger.warning('Realize research according to selected parameters')
        
        
        # Select origin
        logger.info('From {}'.format(origin))
        searchbox = self.driver.find_element_by_id('vsb-origin-train-launch')
        searchbox.clear()
        logger.debug('Wait 1s') ; time.sleep(1.1)
        searchbox.send_keys(origin)
        logger.debug('Wait 3s') ; time.sleep(3.3) 
        searchbox.send_keys(Keys.ENTER)
        
        # Select destination
        logger.info('To {}'.format(destination))
        searchbox2 = self.driver.find_element_by_id('vsb-destination-train-launch')
        searchbox2.clear()
        logger.debug('Wait 1s') ; time.sleep(1.2)
        searchbox2.send_keys(destination)
        logger.debug('Wait 3s') ; time.sleep(2.7)
        searchbox2.send_keys(Keys.ENTER)
        
        # Select date
        id_ = 'train-launch-d-{}-{}-{}'.format(jour, mois, annee)
        logger.info('Date {}'.format(id_))
        logger.info('- Open date selector')
        date = self.driver.find_element_by_id('vsb-dates-dialog-train-launch-aller-retour-1')
        date.click()
        logger.debug('Wait 4s') ; time.sleep(4.23)
        # previous_month = self.driver.find_element_by_id('previousMonth')
        # next_month = self.driver.find_element_by_id('nextMonth')
        logger.info('- Select choosen date')
        date_selected = self.driver.find_element_by_id(id_)
        date_selected.click()
        logger.debug('Wait 2s') ; time.sleep(1.95)
        # Eventuall select hour
        logger.info('- Validate date')
        button =  self.driver.find_element_by_id('vsb-datepicker-train-launch-aller-retour-submit')
        button.click()
        logger.debug('Wait 4s') ; time.sleep(4.1)


        # Validate research
        logger.info('Validate research')
        btn = self.driver.find_element_by_id('vsb-booking-train-launch-submit')
        btn.click()
        logger.debug('Wait 15s') ; time.sleep(15)
    
    def trajets_suivants(self):
        logger.warning('> Affichage des trajets suivants')
        button = self.driver.find_elements_by_xpath('//span[@data-auto="LINK_TRAVEL_NEXT_HOUR"]')
        if len(button)==1:
            logger.debug(button[0])
            self.scroll_to_element(button[0])
            button = self.driver.find_elements_by_xpath('//span[@data-auto="LINK_TRAVEL_NEXT_HOUR"]')
            button[0].click()
            logger.debug('Wait 2s') ; time.sleep(2.3)
        else:
            logger.error('Pas possible voyage suivant')
            # verifier jour suivnat


    def select_train(self, horaire_souhaite='15:52'):
        logger.warning('Select train : {}'.format(horaire_souhaite))

        tgvmax_signature = ['meilleur', 'prix', '0', '€', '0,00', '€']

        ##########################
        # Get list of existing trains
        logger.info('>>> Extract list of trains')
        list_of_trains = self.driver.find_elements_by_xpath('//button[@data-auto="BTN_TRAVEL_SUMMARY"]')
        #print([i.location for i in list_of_trains])
        logger.info(' - Found total : ', len(list_of_trains))

        # Get list of boughtable trains
        list_of_prices = self.driver.find_elements_by_xpath('//button[@data-auto="BTN_PRICEBTN_SECOND"]')
        logger.info(' - Found to buy : ', len(list_of_prices))

        # Keep list of tgvmax
        list_of_tgvmax = [i for i in list_of_prices if i.text.split()==tgvmax_signature]
        y_buttons = [i.location['y'] for i in list_of_tgvmax]
        # print([i.location for i in list_of_tgvmax])
        logger.info(' - Found TGVMax : ', len(list_of_tgvmax))

        # Keep train tgvmax
        travel_2_keep = []
        for train in list_of_trains:
            if train.location['y'] in y_buttons:
                travel_2_keep.append(train)
        logger.info('>>> TGVMAX POWER:')
        _ = [logger.debug((i.location, i.text.split())) for i in travel_2_keep]

        # Check if horaire is available
        for travel in travel_2_keep:
            if horaire_souhaite in travel.text:
                wanted_button = travel
        logger.info('Train found')
        ##########################
        
        # If horaire is ok
        logger.info('Click on selected train')
        self.scroll_to_element(wanted_button)





        ##########################
        # Get list of existing trains
        logger.info('>>> Extract list of trains')
        list_of_trains = self.driver.find_elements_by_xpath('//button[@data-auto="BTN_TRAVEL_SUMMARY"]')
        #print([i.location for i in list_of_trains])
        logger.info(' - Found total : ', len(list_of_trains))

        # Get list of boughtable trains
        list_of_prices = self.driver.find_elements_by_xpath('//button[@data-auto="BTN_PRICEBTN_SECOND"]')
        logger.info(' - Found to buy : ', len(list_of_prices))

        # Keep list of tgvmax
        list_of_tgvmax = [i for i in list_of_prices if i.text.split()==tgvmax_signature]
        y_buttons = [i.location['y'] for i in list_of_tgvmax]
        # print([i.location for i in list_of_tgvmax])
        logger.info(' - Found TGVMax : ', len(list_of_tgvmax))

        # Keep train tgvmax
        travel_2_keep = []
        for train in list_of_trains:
            if train.location['y'] in y_buttons:
                travel_2_keep.append(train)
        logger.info('>>> TGVMAX POWER:')
        _ = [logger.debug((i.location, i.text.split())) for i in travel_2_keep]

        # Check if horaire is available
        for travel in travel_2_keep:
            if horaire_souhaite in travel.text:
                wanted_button = travel
        logger.info('Train found')
        ##########################



        wanted_button.click()
        logger.debug('Wait 7s') ; time.sleep(6.7)

    def select_aller(self):
        logger.warning('Selection step')
        selecter = self.driver.find_elements_by_xpath('//button[@data-auto="BTN_SELECT_TRAVEL"]')
        if len(selecter)!=1:
            logger.error('ERRRRROOOOOOOR  : multiple buttons')
        else:
            select_train = selecter[0]
            select_train.click()
            logger.debug('Wait 9s') ; time.sleep(8.6)


    def valid_aller(self, ma_salle=None, mon_siege=None):
        logger.warning('Validation step')
        # Eventually select haut/bas

        # Eventually select fenetre/coulaire

        # Attention mettre un garde fou pour valider que les billets dont on est sur qu'ils sontà 0€
        valid_train = self.driver.find_element_by_xpath('//button[@data-auto="BTN_SEATING_VALIDATE"]')
        valid_train.click()
        logger.debug('Wait 10s') ; time.sleep(10)

        # Changement de page auto (go to panier)
        print(self.driver.current_url)


    
    def confirm_basket(self):
        logger.warning('Basket confirmation')
        logger.info(self.driver.current_url)

        # reject assurance
        logger.info('Rejecting assurance')
        label_assurance = self.driver.find_elements_by_xpath('//label[@for="ASSURANCE_VOYAGE_CHOICE_0_NO"]')
         #.find_element_by_css_selector('> span.radio-button')
        if len(label_assurance)==1:
            radio = label_assurance[0]
            logger.info('Moving to radio')
            
            self.scroll_to_element(radio)
            label_assurance = self.driver.find_elements_by_xpath('//label[@for="ASSURANCE_VOYAGE_CHOICE_0_NO"]')
            radio = label_assurance[0]

            logger.info('Clicking to radio')
            radio.click()
            logger.debug('Wait 2s') ; time.sleep(2)
            logger.info('Assurance rejected')

            logger.info('Moving to Basket valiation')
            final_validation = self.driver.find_elements_by_xpath('//input[@name="action:CmdValidBasket"]')
            
            if len(final_validation)==1:

                self.scroll_to_element(final_validation[0])
                final_validation = self.driver.find_elements_by_xpath('//input[@name="action:CmdValidBasket"]')
            
                logger.info('Clicking on Basket valiation')

                final_validation[0].click()
                logger.debug('Wait 10s') ; time.sleep(10)

            else:
                logger.error('Final validation button bug')
        else:
            logger.error('Found multiple radio button => be sure not to choose assurance.')

    def booking_confirmation(self):
        logger.warning('Last step : Booking conformation')
        final_validation = self.driver.find_elements_by_xpath('//div[@class="vsf-form__button"]//button[contains(@class,"oui-button")]')
        print(len(final_validation))

        if final_validation[0].text =='Valider ma commande (0 €)':
            logger.info(final_validation[0].text)
            btn = final_validation[0]
            logger.info('Moving to button')
            
            self.scroll_to_element(btn)
            final_validation = self.driver.find_elements_by_xpath('//div[@class="vsf-form__button"]//button[contains(@class,"oui-button")]')
            btn = final_validation[0]

            logger.info('Clicking on button')
            btn.click()
            logger.debug('Wait 7s') ; time.sleep(7.3)  

    def consult_command(self):
        logger.error('Command done : Going to ticket page')
        
        buttons = self.driver.find_elements_by_css_selector('oui-button > button')
        if len(buttons)==1:
            # self.scroll_to_element(buttons[0])
            buttons[0].click()
        else:
            logger.error('Multiple buttons : dont know where to click')



if __name__ == "__main__":
    # from book_sncf import BookSNCF
    
    # Collect identifiers
    rep = get_identifiants('credentials.json')
    user, password, prenom = rep
    
    # Instanciate object and lof to website
    bs = BookSNCF(user, password, prenom)
    bs.get_url()
    bs.login()
    is_logged = bs.check_login()

    # Make reservation
    if is_logged:
        logger.info('Correctly logged')
        bs.make_search(origin='Bordeaux', destination='Paris', jour='25', mois='03', annee='2020')
        bs.trajets_suivants()
        bs.select_train('8:04')
        bs.select_aller()
        bs.valid_aller(ma_salle=None, mon_siege=None)
        bs.confirm_basket()
        bs.booking_confirmation()
        bs.consult_command()
    else:
        logger.error('NOT LOGED IN')
    
    # Close instance
    bs.close_driver()