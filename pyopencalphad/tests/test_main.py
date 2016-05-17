import numpy as np
import libocpy as pyoc

phase_names_test = ['AL12W', 'AL13CO4', 'AL2W', 'AL3CO', 'AL3NI1',
                    'AL3NI2', 'AL3NI5', 'AL3RU2', 'AL4W', 'AL5CO2', 'AL5W', 'AL77W23',
                    'AL7W3', 'AL9CO2', 'ALM3_D019', 'ALTI', 'BCC_B2', 'C14_LAVES',
                    'C15_LAVES', 'C16_MXTA2', 'C36_LAVES', 'CHI', 'CO7TA2', 'DO22', 'DOA',
                    'EPSILON_L', 'ETA_AL2TI', 'HCP_A3', 'KAPPA', 'L12_FCC', 'LIQUID',
                    'MU', 'NI2TA', 'NI3TI', 'NI4W', 'NITI2', 'NIW', 'NIW2', 'O_ALTATI2',
                    'PHI_ALTA', 'PT3TA', 'SIGMA', 'ZETA_AL5TI2']

phases_equil_dict = {'C14_LAVES': 0.0, 'NI3TI': 0.0, 'DO22': 0.0, 'HCP_A3': 0.0, 'DOA': 0.0, 'O_ALTATI2': 0.0, 'AL3RU2': 0.0, 'NI4W': 0.0, 'AL5W': 0.0, 'SIGMA': 0.0, 'L12_FCC': 0.0, 'CO7TA2': 0.0, 'LIQUID': 0.0, 'AL3NI1': 0.0, 'AL3NI2': 0.0, 'AL3NI5': 0.0, 'BCC_B2': 0.1014584445747258, 'AL13CO4': 0.0, 'EPSILON_L': 0.0, 'PT3TA': 0.0, 'AL7W3': 0.0, 'AL5CO2': 0.0, 'AL3CO': 0.0, 'KAPPA': 0.0, 'CHI': 0.0, 'NI2TA': 0.0, 'NIW2': 0.0, 'NITI2': 0.0, 'AL2W': 0.0, 'PHI_ALTA': 0.0, 'AL4W': 0.0, 'BCC_B2_AUTO#3': 0.0, 'BCC_B2_AUTO#2': 0.89854155542527414, 'ETA_AL2TI': 0.0, 'AL12W': 0.0, 'ALTI': 0.0, 'AL9CO2': 0.0, 'ALM3_D019': 0.0, 'AL77W23': 0.0, 'ZETA_AL5TI2': 0.0, 'NIW': 0.0, 'MU': 0.0, 'C15_LAVES': 0.0, 'C16_MXTA2': 0.0, 'C36_LAVES': 0.0}

phase_fractions_fcc_test = [0.26675020237180319, 0.2695837201374871,
                            0.27233510967799979, 0.27497961780949498,
                            0.14999809482541621, 0.27986689732531289,
                            0.14999569861892356, 0.28412192440195072,
                            0.14999058356846937, 0.14998621534373788,
                            0.28921941517683836, 0.29059433117395173,
                            0.29183298979013106, 0.29296261634652415,
                            0.29402059900877858, 0.29505742704647608,
                            0.29614145454678698, 0.29736693097169248,
                            0.29886825014467733, 0.30084693553197017,
                            0.30362729056195775, 0.30778506458753119,
                            0.31449351996042846, 0.3266208609464597,
                            0.35118441507036369, 0.3872403322676054,
                            0.4205087831746972, 0.45076361518351499,
                            0.4801648431474369, 0.5100983284613495,
                            0.91226128356372871, 0.12402511915394167,
                            0.61279477884258093, 0.12020305273699453,
                            0.11831035656191249, 0.11656687493363968,
                            0.11495473534346042, 0.11345921260503246,
                            0.11206789019299096, 0.11077024692080557,
                            0.10955728491530409, 0.10842125069001407,
                            0.10735546515947272, 0.10635413986504474,
                            0.10541223016817101, 0.1045253588559842,
                            0.10368968778558225, 0.1029018725602487,
                            0.10215898413460409, 0.1014584445747258]

def test_co_ni_al_w():
    """Primary test case for pyopencalphad.

    This test case calculates a cobolt, nickel, aluminium, tungsten
    system using pyopencalphad.

    """
    pyoc.tqini()
    pyoc.tqrpfil('database/Co_Chimad.TDB',('CO','NI','AL','W'))

    element_names = pyoc.tqgcom()

    assert element_names == ['AL', 'CO', 'NI', 'W']

    phase_names_actual = pyoc.tqgpn()

    assert phase_names_actual == phase_names_test

    ## calc using method 1
    pyoc.tqsetc('N',0,1.)
    pyoc.tqsetc('P',0,1E5)
    pyoc.tqsetc('T',0,900)
    pyoc.tqsetc('X','NI',0.1)
    pyoc.tqsetc('X','AL',0.12)
    pyoc.tqsetc('X','W',0.15)
    pyoc.tqce()
    phase_names_equil_method1 = pyoc.tqgpn()

    ## calc using method 2
    pyoc.tqsetcs({'T':900,'P':1E5,'N':1.,'X(NI)':0.1,'X(AL)':0.12,'X(W)':0.15})
    pyoc.tqce()
    phase_names_equil_method2 = pyoc.tqgpn()

    ## test both methods
    for phase_names_equil in phase_names_equil_method1, phase_names_equil_method2:
        phase_fractions = [pyoc.tqgetv('NP', phase_name, 'NA') for phase_name in phase_names_equil]
        assert dict(zip(phase_names_equil, phase_fractions)) == phases_equil_dict

    pyoc.tqphsts("*","SUS",0.)
    pyoc.tqphsts("BCC","ENT",1.)
    pyoc.tqphsts("L12","ENT",1.)

    def calc_phase_fraction(temperature):
        pyoc.tqsetc('T', 0, temperature)
        pyoc.tqce()
        return pyoc.tqgetv('NP','BCC','NA')

    phase_fractions_fcc_actual = [calc_phase_fraction(temperature) \
                                 for temperature in np.linspace(500, 1500, 50)]

    assert phase_fractions_fcc_test == phase_fractions_fcc_actual
