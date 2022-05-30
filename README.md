# aqdata
## Machine Learning Estimation Service for Indoor Air Quality Index
---
this is a python based machine learning (ML) service for estimating indoor air quality (IAQ) with the following parameters provided by IoT sensors:
- CO2 - Carbon Dioxide in ppm
- VOC - Volatile Organic Compounds in μg/m³
- RH - Relative Humidity in %
- TEM - Temperature in 'C
- PM25 - PM2.5 particles in μg/m³

An integer score shall be returned upon request after calculation on a scale of **1 to 13**, with a larger number indicating a less desirable condition of IAQ.

There are 3 major sections, or modules in this system, namely:
1. IAQ historial data retrival and preparation
2. ML with Deep Neural Network and modelling
3. Estimation request and network interfaces

---
