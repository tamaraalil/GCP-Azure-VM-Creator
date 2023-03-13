# GCP-Azure-VM-Creator
Python script to automatically create up to 20 VMs total on Google Cloud Platform and Azure.

## Before Running
- For GCP, ensure that the projects you will create VMs in have "Compute Engine API" enabled before running the program, and that billing information has been entered.
- Ensure you are logged into Azure using "az login" before running the program.

## Compile & Run:
- Add "azure.conf" and "gcp.conf" to directory
python3 automate.py

## Notes:
- When prompted for the project ID for the GCP VMs, make sure to type the Project ID and not the Project name. The program will keep prompting for input until it gets a Project ID that exists.
- The program will create three new files upon completion, all timestamped in the filename:
    - "VMcreation_<timestamp>.conf" lists details about the VMs created
    - "azure_<timestamp>.conf" saves the contents from "azure.conf" for archiving purposes of the user
    - "gcp_<timestamp>.conf" saves the contents from "gcp.conf" for archiving purposes of the user
- This program assumes that the user already has Azure and GCP CLI installed on their machine before running the program
### .conf Files
- Maximum 10 VMs per .conf file
- Naming convention:
    - The section names of the VMs detailed in the .conf files must be of the naming convention "azure01", "azure02", ... "azure10" in azure.conf, and "gcp01", "gcp02", ... "gcp10" in gcp.conf.
    - The names must start at "01" and cannot exceed 10.

## Code Structure
- My program will first error check the naming conventions in the .conf files and quits if the names are not of the 
correct format.
- Then, the program will create the Azure VMs. For each VM, it will prompt the user for a password for the VM.
- Then, the program will create the GCP VMs. For each VM, it will prompt the user for a project ID to enter.