# CA - stands for "Castle Age"
## This is the python project for automation of CA.
***
|Author|DOCK CHEN|
|:---|:---|
|Email|dock.chen@gmail.com|
***
Castle age home page 
- https://web3.castleagegame.com/castle_ws/index.php
***
### HOW TO START
1. Install Python and clone this git
    - Python: <https://www.python.org/downloads/>
    - GitHub: <https://github.com/dockchen/CA>
2. Update "CA_accounts_full.json" before start<br>
    This JSON file stores all CA account information for automation. mandatory fields needed should be,<br>
        `NO`: serial number<br>
        `Guild`: Guild name<br>
        `Name`: user name<br>
        `Email`: CA login email<br>
        `PWD`: CA login password<br>
        `Squad`: squad of 10p battle<br>
        `Def_loadout`: default loadout when all actions done<br>
        `Conquest_Duel`: Perform conquest duel or not. 0: No, 1: Yes<br>
        `Collect_Conquest`: Collect Conquest path rewards. 0: No, 1: Yes<br>
        `PvP_Loadout`: PvP loadout, used when perform "conquest duel"<br>
        `DailyClick`: Perform daily click or not. 0: No, 1: Yes<br>
        `Blessing`: Perform bless or not. 0: No, 1: Yes<br>
        `Campaign`: Specify Campaign type. will activate campaign when blessing.<br>
        `Reward_100P`: Collect 100p rewards or not. 0: No, 1: Yes<br>
        `Reward_10P`: Collect 10p rewards or not. 0: No, 1: Yes<br>
        `Reward_CGB`: Collect classical Guild Battle rewards or not. 0: No, 1: Yes<br>
        
        [
            {
                "NO": 63,
                "Guild": "GuildName",
                "Name": "UserName",
                "Email": "CA login email",
                "PWD": "CA login password",
                "Class": "Mage",
                "Squad": 0,
                "Def_Loadout": 5,
                "Conquest_Duel": 0,
                "Collect_Conquest": 0,
                "PvP_Loadout": 6,
                "DailyClick": 1,
                "Blessing": 2,
                "Campaign": "easy",
                "Reward_100P": 0,
                "Reward_CGB": 0,
                "Reward_10P": 0,
                "Army code": "123456",
                "BSI": 310.2,
                "eng": 341,
                "eng_bonus": 0,
                "sta": 389,
                "sta_bonus": 0,
                "atk": 266,
                "atk_bonus": 26,
                "def": 21,
                "def_bonus": 5,
                "health": 102,
                "health_bonus": 0,
                "army": 283,
                "Comment": null,
                "Owner": null
            }
        ]

3. Update "target_id_list.json" before start<br>
    target_id_list.json is a list of conquest duel target id as format shown below, conquest duel will choose one target in the list randomly.<br>
    ```
    [
        {
        "target_id": "19608101",
        "max_bsi": 5332.0,
        "min_bsi": 0
        }
    ]
    ```
4. Start CA automation<br>
    `CA.py` is the main function of CA project. You can start CA automation by executing `CA.py` as below.<br>
    ```
    python CA.py -DC -CD
    python CA.py -g Fu -sqd 1 -sqd 2 -10p
    ```
    ### Syntax as shown below:
        usage: ca.py [-h] [-v] [-f FILENAME] [-10p] [-100p] [-CGB] [-DC]
             [-b {0,1,2,3,4,5}] [-CD] [-g {Any,YoPing,Fu,Lu}]
             [-sqd {1,2,3,4,5,6,7,8,9,10}]

        Castle Age Automation

        optional arguments:
          -h, --help            show this help message and exit
          -v, --version         show program's version number and exit
          -f FILENAME, --filename FILENAME
          -10p, --Reward_10P    Collect 10P battle reward
          -100p, --Reward_100P  Collect 100P battle reward
          -CGB, --Reward_CGB    Collect Classical GB reward
          -DC, --DailyClick     Daily clicks - Enable, Bless, Resource, Crystal...
          -b {0,1,2,3,4,5}, --Blessing {0,1,2,3,4,5}
                                Blessing - 0: profile; 1:Eng; 2:Atk; 3:Def; 4:Health;
                                5:STA
          -CD, --ConquestDuel   Auto Conquest Duel
          -g {Any,YoPing,Fu,Lu}, --Guild {Any,YoPing,Fu,Lu}
                                Specify guild to do actions
          -sqd {1,2,3,4,5,6,7,8,9,10}, --Squad {1,2,3,4,5,6,7,8,9,10}
                                Specify squads to do actions
5. Create your own function<br>
    Key features are bounded in `CA_util\CA_util_class`, initial a instance to start automation<br>
    for example: <br>
    ```
    from CA_util import CA_util_class

    CA = CA_util_class.CA_instance(args)
    CA.do_CA_actions()
    del CA
    ```
