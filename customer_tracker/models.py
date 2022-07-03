from django.db import models
import re

# Create your models here.

class Customer(models.Model):
    first_name    = models.CharField(max_length=200) 
    last_name     =  models.CharField(max_length=200) 
    address       =  models.CharField(max_length=200) 
    city          = models.CharField(max_length=200) 
    zip_code      = models.CharField(max_length=9) 
    state_code    =  models.CharField(max_length=2) 

    # Translate States Dict
    valid_states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    def __str__(self):
        """
        Override str method provide last , first as a standard print
        """
        return(str(self.last_name) + ', ' + str(self.first_name))

    def check_zip(self) -> bool:
        """
        Checks zip code for standard us format
        """
        return bool(re.match('^([0-9]{5})(?:[-][0-9]{4})?$', self.zip_code))

    def check_states(self) -> bool:
        """
        Design around 2 digit state in a drop down check that we are only getting a valid one
        """
        return bool(self.state_code in self.valid_states)

    def translate_state(self) -> str:
        """
        Pull back the long text for a 2 digit state code if needed
        """
        return valid_states[self.state_code]

    def validate_customer(self):
        """
        Returns an exception when the customer is not valid pre save
        Checks all fields populated
        Checks zip code is valid format
        Checks state is a valid US state
        """
        if ( self.first_name is  None or
             self.last_name is None or
             self.address is None or
             self.city is None or
             self.zip_code is None or
             self.state_code is None  or 
             self.check_zip() == False or
             self.check_states() == False
            ):
            raise ValidationError(
                {'Customer': "The customer was missing fields or had invalid location data"}) 

    
    def save(self, *args, **kwargs):
        """
        Override save method and stack the validation ahead of save
        """
        self.validate_customer()
        return super().save(*args, **kwargs)
