# -- version --
__version__ = (2, 3, 0)
# -- version --

# meta developer: @Itachi_Uchiha_sss
# meta banner: https://t.me/Itachi_Uchiha_sss

import requests
from requests import RequestException
from .. import loader, utils
from telethon.tl.types import Message
from datetime import datetime, timezone, timedelta
import time
import asyncio

API_URL = "https://api.opendota.com/api"


@loader.tds
class DotaStatsMod(loader.Module):
    strings = {"name": "OpenDota"}

    def is_win(self, match):
        is_radiant = match["player_slot"] < 128
        return match["radiant_win"] == is_radiant

    def _extract_api_error(self, payload) -> str:
        if isinstance(payload, dict):
            for key in ("error", "message", "detail"):
                value = payload.get(key)
                if value:
                    return str(value)
        return f"unexpected response type: {type(payload).__name__}"

    def _get_json(self, path: str, *, params=None, timeout: int = 15, retries: int = 2):
        last_error = None

        for attempt in range(retries + 1):
            try:
                response = requests.get(
                    f"{API_URL}{path}",
                    params=params,
                    timeout=timeout,
                )
                response.raise_for_status()
                return response.json()
            except requests.Timeout as e:
                last_error = e
                if attempt == retries:
                    raise TimeoutError(
                        "OpenDota не ответил вовремя, попробуй ещё раз чуть позже"
                    ) from e
            except RequestException as e:
                raise ConnectionError(f"Ошибка запроса к OpenDota: {e}") from e

        raise ConnectionError(f"Ошибка запроса к OpenDota: {last_error}")

    async def _get_json_async(self, path: str, *, params=None, timeout: int = 15, retries: int = 2):
        return await asyncio.to_thread(
            self._get_json,
            path,
            params=params,
            timeout=timeout,
            retries=retries,
        )

    def _fetch_player_matches(self, player_id: int, limit: int = 40):
        payload = self._get_json(
            f"/players/{player_id}/matches",
            params={"limit": limit},
        )

        if not isinstance(payload, list):
            raise ValueError(
                f"OpenDota API returned {self._extract_api_error(payload)}"
            )

        return payload[:limit]

    async def _fetch_player_matches_async(self, player_id: int, limit: int = 40):
        return await asyncio.to_thread(
            self._fetch_player_matches,
            player_id,
            limit,
        )

    def _check_endpoint(self, url: str, *, params=None, timeout: int = 10) -> dict:
        started = time.time()
        try:
            response = requests.get(url, params=params, timeout=timeout)
            elapsed = round(time.time() - started, 2)
            return {
                "ok": response.ok,
                "status": response.status_code,
                "elapsed": elapsed,
            }
        except requests.Timeout:
            elapsed = round(time.time() - started, 2)
            return {
                "ok": False,
                "status": "timeout",
                "elapsed": elapsed,
                "error": "сервер не ответил вовремя",
            }
        except RequestException as e:
            elapsed = round(time.time() - started, 2)
            return {
                "ok": False,
                "status": "error",
                "elapsed": elapsed,
                "error": str(e),
            }

    async def _check_endpoint_async(self, url: str, *, params=None, timeout: int = 10) -> dict:
        return await asyncio.to_thread(
            self._check_endpoint,
            url,
            params=params,
            timeout=timeout,
        )

    def __init__(self):
        self._pages_cache = {}
        self._vs_cache = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "PLAYER_ID",
                None,
                "Steam ID игрока",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "TIMEZONE",
                0,
                "Часовой пояс (0=UTC+0, 1=UTC+1, 2=UTC+2, 3=UTC+3, 4=UTC+4, 5=UTC+5, 6=UTC+6, 7=UTC+7, 8=UTC+8, 9=UTC+9, 10=UTC+10, 11=UTC+11, 12=UTC+12, -1=UTC-1... -12=UTC-12)",
                validator=loader.validators.Choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12])
            )
        )
        self.heroes = {}
        self.items = {}
        self.item_emojis = {
            "Blink": '<tg-emoji emoji-id="5467710328080981143">🤩</tg-emoji>',
            "Black King Bar": '<tg-emoji emoji-id="5467828615775279955">🤩</tg-emoji>',
            "Ultimate Scepter": '<tg-emoji emoji-id="5467777522844327342">🤩</tg-emoji>',
            "Aghanims Scepter": '<tg-emoji emoji-id="5467777522844327342">🤩</tg-emoji>',
            "Aghanim's Scepter": '<tg-emoji emoji-id="5467777522844327342">🤩</tg-emoji>',
            "Power Treads": '<tg-emoji emoji-id="5467823212706421270">🤩</tg-emoji>',
            "Desolator": '<tg-emoji emoji-id="5467606626095619791">🤩</tg-emoji>',
            "Greater Crit": '<tg-emoji emoji-id="5467526443351170991">🤩</tg-emoji>',
            "Satanic": '<tg-emoji emoji-id="5467481238820381084">🤩</tg-emoji>',
            "Butterfly": '<tg-emoji emoji-id="5467628088047197171">🤩</tg-emoji>',
            "Assault": '<tg-emoji emoji-id="5467467786982809436">🤩</tg-emoji>',
            "Sheepstick": '<tg-emoji emoji-id="5467471613798669675">🤩</tg-emoji>',
            "Rapier": '<tg-emoji emoji-id="5469940176316816456">🤩</tg-emoji>',
            "Heart": '<tg-emoji emoji-id="5469829838606982639">🤩</tg-emoji>',
            "Heart Of Tarrasque": '<tg-emoji emoji-id="5469829838606982639">🤩</tg-emoji>',
            "Invis Sword": '<tg-emoji emoji-id="5469889422688278238">🤩</tg-emoji>',
            "Manta": '<tg-emoji emoji-id="5467786310347413191">🤩</tg-emoji>',
            "Sphere": '<tg-emoji emoji-id="5467841560806709776">🤩</tg-emoji>',
            "Moon Shard": '<tg-emoji emoji-id="5469874360237970537">🤩</tg-emoji>',
            "Crystalys": '<tg-emoji emoji-id="5467629917703264949">🤩</tg-emoji>',
            "Dragon Lance": '<tg-emoji emoji-id="5429427424850906507">🫤</tg-emoji>',
            "Skadi": '<tg-emoji emoji-id="5467912754184609175">🤩</tg-emoji>',
            "Mjollnir": '<tg-emoji emoji-id="5467553437220624541">🤩</tg-emoji>',
            "Eternal Shroud": '<tg-emoji emoji-id="5429168489862565021">🤤</tg-emoji>',
            "Radiance": '<tg-emoji emoji-id="5467917160821053680">🤩</tg-emoji>',
            "Bloodstone": '<tg-emoji emoji-id="5467872957017647753">🤩</tg-emoji>',
            "Vanguard": '<tg-emoji emoji-id="5467905512869745249">🤩</tg-emoji>',
            "Overwhelming Blink": '<tg-emoji emoji-id="5467811268402372102">🤩</tg-emoji>',
            "Force Staff": '<tg-emoji emoji-id="5467816044406004412">🤩</tg-emoji>',
            "Blade Mail": '<tg-emoji emoji-id="5467910258808610438">🤩</tg-emoji>',
            "Lotus Orb": '<tg-emoji emoji-id="5467854656161996490">🤩</tg-emoji>',
            "Diffusal Blade": '<tg-emoji emoji-id="5467589596550291093">🤩</tg-emoji>',
            "Disperser": '<tg-emoji emoji-id="5467511685843540004">🤩</tg-emoji>',
            "Silver Edge": '<tg-emoji emoji-id="5467413421286774948">🤩</tg-emoji>',
            "Solar Crest": '<tg-emoji emoji-id="5470022991876216864">🤩</tg-emoji>',
            "Octarine Core": '<tg-emoji emoji-id="5469910390718616277">🤩</tg-emoji>',
            "Refresher": '<tg-emoji emoji-id="5467413301027691972">🤩</tg-emoji>',
            "Soul Ring": '<tg-emoji emoji-id="5467735694157831691">🤩</tg-emoji>',
            "Pipe": '<tg-emoji emoji-id="5467784545115857970">🤩</tg-emoji>',
            "Cyclone": '<tg-emoji emoji-id="5469770533698556516">🤩</tg-emoji>',
            "Wind Waker": '<tg-emoji emoji-id="5467755674345690984">🤩</tg-emoji>',
            "Hurricane Pike": '<tg-emoji emoji-id="5429505296902945143">🤗</tg-emoji>',
            "Veil Of Discord": '<tg-emoji emoji-id="5467619223234698435">🤩</tg-emoji>',
            "Glimmer Cape": '<tg-emoji emoji-id="5467869675662631035">🤩</tg-emoji>',
            "Shadow Amulet": '<tg-emoji emoji-id="5467818432407819955">🤩</tg-emoji>',
            "Tranquil Boots": '<tg-emoji emoji-id="5467458642997434165">🤩</tg-emoji>',
            "Arcane Boots": '<tg-emoji emoji-id="5467688316373590211">🤩</tg-emoji>',
            "Travel Boots": '<tg-emoji emoji-id="5467854351219318497">🤩</tg-emoji>',
            "Travel Boots 2": '<tg-emoji emoji-id="5467653724706986524">🤩</tg-emoji>',
            "Boots": '<tg-emoji emoji-id="5429649362990960283">💜</tg-emoji>',
            "Phase Boots": '<tg-emoji emoji-id="5467564569775857363">🤩</tg-emoji>',
            "Mask Of Madness": '<tg-emoji emoji-id="5467883471097585936">🤩</tg-emoji>',
            "Ancient Janggo": '<tg-emoji emoji-id="5467804241835876590">🤩</tg-emoji>',
            "Boots Of Bearing": '<tg-emoji emoji-id="5467809013544541750">🤩</tg-emoji>',
            "Meteor Hammer": '<tg-emoji emoji-id="5469909724998687900">🤩</tg-emoji>',
            "Guardian Greaves": '<tg-emoji emoji-id="5427047918479642257">👇</tg-emoji>',
            "Ring Of Basilius": '<tg-emoji emoji-id="5467867145926891521">🤩</tg-emoji>',
            "Smoke Of Deceit": '<tg-emoji emoji-id="5467832077518921780">🤩</tg-emoji>',
            "Dust": '<tg-emoji emoji-id="5467852414189067273">🤩</tg-emoji>',
            "Bottle": '<tg-emoji emoji-id="5467423492985085154">🤩</tg-emoji>',
            "Magic Stick": '<tg-emoji emoji-id="5467520726749699871">🤩</tg-emoji>',
            "Holy Locket": '<tg-emoji emoji-id="5429324818082202689">🥹</tg-emoji>',
            "Magic Wand": '<tg-emoji emoji-id="5467791386998758693">🤩</tg-emoji>',
            "Aether Lens": '<tg-emoji emoji-id="5467863087182797856">🤩</tg-emoji>',
            "Swift Blink": '<tg-emoji emoji-id="5467512635031313209">🤩</tg-emoji>',
            "Null Talisman": '<tg-emoji emoji-id="5469971357779384692">🤩</tg-emoji>',
            "Bracer": '<tg-emoji emoji-id="5469634555033965479">🤩</tg-emoji>',
            "Wraith Band": '<tg-emoji emoji-id="5467754252711516912">🤩</tg-emoji>',
            "Soul Booster": '<tg-emoji emoji-id="5467565600568006619">🤩</tg-emoji>',
            "Kaya": '<tg-emoji emoji-id="5429406474000437184">👩‍❤️‍💋‍👨</tg-emoji>',
            "Yasha": '<tg-emoji emoji-id="5467560339233070091">🤩</tg-emoji>',
            "Sange And Yasha": '<tg-emoji emoji-id="5429589242038749865">🤚</tg-emoji>',
            "Orchid": '<tg-emoji emoji-id="5467520726749699874">🤩</tg-emoji>',
            "Bloodthorn": '<tg-emoji emoji-id="5467694776004401553">🤩</tg-emoji>',
            "Ethereal Blade": '<tg-emoji emoji-id="5467641462575358888">🤩</tg-emoji>',
            "Heavens Halberd": '<tg-emoji emoji-id="5467846439889558895">🤩</tg-emoji>',
            "Sange": '<tg-emoji emoji-id="5469885926584898014">🤩</tg-emoji>',
            "Urn Of Shadows": '<tg-emoji emoji-id="5467630226940910178">🤩</tg-emoji>',
            "Spirit Vessel": '<tg-emoji emoji-id="5429261402890079825">😩</tg-emoji>',
            "Crimson Guard": '<tg-emoji emoji-id="5470036121591240703">🤩</tg-emoji>',
            "Refresher Shard": '<tg-emoji emoji-id="5467436815973636888">🤩</tg-emoji>',
            "Echo Sabre": '<tg-emoji emoji-id="5429603432610695458">🤱</tg-emoji>',
            "Harpoon": '<tg-emoji emoji-id="5467597984621420624">🤩</tg-emoji>',
            "Arcane Blink": '<tg-emoji emoji-id="5467886499049528800">🤩</tg-emoji>',
            "Abaddon’s Aghanim’s Scepter": '<tg-emoji emoji-id="5469857141714083939">🤩</tg-emoji>',
            "Mekansm": '<tg-emoji emoji-id="5467932824566784067">🤩</tg-emoji>',
            "Rod Of Atos": '<tg-emoji emoji-id="5467818376573246343">🤩</tg-emoji>',
            "Kaya And Sange": '<tg-emoji emoji-id="5467789192270470219">🤩</tg-emoji>',
            "Phylactery": '<tg-emoji emoji-id="5208510580775737094">😎</tg-emoji>',
            "Angels Demise": '<tg-emoji emoji-id="5467410049737448975">🤩</tg-emoji>',
            "Bfury": '<tg-emoji emoji-id="5469748109674306463">🤩</tg-emoji>',
            "Monkey King Bar": '<tg-emoji emoji-id="5470163106594312935">🤩</tg-emoji>',
            "Hand Of Midas": '<tg-emoji emoji-id="5429484178548752495">🤡</tg-emoji>',
            "Basher": '<tg-emoji emoji-id="5469746426047125184">🤩</tg-emoji>',
            "Abyssal Blade": '<tg-emoji emoji-id="5467666536594431270">🤩</tg-emoji>',
            "Aeon Disk": '<tg-emoji emoji-id="5467791133595686879">🤩</tg-emoji>',
            "Armlet": '<tg-emoji emoji-id="5469824396883416139">🤩</tg-emoji>',
            "Witch Blade": '<tg-emoji emoji-id="5467826399572156107">🤩</tg-emoji>',
            "Devastator": '<tg-emoji emoji-id="5467805345642470314">🤩</tg-emoji>',
            "Revenants Brooch": '<tg-emoji emoji-id="5469908634076992123">🤩</tg-emoji>',
            "Ward Observer": '<tg-emoji emoji-id="5467632846870962993">🤩</tg-emoji>',
            "Ward Sentry": '<tg-emoji emoji-id="5467462169165586203">🤩</tg-emoji>',
            "Ward Dispenser": '<tg-emoji emoji-id="5469962815089431997">🤩</tg-emoji>',
            "Falcon Blade": '<tg-emoji emoji-id="5467861553879473110">🤩</tg-emoji>',
            "Mage Slayer": '<tg-emoji emoji-id="5470013504293461332">🤩</tg-emoji>',
            "Dagon": '<tg-emoji emoji-id="5467488218142235587">🤩</tg-emoji>',
            "Dagon 2": '<tg-emoji emoji-id="5469969296195082383">🤩</tg-emoji>',
            "Dagon 3": '<tg-emoji emoji-id="5469622112513709919">🤩</tg-emoji>',
            "Dagon 4": '<tg-emoji emoji-id="5469844480150492940">🤩</tg-emoji>',
            "Dagon 5": '<tg-emoji emoji-id="5469686244965374270">🤩</tg-emoji>',
            "Nullifier": '<tg-emoji emoji-id="5467639448235695534">🤩</tg-emoji>',
            "Helm Of The Dominator": '<tg-emoji emoji-id="5467464140555575688">🤩</tg-emoji>',
            "Helm Of The Overlord": '<tg-emoji emoji-id="5467741569673092276">🤩</tg-emoji>',
            "Maelstrom": '<tg-emoji emoji-id="5467923019156446536">🤩</tg-emoji>',
            "Ghost": '<tg-emoji emoji-id="5470035653439803744">🤩</tg-emoji>',
            "Quelling Blade": '<tg-emoji emoji-id="5467378189670046307">🤩</tg-emoji>',
            "Shivas Guard": '<tg-emoji emoji-id="5467835062521190904">🤩</tg-emoji>',
            "Infused Raindrop": '<tg-emoji emoji-id="5429589508326716866">💑</tg-emoji>',
            "Gem": '<tg-emoji emoji-id="5467526344566921150">🤩</tg-emoji>',
            "Yasha And Kaya": '<tg-emoji emoji-id="5429591746004680178">💤</tg-emoji>',
            "Lifesteal": '<tg-emoji emoji-id="5469950286669829137">🤩</tg-emoji>',
            "Lesser Crit": '<tg-emoji emoji-id="5467629917703264949">🤩</tg-emoji>',
            "Vladmir": '<tg-emoji emoji-id="5467690648540830431">🤩</tg-emoji>',
            "Orb Of Frost": '<tg-emoji emoji-id="5429604854244872076">😶‍🌫️</tg-emoji>',
            "Wind Lace": '<tg-emoji emoji-id="5429632793007129283">🤕</tg-emoji>',
            "Fluffy Hat": '<tg-emoji emoji-id="5429599227837712299">😑</tg-emoji>',
            "Blight Stone": '<tg-emoji emoji-id="5429570795154210156">👩‍🦰</tg-emoji>',
            "Mithril Hammer": '<tg-emoji emoji-id="5467426739980361549">🤩</tg-emoji>',
            "Ogre Axe": '<tg-emoji emoji-id="5467868851028908643">🤩</tg-emoji>',
            "Circlet": '<tg-emoji emoji-id="5440652308994098468">👹</tg-emoji>',
            "Cloak": '<tg-emoji emoji-id="5438211616518734925">🤢</tg-emoji>',
            "Clarity": '<tg-emoji emoji-id="5467785249490493699">🤩</tg-emoji>',
            "Ring Of Health": '<tg-emoji emoji-id="5467752805307539172">🤩</tg-emoji>',
            "Eagle": '<tg-emoji emoji-id="5467582647293204653">🤩</tg-emoji>',
            "Branches": '<tg-emoji emoji-id="5467442214747526492">🤩</tg-emoji>',
            "Robe": '<tg-emoji emoji-id="5467691451699716884">🤩</tg-emoji>',
            "Tango": '<tg-emoji emoji-id="5467809876832968643">🤩</tg-emoji>',
            "Tiara Of Selemene": '<tg-emoji emoji-id="5470172177565240449">🤩</tg-emoji>',
            "Aegis": '<tg-emoji emoji-id="5467744176718240540">🤩</tg-emoji>',
            "Vitality Booster": '<tg-emoji emoji-id="5467811242632567795">🤩</tg-emoji>',
            "Headdress": '<tg-emoji emoji-id="5467884171177255427">🤩</tg-emoji>',
            "Pers": '<tg-emoji emoji-id="5467634204080624390">🤩</tg-emoji>',
            "Relic": '<tg-emoji emoji-id="5467765355201976698">🤩</tg-emoji>',
            "Void Stone": '<tg-emoji emoji-id="5467395210625440792">🤩</tg-emoji>',
            "Ultimate Orb": '<tg-emoji emoji-id="5467578854837085359">🤩</tg-emoji>',
            "Gauntlets": '<tg-emoji emoji-id="5467430596860992009">🤩</tg-emoji>',
            "Point Booster": '<tg-emoji emoji-id="5467599337536119160">🤩</tg-emoji>',
            "Famango": '<tg-emoji emoji-id="5467577836929835133">🤩</tg-emoji>',
            "Platemail": '<tg-emoji emoji-id="5467920592499924802">🤩</tg-emoji>',
            "Orb Of Corrosion": '<tg-emoji emoji-id="5467924105783171604">🤩</tg-emoji>',
            "Blade Of Alacrity": '<tg-emoji emoji-id="5467464917944656239">🤩</tg-emoji>',
            "Cheese": '<tg-emoji emoji-id="5467903739048254682">🤩</tg-emoji>',
            "Gungir": '<tg-emoji emoji-id="5467458591457827736">🤩</tg-emoji>',
            "Staff Of Wizardry": '<tg-emoji emoji-id="5467822662950609346">🤩</tg-emoji>',
            "Diadem": '<tg-emoji emoji-id="5469685862713284861">🤩</tg-emoji>',
            "Blood Grenade": '<tg-emoji emoji-id="5280926765928193216">👨‍🦱</tg-emoji>',
            "Mystic Staff": '<tg-emoji emoji-id="5467388080979730073">🤩</tg-emoji>',
            "Gloves": '<tg-emoji emoji-id="5469841349119332616">🤩</tg-emoji>',
            "Broadsword": '<tg-emoji emoji-id="5467756065187716276">🤩</tg-emoji>',
            "Chainmail": '<tg-emoji emoji-id="5467372309859818911">🤩</tg-emoji>',
            "Energy Booster": '<tg-emoji emoji-id="5467828508401100211">🤩</tg-emoji>',
            "Cornucopia": '<tg-emoji emoji-id="5467743695681904292">🤩</tg-emoji>',
            "Blitz Knuckles": '<tg-emoji emoji-id="5467602112084990687">🤩</tg-emoji>',
            "Enchanted Mango": '<tg-emoji emoji-id="5467870783764192653">🤩</tg-emoji>',
            "Belt Of Strength": '<tg-emoji emoji-id="5467715709675001734">🤩</tg-emoji>',
            "Javelin": '<tg-emoji emoji-id="5467443365798766241">🤩</tg-emoji>',
            "Roshans Banner": '<tg-emoji emoji-id="5467430893213734638">🤩</tg-emoji>',
            "Slippers": '<tg-emoji emoji-id="5467824982232948778">🤩</tg-emoji>',
            "Hyperstone": '<tg-emoji emoji-id="5469995989416825772">🤩</tg-emoji>',
            "Ring Of Tarrasque": '<tg-emoji emoji-id="5467665836514761681">🤩</tg-emoji>',
            "Flask": '<tg-emoji emoji-id="5467399406808492353">🤩</tg-emoji>',
            "Faerie Fire": '<tg-emoji emoji-id="5314334224147322409">👩‍🦲</tg-emoji>',
            "Orb Of Venom": '<tg-emoji emoji-id="5469911017783841138">🤩</tg-emoji>',
            "Oblivion Staff": '<tg-emoji emoji-id="5467710761872678029">🤩</tg-emoji>',
            "Demon Edge": '<tg-emoji emoji-id="5469879359579903518">🤩</tg-emoji>',
            "Ring Of Protection": '<tg-emoji emoji-id="5467518867028859087">🤩</tg-emoji>',
            "Sobi Mask": '<tg-emoji emoji-id="5467627091614789052">🤩</tg-emoji>',
            "Buckler": '<tg-emoji emoji-id="5467614331266948301">🤩</tg-emoji>',
            "Greater Famango": '<tg-emoji emoji-id="5467476810709098517">🤩</tg-emoji>',
            "Consecrated Wraps": '<tg-emoji emoji-id="5341441218746293135">👘</tg-emoji>',
            "Ring Of Regen": '<tg-emoji emoji-id="5467603203006685200">🤩</tg-emoji>',
            "Hydras Breath": '<tg-emoji emoji-id="5343760363647178272">👲</tg-emoji>',
            "Essence Distiller": '<tg-emoji emoji-id="5341457728600577852">💨</tg-emoji>',
            "Chasm Stone": '<tg-emoji emoji-id="5346305063050580881">🤕</tg-emoji>',
            "Voodoo Mask": '<tg-emoji emoji-id="5467416891620352938">🤩</tg-emoji>',
            "Reaver": '<tg-emoji emoji-id="5346110470967303740">🥴</tg-emoji>',
            "Shawl": '<tg-emoji emoji-id="5346268319605383344">🕺</tg-emoji>',
            "Specialists Array": '<tg-emoji emoji-id="5341312588770743680">🧰</tg-emoji>',
            "Crellas Crozier": '<tg-emoji emoji-id="5341699256086465595">🧙</tg-emoji>',
            "Claymore": '<tg-emoji emoji-id="5467518123999517884">🤩</tg-emoji>',
            "Talisman Of Evasion": '<tg-emoji emoji-id="5469849462312556864">🤩</tg-emoji>',
            "Splintmail": '<tg-emoji emoji-id="5388862240424235116">🤎</tg-emoji>',
            "Crown": '<tg-emoji emoji-id="5467598594506775207">🤩</tg-emoji>',
            "Wizard Hat": '<tg-emoji emoji-id="5389046430096728598">🤍</tg-emoji>',
            "Foragers Mana": '<tg-emoji emoji-id="5389065267823282566">👩‍🍼</tg-emoji>',
            "Foragers Health": '<tg-emoji emoji-id="5389097630401859068">😐</tg-emoji>'
        }
        self.rank_emojis = {
            "Herald": '<tg-emoji emoji-id="5963157659195542640">🎖</tg-emoji>',
            "Guardian": '<tg-emoji emoji-id="5963215018483780860">🎖</tg-emoji>',
            "Crusader": '<tg-emoji emoji-id="5960576663023523045">🎖</tg-emoji>',
            "Archon": '<tg-emoji emoji-id="5963052342302477581">🎖</tg-emoji>',
            "Legend": '<tg-emoji emoji-id="5963061984504056919">🎖</tg-emoji>',
            "Ancient": '<tg-emoji emoji-id="5963027435787127662">🎖</tg-emoji>',
            "Divine": '<tg-emoji emoji-id="5963113657255594572">🎖</tg-emoji>',
            "Immortal": '<tg-emoji emoji-id="5960656609544768701">🎖</tg-emoji>'
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

        self.item_emojis_norm = {self._norm_item_name(k): v for k, v in self.item_emojis.items()}
        self._load_heroes()
        self._load_items()

    def _norm_item_name(self, name: str) -> str:
        if not name:
            return ""
        name = name.lower().replace("’", "'")
        name = name.replace("'", "")
        name = name.replace("-", " ")
        name = " ".join(name.split())
        return name

    def _to_account_id(self, raw_id: int) -> int:
        return raw_id - 76561197960265728 if raw_id > 76561197960265728 else raw_id

    async def close_msg(self, call):
        try:
            await call.delete()
        except Exception as e:
            await call.answer(f"Не получилось удалить сообщение 😡\n{e}", alert=True)

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

    def _format_match_time(self, start_time: int) -> str:
        try:
            tz_offset = int(self.config["TIMEZONE"])
            match_time = datetime.fromtimestamp(start_time, tz=timezone.utc) + timedelta(hours=tz_offset)
            now = datetime.now(timezone.utc) + timedelta(hours=tz_offset)
            time_diff = now - match_time

            seconds = int(time_diff.total_seconds())

            if seconds < 60:
                return f"только что ({match_time.strftime('%d.%m.%Y %H:%M')})"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} минут назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
            elif seconds < 86400:
                hours = seconds // 3600
                return f"{hours} часов назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
            else:
                days = seconds // 86400
                return f"{days} дней назад ({match_time.strftime('%d.%m.%Y %H:%M')})"
        except Exception as e:
            print(f"[DotaStats] Ошибка форматирования времени: {e}")
            return "неизвестно"

    @loader.command(
        en_doc="- show your profile (uses PLAYER_ID)",
        ru_doc="- показать свой профиль (использует PLAYER_ID)",
        ua_doc="- показати свій профіль (використовує PLAYER_ID)",
    )
    async def profile2cmd(self, message: Message):
        pid = self.config["PLAYER_ID"]
        if not pid:
            return await utils.answer(message, '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Не задан Steam ID')
        await self._send_profile(message, pid)

    @loader.command(
        en_doc="- show profile by Steam account_id",
        ru_doc="- показать профиль по Steam account_id",
        ua_doc="- показати профіль за Steam account_id",
    )
    async def profileidcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            return await utils.answer(message, "Используй: .profileid <id>")
        await self._send_profile(message, args)

    @loader.command(
        en_doc="- check OpenDota site and API availability",
        ru_doc="- проверить доступность сайта и API OpenDota",
        ua_doc="- перевірити доступність сайту та API OpenDota",
    )
    async def odcheckcmd(self, message: Message):
        checks = [
            ("Сайт", await self._check_endpoint_async("https://www.opendota.com")),
            ("API", await self._check_endpoint_async(f"{API_URL}/heroes")),
        ]

        pid = self.config["PLAYER_ID"]
        if pid:
            checks.append(
                (
                    "Матчи игрока",
                    await self._check_endpoint_async(
                        f"{API_URL}/players/{pid}/matches",
                        params={"limit": 1},
                    ),
                )
            )

        lines = ["<b>Проверка OpenDota</b>\n"]
        for label, result in checks:
            if result["ok"]:
                lines.append(
                    f"✅ {label}: <code>{result['status']}</code> за <code>{result['elapsed']}s</code>"
                )
            else:
                error = result.get("error", "неизвестная ошибка")
                lines.append(
                    f"❌ {label}: <code>{result['status']}</code> за <code>{result['elapsed']}s</code> | {error}"
                )

        if not pid:
            lines.append('\n<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> PLAYER_ID не задан, проверка матчей игрока пропущена')

        await utils.answer(message, "\n".join(lines), parse_mode="html")

    async def _send_profile(self, message: Message, pid: str):
        try:
            r = await self._get_json_async(f"/players/{pid}")
            profile = r.get("profile", {})

            wl = await self._get_json_async(f"/players/{pid}/wl")
            win, lose = wl.get("win", 0), wl.get("lose", 0)
            total = win + lose
            wr = round(win / total * 100, 2) if total > 0 else 0

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

            msg = (
                f'<blockquote><tg-emoji emoji-id="5235611059909323996">⭐️</tg-emoji> Профиль: <code>{profile.get("personaname", "Unknown")}</code></blockquote>\n'
                f'<blockquote><tg-emoji emoji-id="5422683699130933153">🪪</tg-emoji> Steam ID: <code>{pid}</code></blockquote>\n'
                f'<blockquote><tg-emoji emoji-id="5456498809875995940">🏆</tg-emoji> Ранг: {rank_info}</blockquote>\n'
                f'<blockquote><tg-emoji emoji-id="5429381339851796035">✅</tg-emoji> Победы: {win}</blockquote>\n'
                f'<blockquote><tg-emoji emoji-id="5465225015190367274">👎</tg-emoji> Поражения: {lose}</blockquote>\n'
                f'<blockquote><tg-emoji emoji-id="5364265190353286344">📊</tg-emoji> Винрейт: {wr}%</blockquote>\n'
            )
            await utils.answer(message, msg, parse_mode="html")
        except Exception as e:
            await utils.answer(message, f'<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Ошибка загрузки профиля: {str(e)}')

    @loader.command(
        en_doc="- last 40 matches for PLAYER_ID",
        ru_doc="- последние 40 матчей по PLAYER_ID",
        ua_doc="- останні 40 матчів для PLAYER_ID",
    )
    async def dota2cmd(self, message: Message):
        pid = self.config["PLAYER_ID"]
        if not pid:
            return await utils.answer(message, '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Не задан Steam ID')

        try:
            matches = await self._fetch_player_matches_async(pid, limit=40)
            if not matches:
                return await utils.answer(message, '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Нет данных матчей')

            pages = self._build_pages(matches)

            msg = await utils.answer(
                message,
                pages[0]["text"],
                reply_markup=self._pagination_markup(
                    0,
                    len(pages),
                    pid,
                    pages[0]["match_ids"],
                )
            )

            msg_id = str(msg.inline_message_id)
            self._pages_cache[msg_id] = {
                "pages": pages,
                "player_id": str(pid),
            }

        except Exception as e:
            return await utils.answer(message, f"Ошибка: {e}")

    @loader.command(
        en_doc="- last 40 matches (Steam64 or account_id)",
        ru_doc="- последние 40 матчей (Steam64 или account_id)",
        ua_doc="- останні 40 матчів (Steam64 або account_id)",
    )
    async def dota2idcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            return await utils.answer(
                message,
                '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Используй: .dota2id <steam_id>'
            )

        raw_id = int(args)

        if raw_id > 76561197960265728:
            pid = raw_id - 76561197960265728
        else:
            pid = raw_id

        try:
            matches = await self._fetch_player_matches_async(pid, limit=40)
            if not matches:
                return await utils.answer(
                    message,
                    '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Нет данных матчей (профиль скрыт или нет игр)'
                )

            pages = self._build_pages(matches)

            msg = await utils.answer(
                message,
                pages[0]["text"],
                reply_markup=self._pagination_markup(
                    0,
                    len(pages),
                    pid,
                    pages[0]["match_ids"],
                )
            )

            msg_id = str(msg.inline_message_id)
            self._pages_cache[msg_id] = {
                "pages": pages,
                "player_id": str(pid),
            }

        except Exception as e:
            return await utils.answer(message, f"Ошибка: {e}")

    @loader.command(
        en_doc="- match details by match_id",
        ru_doc="- подробности матча по match_id",
        ua_doc="- деталі матчу за match_id",
    )
    async def matchcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            return await utils.answer(message, "Используй: .match id")
        await self._send_match_info(message, args)

    async def _send_match_info(self, message: Message, match_id: str):
        try:
            r = await asyncio.to_thread(self._get_match_data, match_id)
            await utils.answer(message, self._format_match_text(r, str(match_id)), parse_mode="html")
        except Exception as e:
            await utils.answer(message, f'<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Ошибка загрузки матча: {str(e)}')

    @loader.command(
        en_doc="- hero stats: last 20 games or all-time with -all",
        ru_doc="- статистика героя: последние 20 игр или вся с -all",
        ua_doc="- статистика героя: останні 20 ігор або вся з -all",
    )
    async def herocmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(
                message,
                "Используй: .hero <имя героя> [-all]"
            )

        parts = args.split()
        hero_query = parts[0].lower()
        mode_all = "-all" in parts

        hero_id = None
        hero_name = None

        for hid, name in self.heroes.items():
            if hero_query in name.lower():
                hero_id = hid
                hero_name = name
                break

        hero_icon = self.hero_emojis.get(hero_name, "")

        if not hero_id:
            return await utils.answer(message, "Герой не найден")

        account_id = self.config["PLAYER_ID"]
        if not account_id:
            return await utils.answer(message, "Не задан Steam ID")

        try:
            if mode_all:
                heroes_stats = await self._get_json_async(
                    f"/players/{account_id}/heroes"
                )

                hero_data = next(
                    (h for h in heroes_stats if h["hero_id"] == hero_id),
                    None
                )

                if not hero_data:
                    return await utils.answer(message, "Нет данных по герою")

                games = hero_data["games"]
                wins = hero_data["win"]
                losses = games - wins
                winrate = round((wins / games) * 100, 1) if games else 0
                total_wr = winrate
                total_wr_color = "🟢" if total_wr >= 55 else "🟡" if total_wr >= 50 else "🔴"

                matches = await self._get_json_async(
                    f"/players/{account_id}/matches",
                    params={"hero_id": hero_id, "limit": 100},
                )

                total_kills = sum(m["kills"] for m in matches)
                total_deaths = sum(m["deaths"] for m in matches)
                total_assists = sum(m["assists"] for m in matches)

                total_games = len(matches)
                avg_k = round(total_kills / total_games, 1) if total_games else 0
                avg_d = round(total_deaths / total_games, 1) if total_games else 0
                avg_a = round(total_assists / total_games, 1) if total_games else 0

                text = (
                    f"─────── ✦ ───────\n"
                    f"<b>Герой: {hero_icon} <code>{hero_name}</code></b>\n\n"
                    f"─────── ✦ ───────\n\n"
                    f'<b>〚<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji>〛 Вся статистика:</b>\n'
                    f'〚<tg-emoji emoji-id="5375437280758496345">🎮</tg-emoji>〛 Матчей➛ <b>{games}</b>\n'
                    f'〚<tg-emoji emoji-id="5429381339851796035">✅</tg-emoji>〛 Побед➛ <b>{wins}</b>\n'
                    f'〚<tg-emoji emoji-id="5352703271536454445">❌</tg-emoji>〛 Поражений➛ <b>{losses}</b>\n'
                    f'〚<tg-emoji emoji-id="5244837092042750681">📈</tg-emoji>〛 Винрейт➛ {total_wr_color} <b>{total_wr}%</b>\n'
                    f'<b>〚<tg-emoji emoji-id="5240271820979981346">⚔️</tg-emoji>〛 Средний KDA (≈100 игр)</b>\n'
                    f"{avg_k} / {avg_d} / {avg_a}"
                )

                return await utils.answer(message, text, parse_mode="HTML")

            matches = await self._get_json_async(
                f"/players/{account_id}/matches",
                params={"hero_id": hero_id, "limit": 20},
            )

            if not matches:
                return await utils.answer(
                    message,
                    "Нет матчей на этом герое"
                )

            total = len(matches)
            wins = sum(1 for m in matches if self.is_win(m))
            losses = total - wins
            winrate = round((wins / total) * 100, 1) if total else 0
            recent_wr = winrate
            recent_wr_color = "🟢" if recent_wr >= 55 else "🟡" if recent_wr >= 50 else "🔴"

            total_kills = sum(m["kills"] for m in matches)
            total_deaths = sum(m["deaths"] for m in matches)
            total_assists = sum(m["assists"] for m in matches)

            avg_k = round(total_kills / total, 1) if total else 0
            avg_d = round(total_deaths / total, 1) if total else 0
            avg_a = round(total_assists / total, 1) if total else 0

            text = (
                f"─────── ✦ ───────\n"
                f"<b>Герой: {hero_icon} <code>{hero_name}</code></b>\n\n"
                f"─────── ✦ ───────\n\n"
                f'<b>〚<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji>〛 Последние 20 игр:</b>\n'
                f'〚<tg-emoji emoji-id="5375437280758496345">🎮</tg-emoji>〛 Матчей➛ <b>{total}</b>\n'
                f'〚<tg-emoji emoji-id="5429381339851796035">✅</tg-emoji>〛 Побед➛ <b>{wins}</b>\n'
                f'〚<tg-emoji emoji-id="5352703271536454445">❌</tg-emoji>〛 Поражений➛ <b>{losses}</b>\n'
                f'〚<tg-emoji emoji-id="5244837092042750681">📈</tg-emoji>〛 Винрейт➛ {recent_wr_color} <b>{recent_wr}%</b>\n'
                f'<b>〚<tg-emoji emoji-id="5240271820979981346">⚔️</tg-emoji>〛 Средний KDA</b>\n'
                f"{avg_k} / {avg_d} / {avg_a}"
            )

            return await utils.answer(message, text, parse_mode="HTML")

        except Exception as e:
            return await utils.answer(message, f"Ошибка hero: {e}")

    @loader.command(
        en_doc="- compare your stats with another player",
        ru_doc="- сравнить статистику с другим игроком",
        ua_doc="- порівняти статистику з іншим гравцем",
    )
    async def comparecmd(self, message: Message):
        args = utils.get_args_raw(message)
        my_raw = self.config["PLAYER_ID"]

        if not my_raw:
            return await utils.answer(message, '<tg-emoji emoji-id="5375557664396835394">❌</tg-emoji> Не задан PLAYER_ID')

        if not args:
            return await utils.answer(message, '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Укажи SteamID или account_id игрока')

        try:
            my_id = self._to_account_id(int(my_raw))
            other_id = self._to_account_id(int(args.strip()))

            my_matches = await self._get_json_async(
                f"/players/{my_id}/matches",
                params={"limit": 100},
            )

            other_matches = await self._get_json_async(
                f"/players/{other_id}/matches",
                params={"limit": 100},
            )

            if not my_matches or not other_matches:
                return await utils.answer(message, '<tg-emoji emoji-id="5375557664396835394">❌</tg-emoji> У одного из игроков нет матчей')

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
                f'<blockquote><tg-emoji emoji-id="5240271820979981346">⚔️</tg-emoji> СРАВНЕНИЕ ИГРОКОВ\n'
                f'<tg-emoji emoji-id="5425013375291629746">😳</tg-emoji> <b>Ты</b>\n'
                f'<tg-emoji emoji-id="5375437280758496345">🎮</tg-emoji> Матчей: {my_games}\n'
                f'<tg-emoji emoji-id="5456498809875995940">🏆</tg-emoji> Побед: {my_wins} ({my_wr}%)\n'
                f'<tg-emoji emoji-id="5240271820979981346">⚔️</tg-emoji> KDA: {my_kda}\n\n'
                f'<tg-emoji emoji-id="6021829047057652150">🧍‍♀️</tg-emoji> <b>Оппонент</b>\n'
                f'<tg-emoji emoji-id="5375437280758496345">🎮</tg-emoji> Матчей: {o_games}\n'
                f'<tg-emoji emoji-id="5456498809875995940">🏆</tg-emoji> Побед: {o_wins} ({o_wr}%)\n'
                f'<tg-emoji emoji-id="5240271820979981346">⚔️</tg-emoji> KDA: {o_kda}\n'
                f"</blockquote>"
            )

            await utils.answer(message, msg, parse_mode="html")

        except Exception as e:
            await utils.answer(message, f'<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Ошибка compare: {e}')

    async def _collect_vs_data(self, my_id: int, other_id: int, limit: int = 100):
        my_matches = await self._get_json_async(
            f"/players/{my_id}/matches",
            params={"limit": limit},
        )
        if not my_matches:
            return {"matches": [], "against": [], "together": []}

        against = []
        together = []

        for m in my_matches:
            try:
                match_data = await asyncio.to_thread(self._get_match_data, str(m["match_id"]))
            except Exception:
                continue

            players = match_data.get("players", [])
            my_p = next((p for p in players if p.get("account_id") == my_id), None)
            other_p = next((p for p in players if p.get("account_id") == other_id), None)

            if not my_p or not other_p:
                continue

            same_team = (my_p["player_slot"] < 128) == (other_p["player_slot"] < 128)
            my_win = self.is_win(my_p)

            entry = {
                "match_id": m["match_id"],
                "my_win": my_win,
                "my_hero": self.heroes.get(my_p["hero_id"], "?"),
                "other_hero": self.heroes.get(other_p["hero_id"], "?"),
                "my_kda": f"{my_p['kills']}/{my_p['deaths']}/{my_p['assists']}",
                "other_kda": f"{other_p['kills']}/{other_p['deaths']}/{other_p['assists']}",
                "duration": match_data.get("duration", 0),
                "start_time": match_data.get("start_time", 0),
            }

            if same_team:
                together.append(entry)
            else:
                against.append(entry)

        return {
            "matches": against + together,
            "against": against,
            "together": together,
        }

    def _build_vs_pages(self, data, mode: str = "against", per_page: int = 5):
        if mode == "against":
            matches = data["against"]
            title = '⚔️ Личные встречи — против'
        elif mode == "together":
            matches = data["together"]
            title = '🤝 Личные встречи — вместе'
        else:
            matches = data["matches"]
            title = '🎮 Личные встречи — все'

        total = len(matches)
        wins = sum(1 for m in matches if m["my_win"])
        losses = total - wins
        wr = round(wins / total * 100, 1) if total else 0

        pages = []

        if total == 0:
            pages.append({
                "text": f'<b>{title}</b>\n\nМатчей не найдено',
                "match_ids": [],
            })
            return pages

        for i in range(0, total, per_page):
            chunk = matches[i:i + per_page]

            text = (
                f'<b>{title}</b>\n'
                f'<blockquote>'
                f'<tg-emoji emoji-id="5375437280758496345">🎮</tg-emoji> Всего: <b>{total}</b> | '
                f'<tg-emoji emoji-id="5429381339851796035">✅</tg-emoji> {wins} | '
                f'<tg-emoji emoji-id="5352703271536454445">❌</tg-emoji> {losses} | '
                f'<tg-emoji emoji-id="5244837092042750681">📈</tg-emoji> {wr}%'
                f'</blockquote>\n\n'
            )

            for m in chunk:
                win = (
                    '<tg-emoji emoji-id="5429381339851796035">✅</tg-emoji> Победа'
                    if m["my_win"]
                    else '<tg-emoji emoji-id="5352703271536454445">❌</tg-emoji> Поражение'
                )

                my_icon = self.hero_emojis.get(m["my_hero"], "")
                other_icon = self.hero_emojis.get(m["other_hero"], "")
                match_time = self._format_match_time(m.get("start_time", 0))
                duration = f'{m["duration"] // 60}:{m["duration"] % 60:02d}'

                text += (
                    f"<blockquote>"
                    f"<b>Матч <code>{m['match_id']}</code></b>\n"
                    f"Ты: {my_icon} {m['my_hero']} — {m['my_kda']}\n"
                    f"Он: {other_icon} {m['other_hero']} — {m['other_kda']}\n"
                    f"{win}\n"
                    f"Время: {match_time} | <tg-emoji emoji-id=5375363394436109945>🕖</tg-emoji> {duration}"
                    f"</blockquote>\n\n"
                )

            pages.append({
                "text": text,
                "match_ids": [str(m["match_id"]) for m in chunk],
            })

        return pages

    def _vs_markup(self, page: int, total: int, my_id: int, other_id: int, mode: str = "against"):
        def mode_btn(label, mode_key):
            style = "danger" if mode == mode_key else "primary"
            return self._btn(label, style=style, callback=self.vs_mode, args=(page, mode_key))

        return [
            [
                mode_btn("⚔️ Против", "against"),
                mode_btn("🤝 Вместе", "together"),
                mode_btn("🎮 Все", "all"),
            ],
            [
                self._btn("◀️", style="primary", callback=self.vs_prev, args=(page, mode)),
                self._btn(f"{page+1}/{total}", style="primary", callback=self._noop),
                self._btn("▶️", style="primary", callback=self.vs_next, args=(page, mode)),
            ],
            [
                self._btn("📊 Противник", style="success", url=self._player_opendota_url(other_id)),
                self._btn("👤 Мой профиль", style="success", url=self._player_opendota_url(my_id)),
            ],
            [
                self._btn("❌ Закрыть", style="danger", action="close"),
            ],
        ]

    async def vs_prev(self, call, page: int, mode: str):
        msg_id = str(call.inline_message_id)
        payload = self._vs_cache.get(msg_id)
        if not payload:
            return
        pages = self._build_vs_pages(payload["data"], mode=mode)
        page = max(0, page - 1)
        await call.edit(
            pages[page]["text"],
            reply_markup=self._vs_markup(page, len(pages), payload["my_id"], payload["other_id"], mode),
        )
        payload["pages"] = pages
        payload["mode"] = mode

    async def vs_next(self, call, page: int, mode: str):
        msg_id = str(call.inline_message_id)
        payload = self._vs_cache.get(msg_id)
        if not payload:
            return
        pages = self._build_vs_pages(payload["data"], mode=mode)
        page = min(len(pages) - 1, page + 1)
        await call.edit(
            pages[page]["text"],
            reply_markup=self._vs_markup(page, len(pages), payload["my_id"], payload["other_id"], mode),
        )
        payload["pages"] = pages
        payload["mode"] = mode

    async def vs_mode(self, call, page: int, mode: str):
        msg_id = str(call.inline_message_id)
        payload = self._vs_cache.get(msg_id)
        if not payload:
            return
        pages = self._build_vs_pages(payload["data"], mode=mode)
        page = min(page, len(pages) - 1)
        await call.edit(
            pages[page]["text"],
            reply_markup=self._vs_markup(page, len(pages), payload["my_id"], payload["other_id"], mode),
        )
        payload["pages"] = pages
        payload["mode"] = mode

    @loader.command(
        en_doc="- head-to-head stats vs another player",
        ru_doc="- статистика личных встреч против игрока",
        ua_doc="- статистика особистих зустрічей проти гравця",
    )
    async def vscmd(self, message: Message):
        args = utils.get_args_raw(message)
        my_raw = self.config["PLAYER_ID"]

        if not my_raw:
            return await utils.answer(message, '<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Не задан PLAYER_ID')
        if not args or not args.isdigit():
            return await utils.answer(message, "Используй: .vs <account_id противника>")

        try:
            my_id = self._to_account_id(int(my_raw))
            other_id = self._to_account_id(int(args.strip()))

            data = await self._collect_vs_data(my_id, other_id, limit=40)

            if not data["matches"]:
                return await utils.answer(
                    message,
                    f'<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Не найдено матчей с игроком <code>{other_id}</code>'
                )

            pages = self._build_vs_pages(data, mode="against")

            msg = await utils.answer(
                message,
                pages[0]["text"],
                reply_markup=self._vs_markup(0, len(pages), my_id, other_id, mode="against"),
            )

            msg_id = str(msg.inline_message_id)
            self._vs_cache[msg_id] = {
                "pages": pages,
                "data": data,
                "my_id": my_id,
                "other_id": other_id,
                "mode": "against",
            }

        except Exception as e:
            await utils.answer(message, f'<tg-emoji emoji-id="5390972675684337321">🤐</tg-emoji> Ошибка: {e}')

    def _get_match_data(self, match_id: str):
        data = requests.get(f"{API_URL}/matches/{match_id}").json()
        if "match_id" not in data:
            raise ValueError("Матч не найден")
        return data

    def _format_match_text(self, match_data, match_id: str):
        duration = f"{match_data['duration'] // 60}:{match_data['duration'] % 60:02d}"
        radiant_win = match_data.get("radiant_win", False)
        result = (
            '<tg-emoji emoji-id="5368338090660209672">🌿</tg-emoji> Radiant Победа'
            if radiant_win
            else '<tg-emoji emoji-id="5397751602956239123">🔥</tg-emoji> Dire Победа'
        )

        radiant, dire = [], []
        for p in match_data.get("players", []):
            hero_name = self.heroes.get(p["hero_id"], f"Unknown({p['hero_id']})")
            hero_icon = self.hero_emojis.get(hero_name, "")
            kda = f"{p['kills']}/{p['deaths']}/{p['assists']}"
            gpm = p.get("gold_per_min", 0)
            xpm = p.get("xp_per_min", 0)
            net = p.get("total_gold", 0)
            account_id = p.get("account_id", "N/A")

            def _first_nonzero(*vals):
                for v in vals:
                    if v not in (None, 0):
                        return v
                return 0

            def _extract_items(player):
                main = [0] * 6
                backpack = [0] * 3

                def set_slot(idx, val):
                    if val in (None, 0):
                        return
                    if 0 <= idx <= 5 and not main[idx]:
                        main[idx] = val
                    elif 6 <= idx <= 8 and not backpack[idx - 6]:
                        backpack[idx - 6] = val

                for i in range(6):
                    set_slot(i, player.get(f"item_{i}"))
                    set_slot(i, player.get(f"item{i}"))

                for i in range(3):
                    set_slot(6 + i, player.get(f"item_{6 + i}"))
                    set_slot(6 + i, player.get(f"backpack_{i}"))
                    set_slot(6 + i, player.get(f"backpack{i}"))

                for k, v in player.items():
                    if v in (None, 0) or not isinstance(k, str):
                        continue
                    if k.startswith("item_") and k[5:].isdigit():
                        set_slot(int(k[5:]), v)
                    elif k.startswith("item") and k[4:].isdigit():
                        set_slot(int(k[4:]), v)
                    elif k.startswith("backpack_") and k[9:].isdigit():
                        set_slot(6 + int(k[9:]), v)
                    elif k.startswith("backpack") and k[8:].isdigit():
                        set_slot(6 + int(k[8:]), v)

                items_list = player.get("items")
                if isinstance(items_list, list) and items_list:
                    for x in items_list:
                        if isinstance(x, int):
                            if x and x not in main and len([v for v in main if v]) < 6:
                                idx = main.index(0)
                                main[idx] = x
                            elif x and x not in backpack and len([v for v in backpack if v]) < 3:
                                idx = backpack.index(0)
                                backpack[idx] = x
                        elif isinstance(x, dict):
                            iid = x.get("item_id") or x.get("itemId") or x.get("id")
                            if iid in (None, 0):
                                continue
                            slot = x.get("slot") or x.get("item_slot")
                            is_backpack = x.get("backpack") or x.get("is_backpack") or x.get("in_backpack")
                            if isinstance(slot, int):
                                set_slot(slot, iid)
                            elif is_backpack:
                                if 0 in backpack:
                                    backpack[backpack.index(0)] = iid
                            else:
                                if 0 in main:
                                    main[main.index(0)] = iid

                backpack_list = player.get("backpack")
                if isinstance(backpack_list, list) and backpack_list:
                    for x in backpack_list:
                        if isinstance(x, int):
                            if x and x not in backpack and 0 in backpack:
                                backpack[backpack.index(0)] = x
                        elif isinstance(x, dict):
                            iid = x.get("item_id") or x.get("itemId") or x.get("id")
                            if iid in (None, 0):
                                continue
                            if 0 in backpack:
                                backpack[backpack.index(0)] = iid

                return main, backpack

            main_item_ids, backpack_item_ids = _extract_items(p)

            def format_items(ids):
                out = []
                for iid in ids:
                    if not iid or iid == 0:
                        continue
                    key = iid
                    item_name = None
                    if key in self.items:
                        item_name = self.items[key]
                    else:
                        str_key = str(key)
                        if str_key in self.items:
                            item_name = self.items[str_key]
                    if item_name:
                        item_icon = self.item_emojis.get(
                            item_name,
                            self.item_emojis_norm.get(self._norm_item_name(item_name), "🧩"),
                        )
                        out.append(f"{item_icon} {item_name}")
                    else:
                        out.append(f"🧩 Unknown({iid})")
                return " | ".join(out) if out else "Нет предметов"

            main_items_str = format_items(main_item_ids)
            backpack_items_str = format_items(backpack_item_ids)

            line = (
                f"- <code>{hero_name}</code> {hero_icon} | {kda} | GPM: {gpm} | "
                f"XPM: {xpm} | Net: {net} | Steam ID: <code>{account_id}</code>\n"
                f'  <tg-emoji emoji-id="5445221832074483553">💼</tg-emoji> {main_items_str}\n'
                f"  🎒 {backpack_items_str}"
            )

            if p["player_slot"] < 128:
                radiant.append(line)
            else:
                dire.append(line)

        return (
            f'<blockquote><tg-emoji emoji-id="5217703082099498813">🤬</tg-emoji> Матч <code>{match_id}</code>\n'
            f'<tg-emoji emoji-id="5373236586760651455">⏱️</tg-emoji> Длительность: <code>{duration}</code>\n'
            f"Результат: {result}\n\n"
            f'<tg-emoji emoji-id="5368338090660209672">🌿</tg-emoji> Radiant:\n' + "\n".join(radiant) +
            f'\n\n<tg-emoji emoji-id="5397751602956239123">🔥</tg-emoji> Dire:\n' + "\n".join(dire) +
            f"</blockquote>"
        )

    def _build_pages(self, matches):
        pages = []
        per_page = 5

        for i in range(0, len(matches), per_page):
            chunk = matches[i:i+per_page]

            text = '<b><tg-emoji emoji-id="5319120041780726017">🎮</tg-emoji>Последние 40 игр<tg-emoji emoji-id="5319120041780726017">🎮</tg-emoji>:</b>\n\n'

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

                duration_sec = m.get("duration")
                duration_str = (
                    f" | <tg-emoji emoji-id=5375363394436109945>🕖</tg-emoji> {duration_sec // 60}:{duration_sec % 60:02d}"
                    if duration_sec
                    else ""
                )

                text += (
                    f"<blockquote>"
                    f"<b>Матч <code>{m['match_id']}</code></b>\n"
                    f"Герой: {hero_icon} {hero_name}\n"
                    f"KDA: {kda} | {win}\n"
                    f"Время: {match_time}{duration_str}"
                    f"</blockquote>\n\n"
                )

            pages.append(
                {
                    "text": text,
                    "match_ids": [str(match["match_id"]) for match in chunk],
                }
            )

        return pages

    def _player_opendota_url(self, player_id):
        return f"https://www.opendota.com/players/{player_id}"

    def _match_opendota_url(self, match_id):
        return f"https://www.opendota.com/matches/{match_id}"

    def _btn(self, text, style="danger", **kwargs):
        return {"text": text, "style": style, **kwargs}

    def _pagination_markup(self, page, total, player_id, match_ids):
        markup = [
            [
                self._btn(
                    "◀️ Назад",
                    style="primary",
                    callback=self.prev_page,
                    args=(page,)
                ),
                self._btn(
                    f"{page+1}/{total}",
                    style="primary",
                    callback=self._noop
                ),
                self._btn(
                    "Вперёд ▶️",
                    style="primary",
                    callback=self.next_page,
                    args=(page,)
                ),
            ],
            [
                self._btn(
                    "📊 Профиль OpenDota",
                    style="success",
                    url=self._player_opendota_url(player_id)
                ),
            ],
            [
                self._btn(
                    "❌ Закрыть",
                    style="danger",
                    action="close"
                )
            ],
        ]

        return markup

    async def _noop(self, call):
        await call.answer()

    async def prev_page(self, call, page: int):
        msg_id = str(call.inline_message_id) if hasattr(call, 'inline_message_id') else call.inline_message_id
        payload = self._pages_cache.get(msg_id)
        if not payload:
            return

        pages = payload["pages"]
        page = max(0, page - 1)

        await call.edit(
            pages[page]["text"],
            reply_markup=self._pagination_markup(
                page,
                len(pages),
                payload["player_id"],
                pages[page]["match_ids"],
            )
        )

    async def next_page(self, call, page: int):
        msg_id = str(call.inline_message_id) if hasattr(call, 'inline_message_id') else call.inline_message_id
        payload = self._pages_cache.get(msg_id)
        if not payload:
            return

        pages = payload["pages"]
        page = min(len(pages) - 1, page + 1)

        await call.edit(
            pages[page]["text"],
            reply_markup=self._pagination_markup(
                page,
                len(pages),
                payload["player_id"],
                pages[page]["match_ids"],
            )
        )