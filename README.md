# flute
[![GitHub issues](https://img.shields.io/github/issues/gumupaier/flute)](https://github.com/gumupaier/flute/issues) [![GitHub forks](https://img.shields.io/github/forks/gumupaier/flute)](https://github.com/gumupaier/flute/network) [![GitHub stars](https://img.shields.io/github/stars/gumupaier/flute)](https://github.com/gumupaier/flute/stargazers) [![GitHub license](https://img.shields.io/github/license/gumupaier/flute)](https://github.com/gumupaier/flute/blob/main/LICENSE)

nebula graph database toolkit python version

- install command
```
pip install nebula-flute
```



- The list of commands

```
# Generate a Docker-Stack file for deploying Nebula
flute amber
```

- Use the sample
```
✗ flute amber
[?] What's your ip list: 192.168.1.1 192.168.1.2 192.168.1.3
[?] What version of Nebula will you deploy?: 1.2
   nightly
   1.1
 > 1.2

[?] Select the machine role with IP as 192.168.1.1: 
   X metad
 > X graphd
   X storaged

[?] What is the hostname of the machine with IP as 192.168.1.1?: nebula1
[?] Select the machine role with IP as 192.168.1.2: 
   X metad
   X graphd
 > X storaged

[?] What is the hostname of the machine with IP as 192.168.1.2?: nebula2
[?] Select the machine role with IP as 192.168.1.3: 
   X metad
   X graphd
 > X storaged

[?] What is the hostname of the machine with IP as 192.168.1.3?: nebula3

```

Then you can see that a Docker-Stack file has been generated
