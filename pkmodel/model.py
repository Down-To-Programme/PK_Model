#
# Model class
#

class Model:
    """A Pharmokinetic (PK) model
    Parameters
    ----------

    value: numeric, optional
        an example paramter

    Vc: float
        central compartment volume
    Vps: list of floats
        list of volumes of peripheral compartments
    Qps: list of floats
        list of transition rates between central compartment
        and peripheral compartments

    """
    def __init__(self, Vc, Vps, Qps, CL):
        self.__compartments = []
        self.__central_volume = Vc
        self.__n_compartments = 1  # nb Includes central compartment
        self.__CL = CL
        for Vp, Qp in zip(Vps, Qps):
            self.add_compartment(Vp, Qp)

    def add_compartment(self, Vp=1, Qp=1):
        """
        Add a peripheral compartment to the model.
        """
        self.__n_compartments += 1
        self.__compartments.append({'Vp': Vp, 'Qp': Qp})

    @property
    def Vps(self):
        """
        Volumes of the peripheral compartments.
        """
        return [elem['Vp'] for elem in self.__compartments]

    @property
    def Qps(self):
        """
        Transition rates between central compartment
        and peripheral compartments.
        """
        return [elem['Qp'] for elem in self.__compartments]

    @property
    def Vc(self):
        """
        Volume of the central compartment.
        """
        return self.__central_volume

    @property
    def size(self):
        """
        Returns the number of peripheral compartments.
        """
        return self.__n_compartments

    @property
    def CL(self):
        """
        Returns the clearance/elimination rate from the central compartment.
        """
        return self.__CL
