# ABBYY Vantage Document Processing Script

## Overview
This script automates document processing using ABBYY Vantage Skills. It monitors a directory for new documents, processes them using the specified Skill, extracts data, and exports the results.

## Usage
1. **Configure Account Information:** Enter your ABBYY Vantage account details in the script.
2. **Define Paths:** Specify paths for importing, processing, and exporting documents.
3. **Specify Skill:** Define the ABBYY Vantage Skill to use.

## Project Description
- **Authorization:** Authenticate access to the ABBYY Vantage API.
- **Skill Verification:** Check if the specified Skill exists.
- **Processing Documents:**
  - Monitor an import directory for new documents.
  - Initiate document processing transactions.
  - Monitor transaction status until completion.
  - Retrieve extracted data.
- **Exporting Results:** Save extracted data as JSON files.
- **Loop:** Continuously monitor for new documents.

## GitHub Usage
1. Clone/download the repository.
2. Modify the script with your ABBYY Vantage account details.
3. Run the script using Python.

