
This script is designed to interact with ABBYY Vantage, an intelligent document processing platform. Here's a breakdown of how to use it and what it does:

How to Use:
Configure Account Information: You need to input your ABBYY Vantage account information, including username, password, and client secret, in the designated fields.
Define Paths: Specify the paths for importing documents (path_import), storing processed documents (path_processed), and exporting extracted data from documents (path_export).
Specify Skill: Define the ABBYY Vantage Skill you want to use (skill_name).
Project Description:
The script facilitates the automated processing of documents using ABBYY Vantage Skills. Here's how it works:

Authorization: The script starts by authorizing access to the ABBYY Vantage API using the provided account information.
Skill Verification: It checks if the specified Skill exists in your account. If not, it exits the script.
Processing Documents:
The script continuously monitors a specified directory (path_import) for new documents.
Once a document is detected, it initiates a transaction with ABBYY Vantage to process the document using the specified Skill.
It then monitors the transaction status until the document is processed.
After processing, it retrieves the extracted data from the document.
Exporting Results:
The extracted data is saved as a JSON file with the same name as the original document in the specified export directory (path_export).
The processed document is moved to another directory (path_processed).
Loop: The script continues to monitor the import directory for new documents, repeating the process.
GitHub Usage:
To use this script via GitHub:

Clone or download the repository containing the script.
Ensure you have Python installed on your system.
Modify the script with your ABBYY Vantage account information, paths, and Skill.
Run the script using a Python interpreter.
