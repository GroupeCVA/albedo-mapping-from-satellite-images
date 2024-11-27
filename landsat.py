import ee

# Définition de la fonction de masquage des nuages pour Landsat
def mask_landsat_clouds(image):
    """
    Masquage des nuages pour les images Landsat 7, 8 et 9

    Input:
    - image: image Landsat 7, 8 ou 9

    Output:
    - image: image Landsat 7, 8 ou 9 sans les nuages
    """
    # Masque de nuages pour Landsat 7, 8 et 9
    qa = image.select('QA_PIXEL')
    # Les bits 3 et 4 sont les nuages et les ombres
    mask = qa.bitwiseAnd(1 << 3).eq(0).And(qa.bitwiseAnd(1 << 4).eq(0))
    return image.updateMask(mask).int16()

# Fonction pour calculer l'albédo sur landsat 7
def compute_albedo_l7(image):
    """
    Calcul de l'albédo à partir des bandes de réflectance de Landsat 7

    Input:
    - image: image Landsat 7

    Output:
    - image: image Landsat 7 avec la bande d'albédo
    """
    b1 = image.select('SR_B1').multiply(2.75e-5).add(-0.2).multiply(0.204043872129643)
    b2 = image.select('SR_B2').multiply(2.75e-5).add(-0.2).multiply(0.14606731516826357)
    b3 = image.select('SR_B3').multiply(2.75e-5).add(-0.2).multiply(0.15029208676230038)
    b4 = image.select('SR_B4').multiply(2.75e-5).add(-0.2).multiply(0.3429313791748935)
    b5 = image.select('SR_B5').multiply(2.75e-5).add(-0.2).multiply(0.11565149702842839)
    b7 = image.select('SR_B7').multiply(2.75e-5).add(-0.2).multiply(0.041013849736471125)
    
    # Somme des bandes pondérées
    return b1.add(b2).add(b3).add(b4).add(b5).add(b7) \
        .set('system:time_start', image.get('system:time_start')) \
        .rename(['albedo'])

# Fonction pour calculer l'albédo sur landsat 8 et 9
def compute_albedo_l8_l9(image):
    """
    Calcul de l'albédo à partir des bandes de réflectance de Landsat 8 et 9
    
    Input:
    - image: image Landsat 8 ou 9
    
    Output:
    - image: image Landsat 8 ou 9 avec la bande d'albédo
    """
    b1 = image.select('SR_B1').multiply(2.75e-5).add(-0.2).multiply(0.09662203364296014)
    b2 = image.select('SR_B2').multiply(2.75e-5).add(-0.2).multiply(0.11052506872088694)
    b3 = image.select('SR_B3').multiply(2.75e-5).add(-0.2).multiply(0.13998546405536413)
    b4 = image.select('SR_B4').multiply(2.75e-5).add(-0.2).multiply(0.1963030623992841)
    b5 = image.select('SR_B5').multiply(2.75e-5).add(-0.2).multiply(0.29851100194879937)
    b6 = image.select('SR_B6').multiply(2.75e-5).add(-0.2).multiply(0.11703944343149952)
    b7 = image.select('SR_B7').multiply(2.75e-5).add(-0.2).multiply(0.04101392003087783)
    
    # Somme des bandes pondérées
    return b1.add(b2).add(b3).add(b4).add(b5).add(b6).add(b7) \
        .set('system:time_start', image.get('system:time_start')) \
        .rename(['albedo'])