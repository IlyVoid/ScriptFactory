<h1>Cryptographic File Encryption and Decryption</h1>

<p>This Python script provides functionality for encrypting and decrypting files using AES encryption with CBC mode and SHA-256 hashing.</p>

<h2>Usage</h2>

<p>Before running the script, make sure you have the necessary dependencies installed:</p>

<pre>
pip install pycryptodome termcolor tqdm
</pre>

<h3>Encrypting Files</h3>

<p>To encrypt files, run the script and choose the option to encrypt (E). You will be prompted to enter a passphrase. The script will then encrypt all files in the current directory recursively. Encrypted files will have the prefix "(encrypted)" added to their names.</p>

<pre>
python crypt.py
</pre>

<h3>Decrypting Files</h3>

<p>To decrypt files, run the script and choose the option to decrypt (D). You will be prompted to enter the filename of the encrypted file you want to decrypt and the passphrase used for encryption. The decrypted file will be saved in the same directory without the "(encrypted)" prefix.</p>

<pre>
python crypt.py
</pre>

<h2>Dependencies</h2>

<ul>
  <li><a href="https://github.com/Legrandin/pycryptodome">pycryptodome</a>: For AES encryption and decryption.</li>
  <li><a href="https://github.com/kennethreitz/termcolor">termcolor</a>: For colored terminal output.</li>
  <li><a href="https://github.com/tqdm/tqdm">tqdm</a>: For progress bars.</li>
</ul>

<h2>Contributing</h2>

<p>Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on <a href="https://github.com/IlyVoid/ScriptFactory">GitHub</a>.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>

