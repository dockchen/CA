# CA - stands for "Castle Age", this is the python project for automation of CA.
 
Castle age - https://web3.castleagegame.com/castle_ws/index.php

1. Key features are bounded in 'CA_util\CA_util_class', initial a instance to start automation
  for example: 
    from CA_util import CA_util_class
    CA = CA_util_class.CA_instance(args)
    
2. argument of constructor of CA_util_class is a command line options (i.e. argparse, ref to "https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse" for detail)
  -v version number
  -f filename 
    specify file name of JSON file which store username, passsword and other key settings of CA users
  -10p 
    collect 10p battle rewards
  -100p 
    collect 100p battle rewards
  -CGB 
    collect Classical GB rewards
  -DC 
    daily click. includes Enable, Bless, Resource, Crystal
  -CD
    conquest duel. perform conquest duel based on "target_id_list.json"
  -g guildname
    specify guild name to perform actions
  -sqd squad_number
    specify squad_number to perform actions

3. CA.py - main function of CA project. You can start automation by executing CA.py as below.
  python CA.py -DC -CD
  python CA.py -g Fu -sqd 1 -sqd 2 -10p

