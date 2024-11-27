import ee

# Définition de la fonction de masquage des nuages pour Sentinel-2
def mask_s2_clouds(image):
    '''
    Filter images with too much clouds
    
    Input:
    - image: ee.Image
    
    Output:
    - Image if there is not too much clouds
    '''
    qa = image.select('QA60')
    # Les bits 10 et 11 représentent respectivement les nuages et les cirrus.
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    # Les deux indicateurs doivent être à zéro, indiquant des conditions claires.
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    return image.updateMask(mask).int16()

# Fonction pour calculer l'albédo
def compute_albedo(image):
    '''
    Compute albedo of each pixel for an image
    
    Input:
    - image: ee.Image
    
    Output:
    - Image with albedo band
    '''
    b2w2 = image.select('B2').multiply(0.22605081620173895e-4)
    b3w3 = image.select('B3').multiply(0.12513826634639683e-4)
    b4w4 = image.select('B4').multiply(0.15804816263810165e-4)
    b8w8 = image.select('B8').multiply(0.3408016673127353e-4)
    b11w11 = image.select('B11').multiply(0.11601772668271282e-4)
    b12w12 = image.select('B12').multiply(0.03394336081831444e-4)
    
    # Somme des bandes pondérées
    return b2w2.add(b3w3).add(b4w4).add(b8w8).add(b11w11).add(b12w12) \
        .set('system:time_start', image.get('system:time_start')) \
        .rename(['albedo'])