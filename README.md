# CCS Regression with K-Means & SVR

This repository contains code and experiments for predicting ion-neutral collision cross sections (CCS) of small molecules via a clustering-plus-regression pipeline. We extend the paper:

Dylan H. Ross, Jang Ho Cho, and Libin Xu

Analytical Chemistry 2020 92 (6), 4548-4557

DOI: 10.1021/acs.analchem.9b05772

by coupling K-Means clustering with Support Vector Regression (SVR) and exploring feature variants such as polarization descriptors, MQNs, adducts, and data cleaning logic.

#### Forked From: https://github.com/dylanhross/c3sdb

---

## 🚀 Highlights

- **Clustering + Regression Pipeline**  
  1. **K-Means** groups molecules by structural similarity  
  2. **SVR** models trained per cluster for fine-grained CCS prediction  

- **Feature experiments**  
  - **MQNs** (Molecular Quantum Numbers)  
  - **Polarization** descriptors  
  - **Adduct-type** encoding  
  - **Data cleaning** logic vs. **uncleaned** raw data  

- **Key observations**  
  - Adding **polarization** features does not reduced test error.  
  - **Cleaned** datasets (filtered outliers & noisy spectra) does not improve SVR stability.  

---

## Deep Learning Extension
### https://github.com/ReubenSantoso/C3S-Neural-Network-Project
