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
2. CA.py 
    - main function of CA project. You can start automation by executing CA.py as below.<br>
    ```
    python CA.py -DC -CD
    python CA.py -g Fu -sqd 1 -sqd 2 -10p
    ```
3. Key features are bounded in 'CA_util\CA_util_class', initial a instance to start automation
    for example: <br>
    ```
    from CA_util import CA_util_class
    
    CA = CA_util_class.CA_instance(args)
    CA.do_CA_actions()
    del CA
    ```

4. argument of constructor of CA_util_class is a command line options (i.e. argparse, ref to "https://docs.python.org/zh-tw/3/library/argparse.html#module-argparse" for detail)<br>
    `-v version number`<br>
        show version number<br>
    `-f filename`<br>
        specify file name of JSON file which store username, passsword and other key settings of CA users<br>
    `-10p` <br>
    collect 10p battle rewards<br>
    `-100p` <br>
    collect 100p battle rewards<br>
    `-CGB` <br>
    collect Classical GB rewards<br>
    `-DC` <br>
    daily click. includes Enable, Bless, Resource, Crystal    <br>
    `-CD`<br>
    conquest duel. perform conquest duel based on "target_id_list.json"<br>
    `-g guildname`<br>
    specify guild name to perform actions<br>
    `-sqd squad_number`<br>
    specify squad_number to perform actions<br>

5. update "CA_accounts_full.json" and "target_id_list.json" before start<br>
    - CA_accounts_full.json
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
        ```
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
    ```
    - target_id_list.json
        list of conquest duel target id as format shown below, conquest duel will choose one target in the list randomly.<br>
        ```
            [
                {
                "target_id": "19608101",
                "max_bsi": 5332.0,
                "min_bsi": 0
                }
            ]
        ```
