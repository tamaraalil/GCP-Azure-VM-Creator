import os
import subprocess
import re
import configparser
from datetime import datetime
import getpass as gt
import shutil


# Program Name: automate.py
# Author: Tamara Alilovic


# Colours for Terminal Printing
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

VMsuccess = []

# Opening message
print(f"{bcolors.OKGREEN}Welcome to VM Creation Automator!{bcolors.ENDC}\n")

# ------------------------- ERROR CHECK CONF FILES -------------------------

# Error check azure.conf
if os.path.isfile('azure.conf'): # Check if config file exists
    azure = configparser.ConfigParser()
    azure.read("azure.conf")
    i = 1
    for section in azure.sections():
        if i < 10: # Naming convention error check
            if section != ("azure0"+str(i)):
                print(f"{bcolors.FAIL}Error:{bcolors.ENDC} the section names in \'azure.conf\' does follow the naming convention.")
                exit(0)
        if i == 10: # Naming convention error check
            if section != "azure10":
                print(f"{bcolors.FAIL}Error:{bcolors.ENDC} the section names in \'azure.conf\' does follow the naming convention.")
                exit(0)
        if i > 10: # Too many VMs error
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} too many VM instances in \'azure.conf\'. There cannot be more than 10 VMs.")
            exit(0)
        i = i + 1
else: # Error message for if azure.conf file exists
    print(f"{bcolors.FAIL}Error:{bcolors.ENDC} \'azure.conf\' does not exist in this directory.")
    exit(0)

# Error check gcp.conf
if os.path.isfile('gcp.conf'): # Check if config file exists
    gcp = configparser.ConfigParser()
    gcp.read("gcp.conf")
    i = 1
    for section in gcp.sections():
        if i < 10: # Naming convention error check
            if section != ("gcp0"+str(i)):
                print(f"{bcolors.FAIL}Error:{bcolors.ENDC} the section names in \'gcp.conf\' does follow the naming convention.")
                exit(0)
        if i == 10: # Naming convention error check
            if section != "gcp10":
                print(f"{bcolors.FAIL}Error:{bcolors.ENDC} the section names in \'gcp.conf\' does follow the naming convention.")
                exit(0)
        if i > 10: # Too many VMs error
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} too many VM instances in \'gcp.conf\'. There cannot be more than 10 VMs.")
            exit(0)
        i = i + 1
else: # Error message for if gcp.conf file exists
    print(f"{bcolors.FAIL}Error:{bcolors.ENDC} \'gcp.conf\' does not exist in this directory.")
    exit(0)

# ------------------------- CREATE AZURE VMs -------------------------

print(f"{bcolors.HEADER} - Creating Azure VMs - {bcolors.ENDC}")

# Loop through each section in the configuration file
for section in azure.sections():
    try: # Read data from config file
        # Define Azure resource group, region, and virtual machine name
        resource_group = azure[section]['resource-group']
        location = azure[section]['location']
        vm_name = azure[section]['name']
        admin_username = azure[section]['admin-username']

        # Define VM image and size based on OS
        os_type = azure[section]['os']
        if os_type == 'linux':
            image = azure[section]['image']
            vm_size = 'Standard_DS1_v2'
        elif os_type == 'windows':
            image = azure[section]['image']
            vm_size = 'Standard_DS2_v2'
        else:
            print(f"Unsupported OS type: {os_type}")
            continue

    except: # Error message for incorrect .conf file format
        print(f"{bcolors.FAIL}Error:{bcolors.ENDC} \'azure.conf\' does not have all of the necessary information.")
        exit(0)

    # Get password from user
    flag = 0
    password_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{12,123}$"
    while flag == 0: # Loop until password complexity is correct
        admin_password = input(f"Type in Password for Azure VM {vm_name}: ")
        if re.match(password_regex, admin_password):
            flag = 1
        else: # Error check password
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} Invalid password. Password must: at least 8 characters, including uppercase and lowercase letters, numbers, one special character.")
            print("\t- Be between 12 and 123 characters in length")
            print("\t- Contain at least one uppercase letter")
            print("\t- Contain at least one lowercase letter")
            print("\t- Contain at least one number")
            print("\t- Contain at least one special character")
            flag = 0

    # Define SSH public key for authentication
    ssh_key_path = "/key.pub"

    # Define Azure CLI commands to create resource group and virtual machine
    create_rg_command = f"az group create --name {resource_group} --location {location} --output table"
    create_vm_command = f"az vm create --name {vm_name} --resource-group {resource_group} --image {image} --size {vm_size} --admin-username {admin_username} --admin-password {admin_password} --output table"

    # Execute Azure CLI commands
    try:
        print(f"{bcolors.OKCYAN}Executing command: {bcolors.ENDC}", create_rg_command)
        subprocess.call(create_rg_command, shell=True)
        print(f"{bcolors.OKCYAN}Executing command: {bcolors.ENDC}", create_vm_command)
        subprocess.call(create_vm_command, shell=True)
        VMsuccess.append(section)
    except: # Error message upon failure
        print(f"{bcolors.FAIL}Error:{bcolors.ENDC} could not create VM.")

# ------------------------- CREATE GCP VMs -------------------------

print(f"{bcolors.HEADER} - Creating GCP VMs - {bcolors.ENDC}")

# Loop through each section in the configuration file
for section in gcp.sections():
    try: # Read data from config file
        # Info needed to create VM
        vm_name = gcp[section]['name']
        image = gcp[section]['image']
        image_project = gcp[section]['imageproject']
        zone = gcp[section]['zone']

    except: # Error message for incorrect .conf file format
        print(f"{bcolors.FAIL}Error:{bcolors.ENDC} \'gcp.conf\' does not have all of the necessary information.")
        exit(0)

    # Error check VM name
    vm_regex = r"^[a-z0-9]*$"
    if not re.match(vm_regex, vm_name):
        print(f"{bcolors.FAIL}Error:{bcolors.ENDC} Invalid VM name. The VM name must only contain lowercase letters and numbers.")

    # Prompt user for project name
    flag = 0
    while flag == 0: # Loop until password complexity is correct
        project = input(f"Input the project ID for the GCP VM \"{vm_name}\": ")
        output = subprocess.check_output('gcloud projects list', shell=True) # List projects
        output = output.decode("utf-8")
        #cmd = f'gcloud projects list --filter="name={project}" --format="value(projectId)"'
        #project_id = subprocess.check_output(cmd, shell = True)
        #project_id = project_id.decode("utf-8")
        #print("id: ", project_id)
        if project in output:
            flag = 1
        else: # Error check password
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} project name inputted does not exist. Please try again.")
            flag = 0
    
    # Create commands
    set_project_command = f'gcloud config set project {project}'
    createVMCommand = f"gcloud compute instances create {vm_name} --image {image} --image-project {image_project} --zone {zone}"

    # Run commands
    output = ""
    try:
        print(f"{bcolors.OKCYAN}Executing command: {bcolors.ENDC}", set_project_command)
        subprocess.call(set_project_command, shell = True)
        print(f"{bcolors.OKCYAN}Executing command: {bcolors.ENDC}", createVMCommand)
        output = subprocess.check_output(createVMCommand, shell=True)
    except: # Error message upon failure
        print(f"{bcolors.FAIL}Error:{bcolors.ENDC} could not create VM.")
    
    # If successful, add to list of successful VMs
    if isinstance(output, bytes):
        if "ERROR" not in output.decode('utf-8'):
            VMsuccess.append(section)
    elif isinstance(output, str):
        if "ERROR" not in output:
            VMsuccess.append(section)

# ------------------------- CREATE DOCUMENTATION FILE -------------------------

# Create documentation file
date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
filename = "VMcreation_" + date + ".txt"
f = open(filename, "w")

f.write("automate.py VM Creation Documentation \n\n")
f.write("System Admin Name: " + gt.getuser() + "\n\n")

# Add Azure VM information to doc file
f.write("AZURE VMs: \n")
for section in azure.sections():
    f.write("\t\t" + section + "\n")
    f.write("\tVM Name: " + azure[section]['name'] + "\n")
    f.write("\tPurpose: " + azure[section]['purpose'] + "\n")
    f.write("\tTeam: " + azure[section]['team'] + "\n")
    f.write("\tOS: " + azure[section]['os'] + "\n")
    if section in VMsuccess:
        f.write("\tVM Status: Running\n\n")
    else:
        f.write("\tVM Status: Failed to create\n\n")

# Add GCP VM information to doc file
f.write("\nGCP VMs: \n")
for section in gcp.sections():
    f.write("\t\t" + section + "\n")
    f.write("\tVM Name: " + gcp[section]['name'] + "\n")
    f.write("\tProject: " + gcp[section]['project'] + "\n")
    f.write("\tPurpose: " + gcp[section]['purpose'] + "\n")
    f.write("\tTeam: " + gcp[section]['team'] + "\n")
    f.write("\tOS: " + gcp[section]['os'] + "\n")
    if section in VMsuccess:
        f.write("\tVM Status: Running\n\n")
    else:
        f.write("\tVM Status: Failed to create\n\n")
f.close()

# Copy .conf files over to datestamped files
shutil.copyfile('azure.conf','azure_' + date + '.conf')
shutil.copyfile('gcp.conf','gcp_' + date + '.conf')

# Exit messages
print(f"{bcolors.OKGREEN}\nVM Documentation added to file {filename} {bcolors.ENDC}")
print(f"{bcolors.OKGREEN}Exiting program, goodbye!{bcolors.ENDC}")