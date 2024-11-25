### Network Security : Phishing URL Detection System Using Machine Learning 

This project focuses on building a machine learning model to detect phishing URLs using feature-based analysis. The system follows MLOps principles, with data ingested from MongoDB, models tracked in DagsHub with MLflow, and deployed to AWS using Docker, S3, and ECR. CI/CD is automated via GitHub Actions, ensuring a scalable and efficient pipeline.

---


## Features
- **Data Ingestion**: Seamlessly retrieves data from MongoDB for processing.
- **Data Preprocessing**: Automated cleaning and transformation of URL datasets.
- **Model Training**: ML algorithms to detect phishing URLs with high accuracy.
- **Deployment**: The solution is deployed on an AWS EC2 instance, utilizing S3 buckets for data storage and Amazon ECR for container management.
- **API Integration**: Exposes prediction capabilities via REST API.
- **Containerization**: Deployed using Docker for consistency across environments.
- **Monitoring and Logging**: Tracks system performance and logs errors for troubleshooting.

--- 


## Project Structure
```plaintext
NetworkSecurity/
├── app.py                 # Entry point for the API
├── main.py                # Main script for pipeline execution
├── data_schema/           # Schema definitions for datasets
├── Dockerfile             # Docker configuration
├── networksecurity/       # Core modules and utilities
├── Network_Data/          # Raw data
├── notebooks/             # Jupyter notebooks 
├── prediction_output/     # Model predictions and outputs
├── requirements.txt       # Python dependencies
├── setup.py               # Package setup script
├── templates/             # HTML templates for web interface
├── tests/                 # Test cases
├── test_mongodb.py        # MongoDB-related tests
├── valid_data/            # Validated data for training/testing
```

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jiyadhks/network-security.git
   cd NetworkSecurity
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project
1. **Run the API**:
   ```bash
   python app.py
   ```


## Dataset
The project uses URL datasets for training and validation. The data is stored in `Network_Data/` and follows the schema defined in `data_schema/`.

## Model Details
- **Algorithms Used**:  `AdaBoostClassifier`, `GradientBoostingClassifier`, `RandomForestClassifier`

## Testing
Test cases are located in the `tests/` directory and can be executed using:
```bash
pytest tests/
```

## Deployment
The model is deployed as a REST API using Flask. It runs on an AWS EC2 instance, with data stored in S3 buckets and containerized applications managed through Amazon ECR.

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and submit a pull request.

## Future Enhancements
- Incorporating real-time URL scanning.
- Adding support for more ML models.
- Enhancing logging and monitoring with tools like Prometheus and Grafana.