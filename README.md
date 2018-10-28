# NetworkSecurityProject
project for network security course
<br>
Diffie Hellman + RC4<br>
auth: md5(md5(pass)+random_key)==md5(hash_pass_from_db+random_key)<br>
<br>
DB: users(id,login,hash_pass), sess(id,login,session_key)<br>
<br>
server start: python3 server/tcp_server.py<br>
client start: python3 auth.py<br>





