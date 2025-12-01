import pandas as pd
from scipy import integrate as intg
import ee

def coefficients_calculation(bands_list, irradiance_file, min_spectrum, max_spectrum):
    """
    Coefficients computation for albedo using bands limits and the spectral solar irradiance file.
    
    Input:
    - bands_list: list of tuples containing bands limits 
    - irradiance_file: file containing spectral solar irradiance at wavelengths result of SMARTS model
    - min_spectrum: minimum wavelength of the spectrum
    - max_spectrum: maximum wavelength of the spectrum
    
    Output:
    - coefficients: list of coefficients for the computation of the albedo band

    Example:
    - Use case in albedo.ipynb (Coefficients computation part)
    """
    df = pd.read_csv(irradiance_file)
    df = df[['Wvlgth', 'Direct_normal_irradiance']]
    df.columns = ['wavelength', 'SSI']
    coefficients = []
    
    for bands in bands_list:
        # band[0] : lower wavelength of a band in nm
        # band[1] : upper wavelength of a band in nm
        df_band = df[(df['wavelength'] >= bands[0]) & (df['wavelength'] <= bands[1])]
        df_spectrum = df[(df['wavelength'] >= min_spectrum) & (df['wavelength'] <= max_spectrum)]

        x_numerator = df_band['wavelength'].to_list()
        y_numerator = df_band['SSI'].to_list()
        
        x_denominator = df_spectrum['wavelength'].to_list()
        y_denominator = df_spectrum['SSI'].to_list()

        integral_numerator = intg.trapezoid(y_numerator, x_numerator)
        integral_denominator = intg.trapezoid(y_denominator, x_denominator)

        coefficient = integral_numerator / integral_denominator

        coefficients.append(coefficient)
    return coefficients

def get_stats(image_collection, 
              date, 
              zone,
              scale,
              mean=False, 
              variance=False, 
              median=False, 
              min=False, 
              max=False):
    """
    Get the stats of an image collection at a specific date.

    Input:
    - image_collection: image collection to get the stats from
    - date: date to get the stats from
    - zone: zone to clip the image
    - scale: scale of the image
    - mean: boolean to get the mean of the image
    - variance: boolean to get the variance of the image
    - median: boolean to get the median of the image
    - min: boolean to get the min of the image
    - max: boolean to get the max of the image

    Output:
    - stats_to_return: dictionary containing the stats of the image
    """
    date_p1 = ee.Date(date).advance(1, 'day').format('YYYY-MM-dd').getInfo()
    image_at_date = image_collection.filterDate(date, date_p1).mosaic().clip(zone)
    # get stats
    stats = image_at_date.reduceRegion(
        reducer=ee.Reducer.mean().combine(
            reducer2=ee.Reducer.variance().combine(
                reducer2=ee.Reducer.median().combine(
                    reducer2=ee.Reducer.min().combine(
                        reducer2=ee.Reducer.max(),
                        sharedInputs=True
                    ),
                    sharedInputs=True
                ),
                sharedInputs=True
            ),
            sharedInputs=True
        ),
        geometry=zone,
        scale=scale
    )
    bands_names = image_at_date.bandNames().getInfo()
    # return stats defined as true
    stats_to_return = {}
    for band_name in bands_names:
        if mean:
            stats_to_return[str(band_name) + '_mean'] = stats.getInfo()[str(band_name) + '_mean']
        if variance:
            stats_to_return[str(band_name) + '_variance'] = stats.getInfo()[str(band_name) + '_variance']
        if median:
            stats_to_return[str(band_name) + '_median'] = stats.getInfo()[str(band_name) + '_median']
        if min:
            stats_to_return[str(band_name) + '_min'] = stats.getInfo()[str(band_name) + '_min']
        if max:
            stats_to_return[str(band_name) + '_max'] = stats.getInfo()[str(band_name) + '_max']
    return stats_to_return

def resample_image(image, projection):
    """
    Reduce the resolution of an image to match input resolution

    Input :
    - image: ee.Image
    - projection: ee.Projection

    Output :
    - resampled_sentinel, ee.Image
    """
    resampled_image = image.reproject(
        crs=projection,
    ).reduceResolution(
        reducer=ee.Reducer.mean(),  
    )
    return resampled_image

def compute_albedo_enmap(image):
    '''
    Compute coefficients for EnMAP satellite
    
    Input:
    - image: EnMAP image
    
    Output:
    - albedo for each pixel of an EnMAP image
    '''
    df_enmap = pd.read_csv("data/enmap_bands_coeff.csv")
    albedo = ee.Image.constant(0) 
    # TODO remplacer par un apply()
    for index, row in df_enmap.iterrows():
        band = image.select('b' + str(int(row['BAND #'])))
        band = band.multiply(1e-4).multiply(row['coeff'])
        if not((int(row['BAND #']) >= 130) and (int(row['BAND #']) <= 135)) and (int(row['BAND #']) != 164):
            albedo = albedo.add(band)

    albedo = albedo.select([0])
    return albedo.set('system:time_start', image.get('system:time_start')).rename(['albedo'])

def compute_albedo_prisma(image, bands_to_exclude, summer=True):
    '''
    Compute coefficients for PRISMA image
    
    Input:
    - image: PRISMA image
    - bands_to_exclude: Bands with no values or fex pixels
    - summer: boolean (True if it's summer)
    
    Output:
    - albedo for each pixel of a PRISMA image
    '''
    if summer:
        csv_path = "data/prisma_bands_coeff_summer.csv"
    else:
        csv_path = "data/prisma_bands_coeff_winter.csv"
    df_prisma = pd.read_csv(csv_path)
    albedo = ee.Image.constant(0) 
    # TODO remplacer par un apply()
    for index, row in df_prisma.iterrows():
        band_name = 'b' + str(int(row['BAND #']))
        if band_name not in bands_to_exclude:
            band = image.select(band_name)
            band = band.multiply(row['coeff'])
            albedo = albedo.add(band)

    albedo = albedo.select([0])
    return albedo.set('system:time_start', image.get('system:time_start')).rename(['albedo'])
