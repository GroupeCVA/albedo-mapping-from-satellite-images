# Introduction 
This project is about albedo computation from satellite images, multispectral (Sentinel-2, Landsat-8, Landsat-9) and hyperspectral (EnMAP, PRISMA) using surface reflectance as https://ieeexplore.ieee.org/document/8974188.

Albedo represents the proportion of sunlight that is reflected in a diffuse manner by an object. This measure plays a crucial role in photovoltaic panel applications.
### image example of albedo with solar panels
![Albedo illustration](https://github.com/user/repo_name/blob/branch/image.png)
![Albedo computed with Sentinel-2 images](https://github.com/user/repo_name/blob/branch/image.png)

# Brieve presentation of the method with images of formula

![Coefficient computation](https://github.com/user/repo_name/blob/branch/im.png)

In this calculation, R is the at-surface solar radiation at wavelength. To have it we use SMARTS2 (Simple Model of the Atmospheric Radiative Transfer of Sunshine), which is an atmospheric model allowing us to specify conditions from any of 10 standard atmospheres (depending on location) and the season (summer/winter) in entry. The model gives at-surface spectral solar radiation at wavelength with a 0.5 nm spectral resolution for 280-400nm, 1 nm for 400-1750 nm and 10 nm for 1750-4000 nm. To have global albedo, we calculate the coefficients for each band using the formula above. Finally, we sum the products of surface reflectance with coefficients.

![Albedo computed with Sentinel-2 images](https://github.com/user/repo_name/blob/branch/image.png)

# Getting Started
### Installation process
Use pip to install requirements
```bash
pip install requirements.txt
```

# Results of QC

# Questions
If you have any questions, feel free to send me an email at teledetection@cva-engineering.com