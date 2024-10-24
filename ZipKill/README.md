# zipKill

**zipKill** is a fast ZIP password cracker written in Bash. It uses a wordlist to attempt to find the correct password for encrypted ZIP files, utilizing parallel processing for improved speed.

## Features

- Select any ZIP file for cracking
- Use a custom password wordlist
- Runs multiple password attempts in parallel for faster results
- Simple and easy-to-use command-line interface

## Requirements

- `unzip`: This tool is required to test passwords against ZIP files.
- Bash: The script is intended to run in a Bash environment.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/IlyVoid/zipKill.git
   cd zipKill
   ```

2. Ensure the script is executable:

   ```bash
   chmod +x zipKill.sh
   ```

## Usage

1. Run the script:

   ```bash
   ./zipKill.sh
   ```

2. Follow the prompts to enter the path to the ZIP file and the password wordlist.

   ```
   Enter the path to the ZIP file: /path/to/your/protected.zip
   Enter the path to the password wordlist: /path/to/your/passwords.txt
   ```

3. The script will attempt to crack the ZIP file password, displaying any successful attempts.

## Example

```bash
$ ./zipKill.sh
Enter the path to the ZIP file: /path/to/your/protected.zip
Enter the path to the password wordlist: /path/to/your/passwords.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**zipKill** is intended for educational and ethical purposes only. Use it responsibly and ensure you have permission to test the ZIP files you are working with. Unauthorized access to data is illegal and unethical.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or feature requests.

```

### Notes:
- **Repository URL**: Make sure to replace `https://github.com/IlyVoid/zipKill.git` with the actual URL of your GitHub repository.
- **License**: If you plan to include a license file, ensure you provide details on how to obtain it.
- **Customization**: Feel free to add any additional sections that might be relevant, such as FAQs or troubleshooting tips, depending on your audience and how complex the tool becomes. 
