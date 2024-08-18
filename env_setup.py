import subprocess
import sys

def check_environment(env_name="icloud_env", python_version="3.10"):
    """Check if the conda environment exists and meets the required Python version."""
    try:
        # List all environments
        env_list = subprocess.check_output("conda env list", shell=True).decode(sys.stdout.encoding)
        
        if env_name in env_list:
            print(f"Environment '{env_name}' exists. Checking Python version...")
            
            # Check Python version in the environment
            python_version_output = subprocess.check_output(f"conda run -n {env_name} python --version", shell=True).decode(sys.stdout.encoding).strip()
            print(f"Python version in '{env_name}': {python_version_output}")

            if python_version in python_version_output:
                print(f"Environment '{env_name}' meets the required Python version {python_version}.")
                return True
            else:
                print(f"Environment '{env_name}' does not meet the required Python version. Recreating environment.")
                return False
        else:
            print(f"Environment '{env_name}' does not exist.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error checking environment: {e}")
        return False

def setup_conda_environment(env_name="icloud_env", python_version="3.10"):
    """Create or recreate a conda environment with the specified Python version."""
    try:
        # Remove the environment if it exists
        subprocess.run(f"conda env remove -n {env_name} -y", shell=True, check=True)
        print(f"Existing environment '{env_name}' removed.")
    except subprocess.CalledProcessError:
        print(f"Environment '{env_name}' does not exist or could not be removed.")

    # Create the environment
    subprocess.run(f"conda create -n {env_name} python={python_version} -y", shell=True, check=True)
    print(f"Environment '{env_name}' created with Python {python_version}.")

    # Install pyicloud using pip
    subprocess.run(f"conda run -n {env_name} pip install pyicloud", shell=True, check=True)
    print(f"'pyicloud' installed in environment '{env_name}'.")

def activate_and_run_in_environment(env_name, script_path):
    """Run the provided script in the specified conda environment."""
    subprocess.run(f"conda run -n {env_name} python {script_path}", shell=True, check=True)

def ensure_environment(env_name="icloud_env", python_version="3.10"):
    """Ensure that the environment exists with the required Python version. If not, create it."""
    if check_environment(env_name, python_version):
        print(f"Activating environment '{env_name}'.")
        # The activation step is implicit in `conda run`
        return True
    else:
        print(f"Setting up environment '{env_name}'.")
        setup_conda_environment(env_name, python_version)
        return True