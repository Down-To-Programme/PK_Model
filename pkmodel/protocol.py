#
# Protocol class
#

class Protocol:
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self):
        self.subcutaneous = False
        self.k_a = 0
        self.dose_amount = 0
        self.continuous = False
        self.contionous_period = [0, 0]
        self.dose_times = []
        

    def dose(self, dose_amount):
        self.dose_amount = dose_amount
        return dose_amount

    def make_subcutaneous(self, k_a):
            self.k_a = k_a 
            self.subcutaneous = True

    def make_continuous(self, time_added, time_removed):
        self.continuous = True
        self.contionous_period[0] = time_added
        self.contionous_period[1] = time_removed
    
    def add_dose_time(self, time):
        self.dose_times.append(time)
        self.dose_times.sort()


