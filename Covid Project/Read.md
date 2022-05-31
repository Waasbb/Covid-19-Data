# Covid-19-Data

## Cloud Services Used
- Azure Data Factory
- Azure Data Lake
- Azure Data Warehouse
- Azure Blob Storage
- Azure HDInsight
- Azure Databricks
- Azure SQL DB

## Architecture
<img width="900" alt="Architcture" src="https://user-images.githubusercontent.com/83560277/116968580-c1146f80-ac82-11eb-886a-834d599b9023.PNG">

## Environment Set-up
<img width="709" alt="Enviroment set up" src="https://user-images.githubusercontent.com/83560277/117481984-bdf2db00-af31-11eb-8ad1-fb086ac30259.PNG">

**Azure SQL DB** 
- Will use SQL DB to store our reports.
 
**Azure Data Factory**
- We need this for ingestion and transformation of the raw data. 
- We will also use data flow which is part of ADF.

**Azure Blob Storage**
- This will be used for population data and for the script will use for the HDInsight transformation.

**Azure Data Lake Storage Gen2**
- To store our ingested and transformed data.
  
**Azure Databricks Clusters**
- For Transformation of the data.

**HD Insight Clsuter**
- For Transformation of the data.
























