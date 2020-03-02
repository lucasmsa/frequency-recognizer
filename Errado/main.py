# from clientsClass import lucasLaptop
# from paramiko import SSHClient, AutoAddPolicy
# import simpleaudio as sa
 

# # call for client
# ssh = SSHClient()
# ssh.set_missing_host_key_policy(AutoAddPolicy())

# # connect through client IP, username and password
# ssh.connect(hostname=lucasLaptop.ip, username=lucasLaptop.username, password=lucasLaptop.password)

# # execute file in client
# stdin, stdout, stderr = ssh.exec_command('python test2.py')

# # playing sound
# waveObj = sa.WaveObject.from_wave_file("audio/ps1.wav")
# playSound = waveObj.play()
# playSound.wait_done()

# # closing connection
# ssh.close()
# stdin.close()

