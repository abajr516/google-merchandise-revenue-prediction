# Data
### Source
Learn more about the data [here](https://www.kaggle.com/competitions/ga-customer-revenue-prediction/data)

### Download the Dataset
The raw dataset is not included in this repository because of its large file size.

Authenticate with your Kaggle account:
```bash
kaggle auth login
```
Follow the browser-based authentication steps, then run the data setup script:
```bash
python scripts/download_data.py
```
The script checks available storage, downloads and extracts the datasets, verifies the files, and removes the temporary ZIPs.