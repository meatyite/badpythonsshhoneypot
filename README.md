# badpythonsshhoneypot
a very badly programmed ssh honeypot  <br />
inspired by https://github.com/jaksi/sshesame <br />
feel free to fork this :-)
# How to use (On linux)
sudo apt-get install python-pip <br />
pip install twisted <br />
pip install pyOpenSSL <br /> 
pip install service_identity <br />
cd ~ <br />
mkdir honeypot <br />
cd honeypot <br />
git clone https://github.com/sl4vkek/badpythonsshhoneypot.git ./ <br />
ssh-keygen <br />
cd ~/.ssh <br />
mv ./id_rsa ~/honeypot/ <br />
mv ./id_rsa.pub ~/honeypot/ <br />
cd ~/honeypot/ <br />
python ./honeypot.py <br />
# Test the honeypot
ssh root@127.0.0.1 -p 2222 <br />
(the password is "password")

