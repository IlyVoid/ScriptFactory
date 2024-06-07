<!DOCTYPE html>
<html lang="en">

<h1>Cryptographic File Encryption and Decryption with SHELL</h1>
<p>This shell script provides functionality for encrypting and decrypting files using AES encryption with CBC mode and SHA-256 hashing.</p>

<h2>Usage</h2>
<p>Before running the script, make sure you have the necessary dependencies installed:</p>
<ul>
    <li>OpenSSL</li>
    <li>zsh shell</li>
</ul>

<h3>Encrypting Files</h3>
<p>To encrypt files, run the script, You will be prompted to enter a passphrase. The script will then encrypt all files in the current directory and sub-directories recursively. Encrypted files will have the ".encrypted" extension added to their names.</p>
<pre><code>./lock.sh</code></pre>

<h3>Decrypting Files</h3>
<p>To decrypt files, run the script, You will be prompted to enter the passphrase used for encryption. The decrypted file will be saved in the same directory without the ".encrypted" extension.</p>
<pre><code>./unlock.sh</code></pre>

<h2>Dependencies</h2>
<ul>
    <li>OpenSSL: For AES encryption and decryption.</li>
    <li>zsh shell</li>
</ul>

<h2>Contributing</h2>
<p>Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on <a href="https://github.com/IlyVoid/ScriptFactory">GitHub</a>.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>

</body>
</html>
