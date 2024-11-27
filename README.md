# Introduction 
This project is about albedo computation from satellite images, multispectral (Sentinel-2, Landsat-8, Landsat-9) and hyperspectral (EnMAP, PRISMA) using surface reflectance as https://ieeexplore.ieee.org/document/8974188.

Albedo represents the proportion of sunlight that is reflected in a diffuse manner by an object. This measure plays a crucial role in photovoltaic panel applications.

<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/principe_biface_fond_blanc.jpg" />
</p>
<!-- ![Albedo and solar panels](https://github.com/group-cva/teledetection/blob/main/data/images/principe_biface_fond_blanc.jpg) -->

# Method

<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/weight_computation_fond_blanc.jpg" />
</p>
<!-- ![Weights computation](https://github.com/group-cva/teledetection/blob/main/data/images/weight_computation_fond_blanc.jpg) -->

In this formula, R is the at-surface solar radiation at wavelength. To have it we use SMARTS2 (Simple Model of the Atmospheric Radiative Transfer of Sunshine), which is an atmospheric model allowing us to specify conditions from any of 10 standard atmospheres (depending on location) and the season (summer/winter) in entry. The model gives at-surface spectral solar radiation at wavelength with a 0.5 nm spectral resolution for 280-400nm, 1 nm for 400-1750 nm and 10 nm for 1750-4000 nm. To have global albedo, we compute the coefficients for each band using the formula above. Finally, we sum the products of surface reflectance with coefficients as below.

<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/albedo_computation_fond_blanc.jpg" />
</p>
<!-- ![Albedo computation](https://github.com/group-cva/teledetection/blob/main/data/images/albedo_computation_fond_blanc.jpg) -->

# Example

You can see the [python notebook](https://github.com/group-cva/teledetection/blob/main/albedo.ipynb) as example to apply the algorithm on Sentinel-2 and Landsat 8-9 images, and to compute weights for EnMAP and PRISMA images. 

<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/albedo_s2.png" />
</p>
<!-- ![Albedo computed with Sentinel-2 images](https://github.com/group-cva/teledetection/blob/main/data/images/albedo_s2.png) -->

# Getting Started
### Installation process
Use pip to install requirements
```bash
pip install requirements.txt
```

# Results of QC on hyperspectral

According to https://ieeexplore.ieee.org/document/8974188, if we consider that the method works on Sentinel-2 images, we can compare those images to hyperspectral images.

<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/comparison_enmap_s2_first_image.png" />
</p>
<!-- ![Comparisons between EnMAP and S2](https://github.com/group-cva/teledetection/blob/main/data/images/comparison_enmap_s2_first_image.png) -->
<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/comparison_enmap_s2_second_image.png" />
</p>
<!-- ![Comparisons between EnMAP and S2](https://github.com/group-cva/teledetection/blob/main/data/images/comparison_enmap_s2_second_image.png) -->
<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/comparison_prisma_s2_2020.png" />
</p>
<!-- ![Comparisons between PRISMA and S2](https://github.com/group-cva/teledetection/blob/main/data/images/comparison_prisma_s2_2020.png) -->
<p align="center">
  <img src="https://github.com/group-cva/teledetection/blob/main/data/images/comparison_prisma_s2_2021.png" />
</p>
<!-- ![Comparisons between PRISMA and S2](https://github.com/group-cva/teledetection/blob/main/data/images/comparison_prisma_s2_2021.png) -->

# Questions
If you have any questions, feel free to send an email at teledetection@cva-engineering.com.