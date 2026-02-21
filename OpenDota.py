# -- version --
__version__ = (2, 0, 3)
# -- version --


# meta developer: @Itachi_Uchiha_sss
# meta banner: https://api.opendota.com

import requests
from .. import loader, utils
from telethon.tl.types import Message 
from datetime import datetime, timezone
import time

API_URL = "https://api.opendota.com/api"

@loader.tds
class DotaStatsMod(loader.Module):
    strings = {"name": "DotaStats"}
   
    def is_win(self, match):
        is_radiant = match["player_slot"] < 128
        return match["radiant_win"] == is_radiant



    def __init__(self):
        self._pages_cache = {}
        self.config = loader.ModuleConfig(
            "PLAYER_ID", None, "Steam ID игрока"
        )
        self.heroes = {}
        self.item_emojis = {            
            "Blink": '<emoji document_id=5467710328080981143>🤩</emoji>',
            "Black King Bar": '<emoji document_id=5467828615775279955>🤩</emoji>',
            "Ultimate Scepter": '<emoji document_id=5467777522844327342>🤩</emoji>',
            "Power Treads": '<emoji document_id=5467823212706421270>🤩</emoji>',
            "Desolator": '<emoji document_id=5467606626095619791>🤩</emoji>',
            "Greater Crit": '<emoji document_id=5467526443351170991>🤩</emoji>',
            "Satanic": '<emoji document_id=5467481238820381084>🤩</emoji>',
            "Butterfly": '<emoji document_id=5467628088047197171>🤩</emoji>',
            "Assault Cuirass": '<emoji document_id=5467467786982809436>🤩</emoji>',
            "Sheepstick": '<emoji document_id=5467471613798669675>🤩</emoji>',
            "Rapier": '<emoji document_id=5469940176316816456>🤩</emoji>',
            "Heart": '<emoji document_id=5469829838606982639>🤩</emoji>',
            "Shadow Blade": '<emoji document_id=5469889422688278238>🤩</emoji>',
            "Manta": '<emoji document_id=5467786310347413191>🤩</emoji>', 
            "Sphere": '<emoji document_id=5467841560806709776>🤩</emoji>',
            "Moon Shard": '<emoji document_id=5469874360237970537>🤩</emoji>',  
            "Crystalys": '<emoji document_id=5467629917703264949>🤩</emoji>', 
            "Dragon Lance": '<emoji document_id=5429427424850906507>🫤</emoji>',  
            "Skadi": '<emoji document_id=5467912754184609175>🤩</emoji>',  
            "Mjollnir": '<emoji document_id=5467553437220624541>🤩</emoji>',  
            "Eternal Shroud": '<emoji document_id=5429168489862565021>🤤</emoji>',  
            "Radiance": '<emoji document_id=5467917160821053680>🤩</emoji>',  
            "Bloodstone": '<emoji document_id=5467872957017647753>🤩</emoji>',  
            "Vanguard": '<emoji document_id=5467905512869745249>🤩</emoji>',  
            "Overwhelming Blink": '<emoji document_id=5467811268402372102>🤩</emoji>', 
            "Force Staff": '<emoji document_id=5467816044406004412>🤩</emoji>',    
            "Blade Mail": '<emoji document_id=5467910258808610438>🤩</emoji>',  
            "Lotus Orb": '<emoji document_id=5467854656161996490>🤩</emoji>',  
            "Diffusal Blade": '<emoji document_id=5467589596550291093>🤩</emoji>',
            "Disperser": '<emoji document_id=5467511685843540004>🤩</emoji>',  
            "Silver Edge": '<emoji document_id=5467413421286774948>🤩</emoji>', 
            "Solar Crest": '<emoji document_id=5470022991876216864>🤩</emoji>',     
            "Octarine Core": '<emoji document_id=5469910390718616277>🤩</emoji>',  
            "Refresher": '<emoji document_id=5467413301027691972>🤩</emoji>',      
            "Soul Ring": '<emoji document_id=5467735694157831691>🤩</emoji>',  
            "Pipe": '<emoji document_id=5467784545115857970>🤩</emoji>',  
            "Cyclone": '<emoji document_id=5469770533698556516>🤩</emoji>',
            "Wind Waker": '<emoji document_id=5467755674345690984>🤩</emoji>',  
            "Hurricane Pike": '<emoji document_id=5429505296902945143>🤗</emoji>',    
            "Veil of Discord": '<emoji document_id=5467619223234698435>🤩</emoji>',  
            "Glimmer Cape": '<emoji document_id=5467869675662631035>🤩</emoji>',   
            "Shadow Amulet": '<emoji document_id=5467818432407819955>🤩</emoji>',  
            "Tranquil Boots": '<emoji document_id=5467458642997434165>🤩</emoji>',  
            "Arcane Boots": '<emoji document_id=5467688316373590211>🤩</emoji>',  
            "Travel Boots": '<emoji document_id=5467854351219318497>🤩</emoji>',
            "Travel Boots 2": '<emoji document_id=5467653724706986524>🤩</emoji>',
            "Boots": '<emoji document_id=5429649362990960283>💜</emoji>',  
            "Phase Boots": '<emoji document_id=5467564569775857363>🤩</emoji>',
            "Mask of Madness": '<emoji document_id=5467883471097585936>🤩</emoji>',  
            "Drum of Endurance": '<emoji document_id=5467804241835876590>🤩</emoji>',
            "Boots of Bearing": '<emoji document_id=5467809013544541750>🤩</emoji>', 
            "Meteor Hammer": '<emoji document_id=5469909724998687900>🤩</emoji>',  
            "Guardian Greaves": '<emoji document_id=5427047918479642257>👇</emoji>',    
            "Ring of Aquila": '<emoji document_id=5467867145926891521>🤩</emoji>',         
            "Smoke Of Deceit": '<emoji document_id=5467832077518921780>🤩</emoji>',  
            "Dust": '<emoji document_id=5467852414189067273>🤩</emoji>',  
            "Bottle": '<emoji document_id=5467423492985085154>🤩</emoji>',  
            "Magic Stick": '<emoji document_id=5467520726749699871>🤩</emoji>',
            "Holy Locket": '<emoji document_id=5429324818082202689>🥹</emoji>', 
            "Magic Wand": '<emoji document_id=5467791386998758693>🤩</emoji>',  
            "Aether Lens": '<emoji document_id=5467863087182797856>🤩</emoji>',  
            "Swift Blink": '<emoji document_id=5467512635031313209>🤩</emoji>',    
            "Null Talisman": '<emoji document_id=5469971357779384692>🤩</emoji>',  
            "Bracer": '<emoji document_id=5469634555033965479>🤩</emoji>',  
            "Wraith Band": '<emoji document_id=5467754252711516912>🤩</emoji>',  
            "Soul Booster": '<emoji document_id=5467565600568006619>🤩</emoji>',  
            "Kaya": '<emoji document_id=5429406474000437184>👩‍❤️‍💋‍👨</emoji>',  
            "Yasha": '<emoji document_id=5467560339233070091>🤩</emoji>',  
            "Sange And Yasha": '<emoji document_id=5429589242038749865>🤚</emoji>',  
            "Orchid": '<emoji document_id=5467520726749699874>🤩</emoji>',  
            "Bloodthorn": '<emoji document_id=5467694776004401553>🤩</emoji>',  
            "Ethereal Blade": '<emoji document_id=5467641462575358888>🤩</emoji>',  
            "Heaven’s Halberd": '<emoji document_id=5467846439889558895>🤩</emoji>',      
            "Sange": '<emoji document_id=5469885926584898014>🤩</emoji>',  
            "Urn Of Shadows": '<emoji document_id=5467630226940910178>🤩</emoji>',  
            "Spirit Vessel": '<emoji document_id=5429261402890079825>😩</emoji>',    
            "Crimson Guard": '<emoji document_id=5470036121591240703>🤩</emoji>',    
            "Refresher Shard": '<emoji document_id=5467436815973636888>🤩</emoji>',  
            "Echo Sabre": '<emoji document_id=5429603432610695458>🤱</emoji>',
            "Harpoon": '<emoji document_id=5467597984621420624>🤩</emoji>',    
            "Arcane Blink": '<emoji document_id=5467886499049528800>🤩</emoji>',    
            "Abaddon’s Aghanim’s Scepter": '<emoji document_id=5469857141714083939>🤩</emoji>',    
            "Mekansm": '<emoji document_id=5467932824566784067>🤩</emoji>',  
            "Rod Of Atos": '<emoji document_id=5467818376573246343>🤩</emoji>',
            "Kaya And Sange": '<emoji document_id=5467789192270470219>🤩</emoji>',
            "Phylactery": '<emoji document_id=5208510580775737094>😎</emoji>',
            "Khanda": '<emoji document_id=5467410049737448975>🤩</emoji>',
            "Bfury": '<emoji document_id=5469748109674306463>🤩</emoji>',
            "Monkey King Bar": '<emoji document_id=5470163106594312935>🤩</emoji>',
            "Hand Of Midas": '<emoji document_id=5429484178548752495>🤡</emoji>',
            "Skull Basher": '<emoji document_id=5469746426047125184>🤩</emoji>',
            "Abyssal Blade": '<emoji document_id=5467666536594431270>🤩</emoji>',
            "Aeon Disk": '<emoji document_id=5467791133595686879>🤩</emoji>',
            "Armlet": '<emoji document_id=5469824396883416139>🤩</emoji>',
            "Witch Blade": '<emoji document_id=5467826399572156107>🤩</emoji>',
            "Devastator": '<emoji document_id=5467805345642470314>🤩</emoji>',
            "Revenant's Brooch": '<emoji document_id=5469908634076992123>🤩</emoji>',
            "Ward Observer": '<emoji document_id=5467632846870962993>🤩</emoji>',
            "Ward Sentry": '<emoji document_id=5467462169165586203>🤩</emoji>',
            "Ward Dispenser": '<emoji document_id=5469962815089431997>🤩</emoji>',
            "Falcon Blade": '<emoji document_id=5467861553879473110>🤩</emoji>',
            "Mage Slayer": '<emoji document_id=5470013504293461332>🤩</emoji>',
            "Dagon": '<emoji document_id=5469686244965374270>🤩</emoji>',
            "Nullifier": '<emoji document_id=5467639448235695534>🤩</emoji>',
            "Helm Of The Dominator": '<emoji document_id=5467464140555575688>🤩</emoji>',
            "Helm Of The Overlord": '<emoji document_id=5467741569673092276>🤩</emoji>',
            "Maelstrom": '<emoji document_id=5467923019156446536>🤩</emoji>',
            "Ghost": '<emoji document_id=5470035653439803744>🤩</emoji>',
            "Quelling Blade": '<emoji document_id=5467378189670046307>🤩</emoji>',
            "Shivas Guard": '<emoji document_id=5467835062521190904>🤩</emoji>',
            "Infused Raindrop": '<emoji document_id=5429589508326716866>💑</emoji>',
            "Gem": '<emoji document_id=5467526344566921150>🤩</emoji>',
            "Yasha And Kaya": '<emoji document_id=5429591746004680178>💤</emoji>',
            "Lifesteal": '<emoji document_id=5469950286669829137>🤩</emoji>',
            "Lesser Crit": '<emoji document_id=5467629917703264949>🤩</emoji>',
            "Vladmir": '<emoji document_id=5467690648540830431>🤩</emoji>',
            " Orb Of Frost": '<emoji document_id=5429604854244872076>😶‍🌫️</emoji>',
            "Wind Lace": '<emoji document_id=5429632793007129283>🤕</emoji>',
            "Fluffy Hat": '<emoji document_id=5429599227837712299>😑</emoji>',
            "Blight Stone": '<emoji document_id=5429570795154210156>👩‍🦰</emoji>',
            "Mithril Hammer": '<emoji document_id=5467426739980361549>🤩</emoji>',
            "Ogre Axe": '<emoji document_id=5467868851028908643>🤩</emoji>',
            "Circlet": '<emoji document_id=5440652308994098468>👹</emoji>',
            "Cloak": '<emoji document_id=5438211616518734925>🤢</emoji>',
        }
        self.rank_emojis = {
            "Herald": '<emoji document_id=5963157659195542640>🎖</emoji>',
            "Guardian": '<emoji document_id=5963215018483780860>🎖</emoji>',
            "Crusader": '<emoji document_id=5960576663023523045>🎖</emoji>',
            "Archon": '<emoji document_id=5963052342302477581>🎖</emoji>',
            "Legend": '<emoji document_id=5963061984504056919>🎖</emoji>',
            "Ancient": '<emoji document_id=5963027435787127662>🎖</emoji>',
            "Divine": '<emoji document_id=5963113657255594572>🎖</emoji>',
            "Immortal": '<emoji document_id=5960656609544768701>🎖</emoji>'
        }
        self.hero_emojis = {
            "Anti-Mage": '<tg-emoji emoji-id="6062179938386055768">🟢</tg-emoji>',
            "Axe": '<tg-emoji emoji-id="6061943874098564891">🔴</tg-emoji>',
            "Juggernaut": '<tg-emoji emoji-id="6064624766914924449">🟢</tg-emoji>',
            "Pudge": '<tg-emoji emoji-id="6062065073780690927">🔴</tg-emoji>',
            "Invoker": '<tg-emoji emoji-id="6062314229128499676">📚</tg-emoji>',
            "Bane": '<tg-emoji emoji-id="6062010952897793745">📚</tg-emoji>',
            "Bloodseeker": '<tg-emoji emoji-id="6062032122791598368">🟢</tg-emoji>',
            "Crystal Maiden": '<tg-emoji emoji-id="6064219008469569795">🔵</tg-emoji>',
            "Drow Ranger": '<tg-emoji emoji-id="6061854143641816935">🟢</tg-emoji>',
            "Earthshaker": '<tg-emoji emoji-id="6062153554401955565">🔴</tg-emoji>',
            "Mirana": '<tg-emoji emoji-id="6062297886777937723">🟢</tg-emoji>',
            "Morphling": '<tg-emoji emoji-id="6064443858597449152">🟢</tg-emoji>',
            "Shadow Fiend": '<tg-emoji emoji-id="6064205264574222013">🟢</tg-emoji>',
            "Phantom Lancer": '<tg-emoji emoji-id="6061901993872462041">🟢</tg-emoji>',
            "Puck": '<tg-emoji emoji-id="6062166374879335422">🔵</tg-emoji>',
            "Razor": '<tg-emoji emoji-id="6062104175162954182">🟢</tg-emoji>',
            "Sand King": '<tg-emoji emoji-id="6064151371324592043">📚</tg-emoji>',
            "Storm Spirit": '<tg-emoji emoji-id="6061887283609474004">🔵</tg-emoji>',
            "Sven": '<tg-emoji emoji-id="6062262753945457249">🔴</tg-emoji>',
            "Tiny": '<tg-emoji emoji-id="6061984912511078154">🔴</tg-emoji>',
            "Vengeful Spirit": '<tg-emoji emoji-id="6064293105245359489">📚</tg-emoji>',
            "Windranger": '<tg-emoji emoji-id="6064229565499182127">📚</tg-emoji>',
            "Zeus": '<tg-emoji emoji-id="6062297027784480121">🔵</tg-emoji>',
            "Kunkka": '<tg-emoji emoji-id="6062241455202635774">🔴</tg-emoji>',
            "Lina": '<tg-emoji emoji-id="6064308803350826942">🔵</tg-emoji>',
            "Lion": '<tg-emoji emoji-id="6064289772350737513">🔵</tg-emoji>',
            "Shadow Shaman": '<tg-emoji emoji-id="6064493624383508136">🔵</tg-emoji>',
            "Slardar": '<tg-emoji emoji-id="6062362513150843237">🔴</tg-emoji>',
            "Tidehunter": '<tg-emoji emoji-id="6064434495568743878">🔴</tg-emoji>',
            "Witch Doctor": '<tg-emoji emoji-id="6064291872589746598">🔵</tg-emoji>',
            "Lich": '<tg-emoji emoji-id="6062058639919682717">🔵</tg-emoji>',
            "Riki": '<tg-emoji emoji-id="6062018357421412977">🟢</tg-emoji>',
            "Enigma": '<tg-emoji emoji-id="6062003333625811037">📚</tg-emoji>',
            "Tinker": '<tg-emoji emoji-id="6062141403939475826">🔵</tg-emoji>',
            "Sniper": '<tg-emoji emoji-id="6064553891364605714">🟢</tg-emoji>',
            "Necrophos": '<tg-emoji emoji-id="6062095984660319884">🔵</tg-emoji>',
            "Warlock": '<tg-emoji emoji-id="6062060237647516154">🔵</tg-emoji>',
            "Beastmaster": '<tg-emoji emoji-id="6062239913309376880">📚</tg-emoji>',
            "Queen of Pain": '<tg-emoji emoji-id="6064401802277686782">🔵</tg-emoji>',
            "Venomancer": '<tg-emoji emoji-id="6062083580794772209">📚</tg-emoji>',
            "Faceless Void": '<tg-emoji emoji-id="6061881588482838965">🟢</tg-emoji>',
            "Wraith King": '<tg-emoji emoji-id="6064260386184499015">🔴</tg-emoji>',
            "Death Prophet": '<tg-emoji emoji-id="6064637574507400571">🔵</tg-emoji>',
            "Phantom Assassin": '<tg-emoji emoji-id="6064314197829751274">🟢</tg-emoji>',
            "Pugna": '<tg-emoji emoji-id="6062085620904235332">🔵</tg-emoji>',
            "Templar Assassin": '<tg-emoji emoji-id="6064522215980797912">🟢</tg-emoji>',
            "Viper": '<tg-emoji emoji-id="6061862059266544998">🟢</tg-emoji>',
            "Luna": '<tg-emoji emoji-id="6064138744120741611">🟢</tg-emoji>',
            "Dragon Knight": '<tg-emoji emoji-id="6061964279488188460">🔴</tg-emoji>',
            "Dazzle": '<tg-emoji emoji-id="6062278211532755233">📚</tg-emoji>',
            "Clockwerk": '<tg-emoji emoji-id="6064468047853260553">📚</tg-emoji>',
            "Leshrac": '<tg-emoji emoji-id="6064245985159155473">🔵</tg-emoji>',
            "Nature's Prophet": '<tg-emoji emoji-id="6064634018274485796">🔵</tg-emoji>',
            "Lifestealer": '<tg-emoji emoji-id="6062018963011801353">🔴</tg-emoji>',
            "Dark Seer": '<tg-emoji emoji-id="6062398247278744408">📚</tg-emoji>',
            "Clinkz": '<tg-emoji emoji-id="6064101545408991778">🟢</tg-emoji>',
            "Omniknight": '<tg-emoji emoji-id="6061980239586660582">🔴</tg-emoji>',
            "Enchantress": '<tg-emoji emoji-id="6061974132143166052">🔵</tg-emoji>',
            "Huskar": '<tg-emoji emoji-id="6062174595446739362">🔴</tg-emoji>',
            "Night Stalker": '<tg-emoji emoji-id="6061937216899256550">🔴</tg-emoji>',
            "Broodmother": '<tg-emoji emoji-id="6062384902815354947">📚</tg-emoji>',
            "Bounty Hunter": '<tg-emoji emoji-id="6064255494216748369">🟢</tg-emoji>',
            "Weaver": '<tg-emoji emoji-id="6062351603933909860">🟢</tg-emoji>',
            "Jakiro": '<tg-emoji emoji-id="6062211179978166339">🔵</tg-emoji>',
            "Batrider": '<tg-emoji emoji-id="6064421267069472479">📚</tg-emoji>',
            "Chen": '<tg-emoji emoji-id="6064294763102736140">📚</tg-emoji>',
            "Spectre": '<tg-emoji emoji-id="6061877302105477141">🟢</tg-emoji>',
            "Doom": '<tg-emoji emoji-id="6062238092243243286">🔴</tg-emoji>',
            "Ancient Apparition": '<tg-emoji emoji-id="6062298535318000351">🔵</tg-emoji>',
            "Ursa": '<tg-emoji emoji-id="6061953550659883060">🟢</tg-emoji>',
            "Spirit Breaker": '<tg-emoji emoji-id="6062212988159398402">🔴</tg-emoji>',
            "Gyrocopter": '<tg-emoji emoji-id="6062215659629061561">🟢</tg-emoji>',
            "Alchemist": '<tg-emoji emoji-id="6061874604866015790">🔴</tg-emoji>',
            "Silencer": '<tg-emoji emoji-id="6062244603413664044">🔵</tg-emoji>',
            "Outworld Destroyer": '<tg-emoji emoji-id="6064612483308457397">🔵</tg-emoji>',
            "Lycan": '<tg-emoji emoji-id="6064375495602999258">📚</tg-emoji>',
            "Brewmaster": '<tg-emoji emoji-id="6061862883900264920">📚</tg-emoji>',
            "Shadow Demon": '<tg-emoji emoji-id="6062334733302370465">🔵</tg-emoji>',
            "Lone Druid": '<tg-emoji emoji-id="6064222487393078839">📚</tg-emoji>',
            "Chaos Knight": '<tg-emoji emoji-id="6062017154830570512">🔴</tg-emoji>',
            "Meepo": '<tg-emoji emoji-id="6062221629633599535">🟢</tg-emoji>',
            "Treant Protector": '<tg-emoji emoji-id="6062215127053111729">🔴</tg-emoji>',
            "Ogre Magi": '<tg-emoji emoji-id="6061878204048609835">🔴</tg-emoji>',
            "Undying": '<tg-emoji emoji-id="6064609433881678147">🔴</tg-emoji>',
            "Rubick": '<tg-emoji emoji-id="6062239977733886601">🔵</tg-emoji>',
            "Disruptor": '<tg-emoji emoji-id="6064448153564745401">🔵</tg-emoji>',
            "Nyx Assassin": '<tg-emoji emoji-id="6061919702022622872">📚</tg-emoji>',
            "Naga Siren": '<tg-emoji emoji-id="6061868110875463788">🟢</tg-emoji>',
            "Keeper of the Light": '<tg-emoji emoji-id="6064394346214461058">🔵</tg-emoji>',
            "Io": '<tg-emoji emoji-id="6062230820863611549">📚</tg-emoji>',
            "Visage": '<tg-emoji emoji-id="6062254202665569743">📚</tg-emoji>',
            "Slark": '<tg-emoji emoji-id="6062168303319650843">🟢</tg-emoji>',
            "Medusa": '<tg-emoji emoji-id="6062362427251495358">🟢</tg-emoji>',
            "Troll Warlord": '<tg-emoji emoji-id="6064360695145697016">🟢</tg-emoji>',
            "Centaur Warrunner": '<tg-emoji emoji-id="6062097041222274851">🔴</tg-emoji>',
            "Magnus": '<tg-emoji emoji-id="6064496922918391606">📚</tg-emoji>',
            "Timbersaw": '<tg-emoji emoji-id="6064568103411388841">🔴</tg-emoji>',
            "Bristleback": '<tg-emoji emoji-id="6061862102216217916">🔴</tg-emoji>',
            "Tusk": '<tg-emoji emoji-id="6062111506672128077">🔴</tg-emoji>',
            "Skywrath Mage": '<tg-emoji emoji-id="6064350679281962923">🔵</tg-emoji>',
            "Abaddon": '<tg-emoji emoji-id="6064623817727152506">📚</tg-emoji>',
            "Elder Titan": '<tg-emoji emoji-id="6062004720900247816">🔴</tg-emoji>',
            "Legion Commander": '<tg-emoji emoji-id="6062003041568037236">🔴</tg-emoji>',
            "Techies": '<tg-emoji emoji-id="6064194488501276422">📚</tg-emoji>',
            "Ember Spirit": '<tg-emoji emoji-id="6062314413812098321">🟢</tg-emoji>',
            "Earth Spirit": '<tg-emoji emoji-id="6061952988019167874">🔴</tg-emoji>',
            "Underlord": '<tg-emoji emoji-id="6062200060307836531">🔴</tg-emoji>',
            "Terrorblade": '<tg-emoji emoji-id="6064443330316472109">🟢</tg-emoji>',
            "Phoenix": '<tg-emoji emoji-id="6062297770813821507">📚</tg-emoji>',
            "Oracle": '<tg-emoji emoji-id="6062071215583924862">🔵</tg-emoji>',
            "Winter Wyvern": '<tg-emoji emoji-id="6062264639436100075">📚</tg-emoji>',
            "Arc Warden": '<tg-emoji emoji-id="6062221122827456836">🟢</tg-emoji>',
            "Monkey King": '<tg-emoji emoji-id="6062069394517791133">🟢</tg-emoji>',
            "Dark Willow": '<tg-emoji emoji-id="6064600805292379746">📚</tg-emoji>',
            "Pangolier": '<tg-emoji emoji-id="6061906576602568469">📚</tg-emoji>',
            "Grimstroke": '<tg-emoji emoji-id="6061874050815234471">🔵</tg-emoji>',
            "Hoodwink": '<tg-emoji emoji-id="6062098656129979353">🟢</tg-emoji>',
            "Void Spirit": '<tg-emoji emoji-id="6064163289858838043">📚</tg-emoji>',
            "Snapfire": '<tg-emoji emoji-id="6062098398431940095">📚</tg-emoji>',
            "Mars": '<tg-emoji emoji-id="6062056565450477147">🔴</tg-emoji>',
            "Dawnbreaker": '<tg-emoji emoji-id="6062338388319540368">🔴</tg-emoji>',
            "Marci": '<tg-emoji emoji-id="6062225477924295349">📚</tg-emoji>',
            "Primal Beast": '<tg-emoji emoji-id="6062167156563384847">🔴</tg-emoji>',
            "Muerta": '<tg-emoji emoji-id="6061974394136171083">🔵</tg-emoji>',
            "Largo": '<tg-emoji emoji-id="6269259626194150042">🐸</tg-emoji>',
            "Kez": '<tg-emoji emoji-id="5442844181129104405">🤩</tg-emoji>',
            "Ringmaster": '<tg-emoji emoji-id="6269209104493845341">🤡</tg-emoji>',

            
        }

        self.hero_emojis2 = {
            "Anti-Mage": '<emoji document_id=6062179938386055768>🟢</emoji>',
            "Axe": '<emoji document_id=6061943874098564891>🔴</emoji>',
            "Juggernaut": '<emoji document_id=6064624766914924449>🟢</emoji>',
            "Pudge": '<emoji document_id=6062065073780690927>🔴</emoji>',
            "Invoker": '<emoji document_id=6062314229128499676>📚</emoji>',
            "Bane": '<emoji document_id=6062010952897793745>📚</emoji>',
            "Bloodseeker": '<emoji document_id=6062032122791598368>🟢</emoji>',
            "Crystal Maiden": '<emoji document_id=6064219008469569795>🔵</emoji>',
            "Drow Ranger": '<emoji document_id=6061854143641816935>🟢</emoji>',
            "Earthshaker": '<emoji document_id=6062153554401955565>🔴</emoji>',
            "Mirana": '<emoji document_id=6062297886777937723>🟢</emoji>',
            "Morphling": '<emoji document_id=6064443858597449152>🟢</emoji>',
            "Shadow Fiend": '<emoji document_id=6064205264574222013>🟢</emoji>',
            "Phantom Lancer": '<emoji document_id=6061901993872462041>🟢</emoji>',
            "Puck": '<emoji document_id=6062166374879335422>🔵</emoji>',
            "Razor": '<emoji document_id=6062104175162954182>🟢</emoji>',
            "Sand King": '<emoji document_id=6064151371324592043>📚</emoji>',
            "Storm Spirit": '<emoji document_id=6061887283609474004>🔵</emoji>',
            "Sven": '<emoji document_id=6062262753945457249>🔴</emoji>',
            "Tiny": '<emoji document_id=6061984912511078154>🔴</emoji>',
            "Vengeful Spirit": '<emoji document_id=6064293105245359489>📚</emoji>',
            "Windranger": '<emoji document_id=6064229565499182127>📚</emoji>',
            "Zeus": '<emoji document_id=6062297027784480121>🔵</emoji>',
            "Kunkka": '<emoji document_id=6062241455202635774>🔴</emoji>',
            "Lina": '<emoji document_id=6064308803350826942>🔵</emoji>',
            "Lion": '<emoji document_id=6064289772350737513>🔵</emoji>',
            "Shadow Shaman": '<emoji document_id=6064493624383508136>🔵</emoji>',
            "Slardar": '<emoji document_id=6062362513150843237>🔴</emoji>',
            "Tidehunter": '<emoji document_id=6064434495568743878>🔴</emoji>',
            "Witch Doctor": '<emoji document_id=6064291872589746598>🔵</emoji>',
            "Lich": '<emoji document_id=6062058639919682717>🔵</emoji>',
            "Riki": '<emoji document_id=6062018357421412977>🟢</emoji>',
            "Enigma": '<emoji document_id=6062003333625811037>📚</emoji>',
            "Tinker": '<emoji document_id=6062141403939475826>🔵</emoji>',
            "Sniper": '<emoji document_id=6064553891364605714>🟢</emoji>',
            "Necrophos": '<emoji document_id=6062095984660319884>🔵</emoji>',
            "Warlock": '<emoji document_id=6062060237647516154>🔵</emoji>',
            "Beastmaster": '<emoji document_id=6062239913309376880>📚</emoji>',
            "Queen of Pain": '<emoji document_id=6064401802277686782>🔵</emoji>',
            "Venomancer": '<emoji document_id=6062083580794772209>📚</emoji>',
            "Faceless Void": '<emoji document_id=6061881588482838965>🟢</emoji>',
            "Wraith King": '<emoji document_id=6064260386184499015>🔴</emoji>',
            "Death Prophet": '<emoji document_id=6064637574507400571>🔵</emoji>',
            "Phantom Assassin": '<emoji document_id=6064314197829751274>🟢</emoji>',
            "Pugna": '<emoji document_id=6062085620904235332>🔵</emoji>',
            "Templar Assassin": '<emoji document_id=6064522215980797912>🟢</emoji>',
            "Viper": '<emoji document_id=6061862059266544998>🟢</emoji>',
            "Luna": '<emoji document_id=6064138744120741611>🟢</emoji>',
            "Dragon Knight": '<emoji document_id=6061964279488188460>🔴</emoji>',
            "Dazzle": '<emoji document_id=6062278211532755233>📚</emoji>',
            "Clockwerk": '<emoji document_id=6064468047853260553>📚</emoji>',
            "Leshrac": '<emoji document_id=6064245985159155473>🔵</emoji>',
            "Nature's Prophet": '<emoji document_id=6064634018274485796>🔵</emoji>',
            "Lifestealer": '<emoji document_id=6062018963011801353>🔴</emoji>',
            "Dark Seer": '<emoji document_id=6062398247278744408>📚</emoji>',
            "Clinkz": '<emoji document_id=6064101545408991778>🟢</emoji>',
            "Omniknight": '<emoji document_id=6061980239586660582>🔴</emoji>',
            "Enchantress": '<emoji document_id=6061974132143166052>🔵</emoji>',
            "Huskar": '<emoji document_id=6062174595446739362>🔴</emoji>',
            "Night Stalker": '<emoji document_id=6061937216899256550>🔴</emoji>',
            "Broodmother": '<emoji document_id=6062384902815354947>📚</emoji>',
            "Bounty Hunter": '<emoji document_id=6064255494216748369>🟢</emoji>',
            "Weaver": '<emoji document_id=6062351603933909860>🟢</emoji>',
            "Jakiro": '<emoji document_id=6062211179978166339>🔵</emoji>',
            "Batrider": '<emoji document_id=6064421267069472479>📚</emoji>',
            "Chen": '<emoji document_id=6064294763102736140>📚</emoji>',
            "Spectre": '<emoji document_id=6061877302105477141>🟢</emoji>',
            "Doom": '<emoji document_id=6062238092243243286>🔴</emoji>',
            "Ancient Apparition": '<emoji document_id=6062298535318000351>🔵</emoji>',
            "Ursa": '<emoji document_id=6061953550659883060>🟢</emoji>',
            "Spirit Breaker": '<emoji document_id=6062212988159398402>🔴</emoji>',
            "Gyrocopter": '<emoji document_id=6062215659629061561>🟢</emoji>',
            "Alchemist": '<emoji document_id=6061874604866015790>🔴</emoji>',
            "Silencer": '<emoji document_id=6062244603413664044>🔵</emoji>',
            "Outworld Destroyer": '<emoji document_id=6064612483308457397>🔵</emoji>',
            "Lycan": '<emoji document_id=6064375495602999258>📚</emoji>',
            "Brewmaster": '<emoji document_id=6061862883900264920>📚</emoji>',
            "Shadow Demon": '<emoji document_id=6062334733302370465>🔵</emoji>',
            "Lone Druid": '<emoji document_id=6064222487393078839>📚</emoji>',
            "Chaos Knight": '<emoji document_id=6062017154830570512>🔴</emoji>',
            "Meepo": '<emoji document_id=6062221629633599535>🟢</emoji>',
            "Treant Protector": '<emoji document_id=6062215127053111729>🔴</emoji>',
            "Ogre Magi": '<emoji document_id=6061878204048609835>🔴</emoji>',
            "Undying": '<emoji document_id=6064609433881678147>🔴</emoji>',
            "Rubick": '<emoji document_id=6062239977733886601>🔵</emoji>',
            "Disruptor": '<emoji document_id=6064448153564745401>🔵</emoji>',
            "Nyx Assassin": '<emoji document_id=6061919702022622872>📚</emoji>',
            "Naga Siren": '<emoji document_id=6061868110875463788>🟢</emoji>',
            "Keeper of the Light": '<emoji document_id=6064394346214461058>🔵</emoji>',
            "Io": '<emoji document_id=6062230820863611549>📚</emoji>',
            "Visage": '<emoji document_id=6062254202665569743>📚</emoji>',
            "Slark": '<emoji document_id=6062168303319650843>🟢</emoji>',
            "Medusa": '<emoji document_id=6062362427251495358>🟢</emoji>',
            "Troll Warlord": '<emoji document_id=6064360695145697016>🟢</emoji>',
            "Centaur Warrunner": '<emoji document_id=6062097041222274851>🔴</emoji>',
            "Magnus": '<emoji document_id=6064496922918391606>📚</emoji>',
            "Timbersaw": '<emoji document_id=6064568103411388841>🔴</emoji>',
            "Bristleback": '<emoji document_id=6061862102216217916>🔴</emoji>',
            "Tusk": '<emoji document_id=6062111506672128077>🔴</emoji>',
            "Skywrath Mage": '<emoji document_id=6064350679281962923>🔵</emoji>',
            "Abaddon": '<emoji document_id=6064623817727152506>📚</emoji>',
            "Elder Titan": '<emoji document_id=6062004720900247816>🔴</emoji>',
            "Legion Commander": '<emoji document_id=6062003041568037236>🔴</emoji>',
            "Techies": '<emoji document_id=6064194488501276422>📚</emoji>',
            "Ember Spirit": '<emoji document_id=6062314413812098321>🟢</emoji>',
            "Earth Spirit": '<emoji document_id=6061952988019167874>🔴</emoji>',
            "Underlord": '<emoji document_id=6062200060307836531>🔴</emoji>',
            "Terrorblade": '<emoji document_id=6064443330316472109>🟢</emoji>',
            "Phoenix": '<emoji document_id=6062297770813821507>📚</emoji>',
            "Oracle": '<emoji document_id=6062071215583924862>🔵</emoji>',
            "Winter Wyvern": '<emoji document_id=6062264639436100075>📚</emoji>',
            "Arc Warden": '<emoji document_id=6062221122827456836>🟢</emoji>',
            "Monkey King": '<emoji document_id=6062069394517791133>🟢</emoji>',
            "Dark Willow": '<emoji document_id=6064600805292379746>📚</emoji>',
            "Pangolier": '<emoji document_id=6061906576602568469>📚</emoji>',
            "Grimstroke": '<emoji document_id=6061874050815234471>🔵</emoji>',
            "Hoodwink": '<emoji document_id=6062098656129979353>🟢</emoji>',
            "Void Spirit": '<emoji document_id=6064163289858838043>📚</emoji>',
            "Snapfire": '<emoji document_id=6062098398431940095>📚</emoji>',
            "Mars": '<emoji document_id=6062056565450477147>🔴</emoji>',
            "Dawnbreaker": '<emoji document_id=6062338388319540368>🔴</emoji>',
            "Marci": '<emoji document_id=6062225477924295349>📚</emoji>',
            "Primal Beast": '<emoji document_id=6062167156563384847>🔴</emoji>',
            "Muerta": '<emoji document_id=6061974394136171083>🔵</emoji>',
            "Largo": '<emoji document_id=6269259626194150042>🐸</emoji>',
            "Kez": '<emoji document_id=5442844181129104405>🤩</emoji>',
            "Ringmaster": '<emoji document_id=6269209104493845341>🤡</emoji>',
            
        }
        self._load_heroes()
        self._load_items()

    # 🔥 сюда добавляем метод конвертации SteamID -> account_id
    def _to_account_id(self, steam_id64: int) -> int:
        return steam_id64 - 76561197960265728

    def _to_account_id(self, raw_id: int) -> int:
        return raw_id - 76561197960265728 if raw_id > 76561197960265728 else raw_id


    def _load_heroes(self):
        heroes_data = [
            {"name": "Anti-Mage", "is_radiant": True, "id": 1},
            {"name": "Axe", "is_radiant": False, "id": 2},
            {"name": "Invoker", "is_radiant": True, "id": 3},
            {"name": "Pudge", "is_radiant": False, "id": 4},
            {"name": "Invoker", "is_radiant": True, "id": 5},
            {"name": "Bane", "is_radiant": False, "id": 6},
            {"name": "Bloodseeker", "is_radiant": True, "id": 7},
            {"name": "Crystal Maiden", "is_radiant": False, "id": 8},
            {"name": "Drow Ranger", "is_radiant": True, "id": 9},
            {"name": "Earthshaker", "is_radiant": False, "id": 10},
            {"name": "Mirana", "is_radiant": True, "id": 11}, 
            {"name": "Morphling", "is_radiant": False, "id": 12},
            {"name": "Shadow Fiend", "is_radiant": True, "id": 13},
            {"name": "Phantom Lancer", "is_radiant": False, "id": 14},
            {"name": "Puck", "is_radiant": True, "id": 15},
            {"name": "Razor", "is_radiant": False, "id": 16},
            {"name": "Sand King", "is_radiant": True, "id": 17},
            {"name": "Storm Spirit", "is_radiant": False, "id": 18},
            {"name": "Sven", "is_radiant": True, "id": 19},
            {"name": "Tiny", "is_radiant": False, "id": 20},
            {"name": "Vengeful Spirit", "is_radiant": True, "id": 21},
            {"name": "Windranger", "is_radiant": False, "id": 22},
            {"name": "Zeus", "is_radiant": True, "id": 23},
            {"name": "Kunkka", "is_radiant": False, "id": 24},
            {"name": "Lina", "is_radiant": True, "id": 25},
            {"name": "Lion", "is_radiant": False, "id": 26},
            {"name": "Shadow Shaman", "is_radiant": True, "id": 27},
            {"name": "Slardar", "is_radiant": False, "id": 28},
            {"name": "Tidehunter", "is_radiant": True, "id": 29},
            {"name": "Witch Doctor", "is_radiant": False, "id": 30},
            {"name": "Lich", "is_radiant": True, "id": 31},
            {"name": "Riki", "is_radiant": False, "id": 32},
            {"name": "Enigma", "is_radiant": True, "id": 33},
            {"name": "Tinker", "is_radiant": False, "id": 34},
            {"name": "Sniper", "is_radiant": True, "id": 35},
            {"name": "Necrophos", "is_radiant": False, "id": 36},
            {"name": "Warlock", "is_radiant": True, "id": 37},
            {"name": "Beastmaster", "is_radiant": False, "id": 38},
            {"name": "Queen of Pain", "is_radiant": True, "id": 39},
            {"name": "Venomancer", "is_radiant": False, "id": 40},
            {"name": "Faceless Void", "is_radiant": True, "id": 41},
            {"name": "Wraith King", "is_radiant": False, "id": 42},
            {"name": "Death Prophet", "is_radiant": True, "id": 43},
            {"name": "Phantom Assassin", "is_radiant": False, "id": 44},
            {"name": "Pugna", "is_radiant": True, "id": 45},
            {"name": "Templar Assassin", "is_radiant": False, "id": 46},
            {"name": "Viper", "is_radiant": True, "id": 47},
            {"name": "Luna", "is_radiant": False, "id": 48},
            {"name": "Dragon Knight", "is_radiant": True, "id": 49},
            {"name": "Dazzle", "is_radiant": False, "id": 50},
            {"name": "Clockwerk", "is_radiant": True, "id": 51},
            {"name": "Leshrac", "is_radiant": False, "id": 52},
            {"name": "Nature's Prophet", "is_radiant": True, "id": 53},
            {"name": "Lifestealer", "is_radiant": False, "id": 54},
            {"name": "Dark Seer", "is_radiant": True, "id": 55},
            {"name": "Clinkz", "is_radiant": False, "id": 56},
            {"name": "Omniknight", "is_radiant": True, "id": 57},
            {"name": "Enchantress", "is_radiant": False, "id": 58},
            {"name": "Huskar", "is_radiant": True, "id": 59},
            {"name": "Night Stalker", "is_radiant": False, "id": 60},
            {"name": "Broodmother", "is_radiant": True, "id": 61},
            {"name": "Bounty Hunter", "is_radiant": False, "id": 62},
            {"name": "Weaver", "is_radiant": True, "id": 63},
            {"name": "Jakiro", "is_radiant": False, "id": 64},
            {"name": "Batrider", "is_radiant": True, "id": 65},
            {"name": "Chen", "is_radiant": False, "id": 66},
            {"name": "Spectre", "is_radiant": True, "id": 67},
            {"name": "Doom", "is_radiant": False, "id": 68},
            {"name": "Ancient Apparition", "is_radiant": True, "id": 69},
            {"name": "Ursa", "is_radiant": False, "id": 70},
            {"name": "Spirit Breaker", "is_radiant": True, "id": 71},
            {"name": "Gyrocopter", "is_radiant": False, "id": 72},
            {"name": "Alchemist", "is_radiant": True, "id": 73},
            {"name": "Silencer", "is_radiant": False, "id": 74},
            {"name": "Outworld Destroyer", "is_radiant": True, "id": 75},
            {"name": "Lycan", "is_radiant": False, "id": 76},
            {"name": "Brewmaster", "is_radiant": True, "id": 77},
            {"name": "Shadow Demon", "is_radiant": False, "id": 78},
            {"name": "Lone Druid", "is_radiant": True, "id": 79},
            {"name": "Chaos Knight", "is_radiant": False, "id": 80},
            {"name": "Meepo", "is_radiant": True, "id": 81},
            {"name": "Treant Protector", "is_radiant": False, "id": 82},
            {"name": "Ogre Magi", "is_radiant": True, "id": 83},
            {"name": "Undying", "is_radiant": False, "id": 84},
            {"name": "Rubick", "is_radiant": True, "id": 85},
            {"name": "Disruptor", "is_radiant": False, "id": 86},
            {"name": "Nyx Assassin", "is_radiant": True, "id": 87},
            {"name": "Naga Siren", "is_radiant": False, "id": 88},
            {"name": "Keeper of the Light", "is_radiant": True, "id": 89},
            {"name": "Io", "is_radiant": False, "id": 90},
            {"name": "Visage", "is_radiant": True, "id": 91},
            {"name": "Slark", "is_radiant": False, "id": 92},
            {"name": "Medusa", "is_radiant": True, "id": 93},
            {"name": "Troll Warlord", "is_radiant": False, "id": 94},
            {"name": "Centaur Warrunner", "is_radiant": True, "id": 95},
            {"name": "Magnus", "is_radiant": False, "id": 96},
            {"name": "Timbersaw", "is_radiant": True, "id": 97},
            {"name": "Bristleback", "is_radiant": False, "id": 98},
            {"name": "Tusk", "is_radiant": True, "id": 99},
            {"name": "Skywrath Mage", "is_radiant": False, "id": 100},
            {"name": "Abaddon", "is_radiant": True, "id": 101},
            {"name": "Elder Titan", "is_radiant": False, "id": 102},
            {"name": "Legion Commander", "is_radiant": True, "id": 103},
            {"name": "Techies", "is_radiant": False, "id": 104},
            {"name": "Ember Spirit", "is_radiant": True, "id": 105},
            {"name": "Earth Spirit", "is_radiant": False, "id": 106},
            {"name": "Underlord", "is_radiant": True, "id": 107},
            {"name": "Terrorblade", "is_radiant": False, "id": 108},
            {"name": "Phoenix", "is_radiant": True, "id": 109},
            {"name": "Oracle", "is_radiant": False, "id": 110},
            {"name": "Winter Wyvern", "is_radiant": True, "id": 111},
            {"name": "Arc Warden", "is_radiant": False, "id": 112},
            {"name": "Monkey King", "is_radiant": True, "id": 113},
            {"name": "Dark Willow", "is_radiant": False, "id": 114},
            {"name": "Pangolier", "is_radiant": True, "id": 115},
            {"name": "Grimstroke", "is_radiant": False, "id": 116},
            {"name": "Hoodwink", "is_radiant": True, "id": 117},
            {"name": "Void Spirit", "is_radiant": False, "id": 118},
            {"name": "Snapfire", "is_radiant": True, "id": 119},
            {"name": "Mars", "is_radiant": False, "id": 120},
            {"name": "Dawnbreaker", "is_radiant": True, "id": 121},
            {"name": "Marci", "is_radiant": False, "id": 122},
            {"name": "Primal Beast", "is_radiant": True, "id": 123},
            {"name": "Muerta", "is_radiant": False, "id": 124},
            {"name": "Largo", "is_radiant": True, "id": 125},
            {"name": "Kez", "is_radiant": False, "id": 126},
            {"name": "Ringmaster", "is_radiant": True, "id": 127},

        ]

        for data in heroes_data:
            emoji = self.hero_emojis.get(data["name"], "❓")
            self.heroes[data["id"]] = {"name": data["name"], "emoji": emoji}


    async def close_msg(self, call):
        try:
            await call.delete()
        except Exception as e:
            await call.answer(f"Не получилось удалить сообщение 😡\n{e}", alert=True)

    
        





    # ---------------- Загрузка данных ----------------
    def _load_heroes(self):
        try:
            resp = requests.get(f"{API_URL}/heroes")
            data = resp.json()
            self.heroes = {h["id"]: h["localized_name"] for h in data}
        except Exception as e:
            print(f"[DotaStats] Ошибка загрузки героев: {e}")
            self.heroes = {}

    def _load_items(self):
        try:
            resp = requests.get(f"{API_URL}/constants/items")
            data = resp.json()
            self.items = {v["id"]: k.replace("_", " ").title() for k, v in data.items() if "id" in v}
        except Exception as e:
            print(f"[DotaStats] Ошибка загрузки предметов: {e}")
            self.items = {}

    # ---------------- Форматирование времени ----------------
    def _format_match_time(self, start_time: int) -> str:
        """Форматирует время матча в читаемый формат"""
        try:
            match_time = datetime.fromtimestamp(start_time, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            time_diff = now - match_time
            
            if time_diff.days > 0:
                if time_diff.days == 1:
                    return f"1 день назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
                else:
                    return f"{time_diff.days} дней назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
            elif time_diff.seconds >= 3600:
                hours = time_diff.seconds // 3600
                if hours == 1:
                    return f"1 час назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
                else:
                    return f"{hours} часов назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
            elif time_diff.seconds >= 60:
                minutes = time_diff.seconds // 60
                if minutes == 1:
                    return f"1 минуту назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
                else:
                    return f"{minutes} минут назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
            else:
                return f"только что ({match_time.strftime('%d.%m.%Y %H:%M')})"
        except Exception as e:
            print(f"[DotaStats] Ошибка форматирования времени: {e}")
            return "неизвестно"

    # ---------------- Профиль ----------------
    async def profile2cmd(self, message: Message):
        """Показать свой профиль"""
        pid = self.config["PLAYER_ID"]
        if not pid:
            return await utils.answer(message, "<emoji document_id=5390972675684337321>🤐</emoji> Не задан Steam ID")
        await self._send_profile(message, pid)

    async def profileidcmd(self, message: Message):
        """Показать профиль по Steam ID"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            return await utils.answer(message, "Используй: .profileid <id>")
        await self._send_profile(message, args)

    async def _send_profile(self, message: Message, pid: str):
        try:
            r = requests.get(f"{API_URL}/players/{pid}").json()
            profile = r.get("profile", {})

            # Получаем статистику побед/поражений
            wl = requests.get(f"{API_URL}/players/{pid}/wl").json()
            win, lose = wl.get("win", 0), wl.get("lose", 0)
            total = win + lose
            wr = round(win / total * 100, 2) if total > 0 else 0

            # Обработка ранга
            rank_tier = r.get("rank_tier")
            leaderboard_rank = r.get("leaderboard_rank")
            rank_names = {
                1: "Herald", 2: "Guardian", 3: "Crusader", 4: "Archon",
                5: "Legend", 6: "Ancient", 7: "Divine", 8: "Immortal",
            }
            
            rank_info = "Неизвестно"
            rank_icon = ""
            if rank_tier:
                major = rank_tier // 10
                minor = rank_tier % 10
                rank_name = rank_names.get(major, "Неизвестно")
                rank_icon = self.rank_emojis.get(rank_name, "")
                if major < 8:
                    rank_info = f"{rank_name} {minor} {rank_icon}"
                else:
                    if leaderboard_rank:
                        rank_info = f"{rank_name} (Топ {leaderboard_rank}) {rank_icon}"
                    else:
                        rank_info = f"{rank_name} {rank_icon}"


            # Формируем сообщение со ВСЕЙ информацией
            msg = (
                f"<blockquote><emoji document_id=5235611059909323996>⭐️</emoji> Профиль: {profile.get('personaname', 'Unknown')}</blockquote>\n"
                f"<blockquote><emoji document_id=5422683699130933153>🪪</emoji> Steam ID: {pid}</blockquote>\n"
                f"<blockquote><emoji document_id=5456498809875995940>🏆</emoji> Ранг: {rank_info}</blockquote>\n"
                f"<blockquote><emoji document_id=5429381339851796035>✅</emoji> Победы: {win}</blockquote>\n"
                f"<blockquote><emoji document_id=5465225015190367274>👎</emoji> Поражения: {lose}</blockquote>\n"
                f"<blockquote><emoji document_id=5364265190353286344>📊</emoji> Винрейт: {wr}%</blockquote>\n"
            )
            await utils.answer(message, msg, parse_mode="html")
        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5390972675684337321>🤐</emoji> Ошибка загрузки профиля: {str(e)}")

    # ---------------- Последние игры ----------------
    async def dota2cmd(self, message: Message):
        """Показать последние 40 игр"""
        pid = self.config["PLAYER_ID"]
        if not pid:
            return await utils.answer(message, "<emoji document_id=5390972675684337321>🤐</emoji> Не задан Steam ID")

        try:
            matches = requests.get(f"{API_URL}/players/{pid}/matches?Limit=40").json()
            if not matches:
                return await utils.answer(message, "<emoji document_id=5390972675684337321>🤐</emoji> Нет данных матчей")

            matches = matches[:40]

            pages = self._build_pages(matches)

            msg = await utils.answer(
                message,
                pages[0],
                reply_markup=self._pagination_markup(0, len(pages))
            )
            
            self._pages_cache[msg.inline_message_id] = pages

        except Exception as e:
            return await utils.answer(message, f"Ошибка: {e}")


    # ---------------- Последние игры по ID ----------------
    async def dota2idcmd(self, message: Message):
        """Показать последние 40 игр по Steam ID"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            return await utils.answer(
                message,
                "<emoji document_id=5390972675684337321>🤐</emoji> Используй: .dota2id <steam_id>"
            )

        raw_id = int(args)

        # 🔥 Конвертация Steam64 → Steam32
        if raw_id > 76561197960265728:
            pid = raw_id - 76561197960265728
        else:
            pid = raw_id

        try:
            matches = requests.get(f"{API_URL}/players/{pid}/matches?Limit=40").json()
            if not matches:
                return await utils.answer(
                    message,
                    "<emoji document_id=5390972675684337321>🤐</emoji> Нет данных матчей (профиль скрыт или нет игр)"
                )

            msg = (
                "<emoji document_id=5319120041780726017>🎮</emoji> "
                f"<b>Последние 40 игр игрока {pid}:</b>\n\n"
            )

            matches = matches [:40]

            pages = self._build_pages(matches)

            msg = await utils.answer(
                message,
                pages[0],
                reply_markup=self._pagination_markup(0, len(pages))
            )

            self._pages_cache[msg.inline_message_id] = pages


        except Exception as e:
            return await utils.answer(message, f"Ошибка: {e}")



    # ---------------- Детали матча ----------------
    async def matchcmd(self, message: Message):
        """Показать подробности матча по ID"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            return await utils.answer(message, "Используй: .match <id>")
        await self._send_match_info(message, args)

    async def _send_match_info(self, message: Message, match_id: str):
        try:
            r = requests.get(f"{API_URL}/matches/{match_id}").json()
            if "match_id" not in r:
                return await utils.answer(message, "<emoji document_id=5390972675684337321>🤐</emoji> Матч не найден")

            duration = f"{r['duration'] // 60}:{r['duration'] % 60:02d}"
            radiant_win = r.get("radiant_win", False)
            result = "<emoji document_id=5368338090660209672>🌿</emoji> Radiant Победа" if radiant_win else "<emoji document_id=5397751602956239123>🔥</emoji> Dire Победа"

            radiant, dire = [], []
            for p in r.get("players", []):
                hero_name = self.heroes.get(p["hero_id"], f"Unknown({p['hero_id']})")
                hero_icon = self.hero_emojis2.get(hero_name, "")
                kda = f"{p['kills']}/{p['deaths']}/{p['assists']}"
                gpm, xpm, net = p.get("gold_per_min", 0), p.get("xp_per_min", 0), p.get("total_gold", 0)
                account_id = p.get("account_id", "N/A")

                # 🎒 Предметы
                item_ids = [
                    p.get("item_0"), p.get("item_1"), p.get("item_2"),
                    p.get("item_3"), p.get("item_4"), p.get("item_5")
                ]
                items_str = []
                for iid in item_ids:
                    if iid in self.items:
                        item_name = self.items[iid]
                        item_icon = self.item_emojis.get(item_name, "🧩")
                        items_str.append(f"{item_icon} {item_name}")
                items_str = " | ".join(items_str) if items_str else "Нет предметов"

                line = (
                    f"- {hero_name} {hero_icon} | {kda} | GPM: {gpm} | XPM: {xpm} | Net: {net} | Steam ID: {account_id}\n"
                    f"  <emoji document_id=5445221832074483553>💼</emoji> {items_str}"
                )

                if p["player_slot"] < 128:
                    radiant.append(line)
                else:
                    dire.append(line)

            msg = (
                f"<blockquote><emoji document_id=5217703082099498813>🤬</emoji> Матч {match_id}\n"
                f"<emoji document_id=5373236586760651455>⏱️</emoji> Длительность: {duration}\n"
                f"Результат: {result}\n\n"
                f"<emoji document_id=5368338090660209672>🌿</emoji> Radiant:\n" + "\n".join(radiant) +
                f"\n\n<emoji document_id=5397751602956239123>🔥</emoji> Dire:\n" + "\n".join(dire) +
                f"</blockquote>"
            )

            await utils.answer(message, msg)
        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5390972675684337321>🤐</emoji> Ошибка загрузки матча: {str(e)}")

    async def herocmd(self, message: Message):
        """Показывает статистику героя | Пример: .hero pudge"""
        args = utils.get_args_raw(message)
        raw_id = self.config["PLAYER_ID"]

        if not raw_id:
            return await utils.answer(
                message,
                "<emoji document_id=5375557664396835394>❌</emoji> Не задан PLAYER_ID"
            )

        raw_id = int(raw_id)

        if raw_id > 76561197960265728:
            account_id = raw_id - 76561197960265728
        else:
            account_id = raw_id

        try:
            if not args:
                return await utils.answer(message, "Укажи имя героя: .hero pudge")

            hero_name_arg = args.strip().lower()
            hero_id = None

            # Ищем героя
            for hid, name in self.heroes.items():
                if name.lower() == hero_name_arg:
                    hero_id = hid
                    hero_name = name
                    break

            if hero_id is None:
                return await utils.answer(
                    message,
                    "<emoji document_id=5390972675684337321>🤐</emoji> Герой не найден"
                )

            # Берём последние 20 матчей НА ЭТОМ ГЕРОЕ
            hero_matches = requests.get(
                f"{API_URL}/players/{account_id}/matches",
                params={
                    "hero_id": hero_id,
                    "limit": 20
                }
            ).json()

            if not hero_matches:
                return await utils.answer(
                    message,
                    f"<emoji document_id=5390972675684337321>🤐</emoji> Ты не играл на {hero_name}"
                )

            games = len(hero_matches)
            wins = sum(1 for m in hero_matches if self.is_win(m))
            winrate = round(wins / games * 100, 1)
            losses = games - wins

            kills = sum(m["kills"] for m in hero_matches)
            deaths = sum(m["deaths"] for m in hero_matches)
            assists = sum(m["assists"] for m in hero_matches)
            kda = round((kills + assists) / max(1, deaths), 2)

            hero_icon = self.hero_emojis2.get(hero_name, "")

            msg = (
                f"<b>Герой: {hero_icon} {hero_name}</b>\n\n"
                f"<emoji document_id=5375437280758496345>🎮</emoji> Матчей: {games}\n"
                f"<emoji document_id=5456498809875995940>🏆</emoji> Побед: {wins} ({winrate}%)\n"
                f"<emoji document_id=5352703271536454445>❌</emoji> Поражений: {losses}\n"
                f"<emoji document_id=5240271820979981346>⚔️</emoji> KDA: {kda}\n"
            )

            return await utils.answer(message, msg, parse_mode="html")

        except Exception as e:
            return await utils.answer(
                message,
                f"<emoji document_id=5390972675684337321>🤐</emoji> Ошибка hero: {e}"
            )

    async def comparecmd(self, message: Message):
        """Сравнения статистики себя и противника .compare <id противника>"""
        args = utils.get_args_raw(message)
        my_raw = self.config["PLAYER_ID"]

        if not my_raw:
            return await utils.answer(message, f"<emoji document_id=5375557664396835394>❌</emoji> Не задан PLAYER_ID")

        if not args:
            return await utils.answer(message, f"<emoji document_id=5390972675684337321>🤐</emoji> Укажи SteamID или account_id игрока")

        try:
            my_id = self._to_account_id(int(my_raw))
            other_id = self._to_account_id(int(args.strip()))

            my_matches = requests.get(
                f"{API_URL}/players/{my_id}/matches",
                params={"limit": 100}
            ).json()

            other_matches = requests.get(
                f"{API_URL}/players/{other_id}/matches",
                params={"limit": 100}
            ).json()

            if not my_matches or not other_matches:
                return await utils.answer(message, "<emoji document_id=5375557664396835394>❌</emoji> У одного из игроков нет матчей")

            def calc_stats(matches):
                games = len(matches)
                wins = sum(1 for m in matches if self.is_win(m))
                kills = sum(m["kills"] for m in matches)
                deaths = sum(m["deaths"] for m in matches)
                assists = sum(m["assists"] for m in matches)

                kda = round((kills + assists) / max(1, deaths), 2)
                winrate = round(wins / games * 100, 1)

                return games, wins, winrate, kda

            my_games, my_wins, my_wr, my_kda = calc_stats(my_matches)
            o_games, o_wins, o_wr, o_kda = calc_stats(other_matches)

            msg = (
                f"<blockquote><emoji document_id=5240271820979981346>⚔️</emoji> СРАВНЕНИЕ ИГРОКОВ\n"
                f"<emoji document_id=5425013375291629746>😳</emoji> <b>Ты</b>\n"
                f"<emoji document_id=5375437280758496345>🎮</emoji> Матчей: {my_games}\n"
                f"<emoji document_id=5456498809875995940>🏆</emoji> Побед: {my_wins} ({my_wr}%)\n"
                f"<emoji document_id=5240271820979981346>⚔️</emoji> KDA: {my_kda}\n\n"
                f"<emoji document_id=6021829047057652150>🧍‍♀️</emoji> <b>Оппонент</b>\n"
                f"<emoji document_id=5375437280758496345>🎮</emoji> Матчей: {o_games}\n"
                f"<emoji document_id=5456498809875995940>🏆</emoji> Побед: {o_wins} ({o_wr}%)\n"
                f"<emoji document_id=5240271820979981346>⚔️</emoji> KDA: {o_kda}\n"
                f"</blockquote>"
            )

            await utils.answer(message, msg)

        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5390972675684337321>🤐</emoji> Ошибка compare: {e}")


        
    def _build_pages(self, matches):
        pages = []
        per_page = 5

        for i in range(0, len(matches), per_page):
            chunk = matches[i:i+per_page]

            text = "<b>Последние 40 игр:</b>\n\n"

            for m in chunk:
                hero_name = self.heroes.get(m["hero_id"], f"Unknown({m['hero_id']})")
                hero_icon = self.hero_emojis.get(hero_name, "")
                kda = f"{m['kills']}/{m['deaths']}/{m['assists']}"

                win = (
                    '<tg-emoji emoji-id="5429381339851796035">✅</tg-emoji> Победа' 
                    if self.is_win(m)
                    else '<tg-emoji emoji-id="5352703271536454445">❌</tg-emoji> Поражение'
                )

                match_time = self._format_match_time(m.get("start_time", 0))

                text += (
                    f"<blockquote>"
                    f"<b>Матч {m['match_id']}</b>\n"
                    f"Герой: {hero_name} {hero_icon}\n"
                    f"KDA: {kda} | {win}\n"
                    f"Время: {match_time}"
                    f"</blockquote>\n\n"
                )

            pages.append(text)

        return pages


    def _pagination_markup(self, page, total):
        return [
            [
                {
                    "text": "⬅️",
                    "callback": self.prev_page,
                    "args": (page,)
                },
                {
                    "text": f"{page+1}/{total}",
                    "callback": self.noop
                },
                {
                    "text": "➡️",
                    "callback": self.next_page,
                    "args": (page,)
                },
            ],
            [
                {
                    "text": "❌ Закрыть",
                    "callback": self.close_msg
                }
            ]
        ]

    async def prev_page(self, call, page: int):
        pages = self._pages_cache.get(call.inline_message_id)
        if not pages:
            return

        page = max(0, page - 1)

        await call.edit(
            pages[page],
            reply_markup=self._pagination_markup(page, len(pages))
        )

    async def next_page(self, call, page: int):
        pages = self._pages_cache.get(call.inline_message_id)
        if not pages:
            return

        page = min(len(pages) - 1, page + 1)

        await call.edit(
            pages[page],
            reply_markup=self._pagination_markup(page, len(pages))
        )

    async def noop(self, call):
        await call.answer()



    async def close_msg(self, call):
        self._pages_cache.pop(call.inline_message_id, None)
        await call.delete()



    def _close_btn(self):
        return [[
            {
                "text": "❌ Закрыть",
                "callback": self.close_msg
            }
        ]]                                      
