# NetworkSecurityProject
project for network security course
<br>
<br>
                          $DH$<br>
  Client                                       Server <br>
  <br>
                                            generate DH params(g,p)<br>
                                            generate a<br>
generate b                                  A=modpow(g,a,p)<br>
                        <==={g,p,A}===  <br>
B=modpow(g,b,p)         ======{B}====>  <br>
KEY=modpow(A,b,p)                           KEY=modpow(B,a,p)<br>
                        <==RC4(KEY)==><br>
<br>
<br>
                            $auth$  <br>         
                                            generate random_key<br>
                        <==random_key==<br>
input login,pass<br>
h=md5(md5(pass)+random_key)<br> 
auth_data = [login,h]<br>
                        ===data_auth==><rb>      
                                             login,hash_pass=get_login_pass_from_db(data[0])<br>
                                             if md5(hashpass+random_key)==data[1]:<br>
                                                  set_session_key_for_user(data[0],KEY)<br>



