import numpy as np
from numpy import array, zeros, ones, full
import scipy as sp
from wood_properties import WoodProperty
from charges import Charges
from math import sin, pi, cos
from chevron import Chevron

# Coefficient de securité (9.1 p29)
K_S = 2.75


def main():


    c18 = WoodProperty(
        18,
        11,
        0.5,
        18,
        2.2,
        2.0,
        9.0,
        6.0,
        0.30,
        0.56,
        320.0,
        380.0,
    )

    gamma_m = 1.3 # bois massif
    k_mod = 0.9 # charge court terme

    correction = k_mod/gamma_m

    # Charges permanentes
    g = Charges()
    g['tuiles'] = 0.50
    g['ba13'] = 0.10
    g['laine_de_verre'] = 0.6
    g['litonnage'] = 0.03
    g['contre_litonnage'] = 0.03
    g['chevrons'] = 0.1
    g['hpv'] = 0.0015
    print('charge_exploitation',g.calcul_charge_totales())
    G = g.calcul_charge_totales()


    s_k = 0.45
    s_ad = 1.0
    mu_i = 0.8

    # Coefficient de forme = 1
    c_e = 1

    charge_neige = mu_i*c_e*s_k
    Q = charge_neige
    print('charges neige', charge_neige)

    c_elu = 1.35*g.calcul_charge_totales() + 1.5*charge_neige
    print('Combinaison ELU', c_elu)

    L = 3200/cos(25.*pi/180.)
    print('L [mm]', L)
    chevron = Chevron(50., 220., L)
    print('')

    # calcul_traction
    N = c_elu*sin(25.*pi/180.)*L
    print('N [Newton]', N)
    sigma_t_0_d = N/chevron.calcul_section()
    print('sigma_t_0_d', sigma_t_0_d)

    # Calcul resistance traction axiale
    k_h = 1.
    f_t_0_d = c18.f_t_0_k*k_mod/gamma_m*k_h
    print('f_t_0_d [MPa]', f_t_0_d)

    print('')
    # Calcul contrainte flexion
    q_z = c_elu*cos(25.*pi/180)
    print('q_z [N/mm2]', q_z)

    moment_flexion = q_z*L**2/8.
    sigma_m_d = moment_flexion/chevron.calcul_module_intertie()
    print('sigma_m_d [MPa]', sigma_m_d)

    k_sys = 1.1 # Coefficient effet systeme
    f_m_d = c18.f_m_k * k_mod/gamma_m * k_sys * k_h
    print('f_m_d [MPa]', f_m_d)
    print()

    taux_travail = sigma_t_0_d/f_t_0_d + sigma_m_d/f_m_d
    print('taux de travail total', taux_travail)

    # calcul fleche instantanée
    q_inst = charge_neige*cos(25.0*pi/180.) * 0.6
    print('q_inst [N/mm]', q_inst)
    print('')


    W_inst = 5.0*q_inst*L**4/(384.*c18.e_0_mean*1000*chevron.calcul_moment_inertie())
    w_inst_lim = L/300.
    crit_inst_lim = W_inst/w_inst_lim
    print('W_inst [mm]', W_inst)
    print('crit_inst_lim', crit_inst_lim)
    print('')

    k_def = 0.8 # coefficient de deformation (classe 2 bois brut)
    phi_2 = 0. # Simultaneite vent nmeige

    w_net_fin = W_inst*(1+(k_def*(G+phi_2*Q)+G)/Q)
    w_net_fim_lim = L/200.
    crit_fin_lim = w_net_fin/w_net_fim_lim
    print('w_net_fin [mm]', w_net_fin)
    print('crit_fint_lim', crit_fin_lim)


if __name__ == "__main__":
    main()