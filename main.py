from typing import Self
import requests

class LeaderboardUser:
    def __init__(self: Self, name: str, rank: int, points: float, aredl_id: str):
        self.name: str = name
        self.rank: int = rank
        self.points: float = points
        self.aredl_id: str = aredl_id

class User:
    def __init__(self: Self, name: str, aredl_id: str):
        self.name: str = name
        self.aredl_id: str = aredl_id

class Verification:
    def __init__(self: Self, verifier: User, video_url: str, fps: int, aredl_id: str):
        self.verifier: User = verifier
        self.video_url: str = video_url
        self.fps: int = fps
        self.aredl_id: str = aredl_id

class Record:
    def __init__(self: Self, submitter: User, video_url: str, fps: int, aredl_id: str):
        self.submitter: User = submitter
        self.video_url: str = video_url
        self.fps: int = fps
        self.aredl_id: str = aredl_id

class ListDemon:
    def __init__(self: Self, name: str, position: int, level_id: int, aredl_id: str):
        self.name: str = name
        self.position: int = position
        self.level_id: int = level_id
        self.aredl_id: str = aredl_id

class Demon:
    def __init__(self: Self, name: str, position: int, publisher: User, points: float, verification: Verification, creators: list[User], records: list[Record], copy_password: str, level_id: int, aredl_id: str):
        self.name: str = name
        self.position: int = position
        self.publisher: User = publisher
        self.points: float = points
        self.verification: Verification = verification
        self.creators: list[User] = creators
        self.records: list[Record] = records
        self.copy_password: str = copy_password
        self.level_id: int = level_id
        self.aredl_id: str = aredl_id

class Pack:
    def __init__(self: Self, name: str, color: str, placement: int, points: float, demons: list[ListDemon], aredl_id: str):
        self.name: str = name
        self.color: str = color
        self.placement: int = placement
        self.points: float = points
        self.demons: list[ListDemon] = demons
        self.aredl_id: str = aredl_id

def get_list() -> list[ListDemon]:
    json: list[dict] = requests.get('https://pb.aredl.com/api/list/').json()
    demon_list: list[ListDemon] = [ListDemon(name=i['name'], position=i['name'], level_id=i['level_id'], aredl_id=i['id']) for i in json]
    return demon_list

def get_demon(level_id: int) -> Demon:
    json: dict = requests.get(f'https://pb.aredl.com/api/list?level_id={level_id}&includeVerification=true&includeCreators=true&includeRecords=true').json()
    try:
        json['level_password']
    except KeyError:
        json['level_password'] = 'None'
    stats: Demon = Demon(
                         name=json['name'],
                         position=json['position'],
                         publisher=User
                            (
                            name=json['publisher']['global_name'],
                            aredl_id=json['publisher']['id']
                            ),
                         points=json['points'],
                         verification=Verification
                            (
                             verifier=User
                                 (
                                 name=json['verification']['submitted_by']['global_name'],
                                 aredl_id=json['verification']['submitted_by']['id']
                                 ),
                            video_url=json['verification']['video_url'],
                            fps=json['verification']['fps'],
                            aredl_id=json['verification']['id']
                            ),
                         creators=[User
                             (
                             name=i['global_name'],
                             aredl_id=i['id']
                             ) for i in json['creators']],
                         records=[Record
                            (
                             submitter=User
                                 (
                                 name=i['submitted_by']['global_name'],
                                 aredl_id=i['submitted_by']['id']
                             ),
                             video_url=i['video_url'],
                             fps=i['fps'],
                             aredl_id=i['id']
                            ) for i in json['records']],
                         copy_password=json['level_password'],
                         level_id=json['level_id'],
                         aredl_id=json['id']
                        )
    return stats

def get_leaderboard() -> list[LeaderboardUser]:
    json: list[dict] = requests.get('https://pb.aredl.com/api/leaderboard/').json()
    leaderboard: list[LeaderboardUser] = [LeaderboardUser(name=i['user']['global_name'], rank=i['rank'], points=i['points'], aredl_id=i['user']['id']) for i in json]
    return leaderboard

def get_packs() -> list[Pack]:
    json: list[dict] = requests.get('https://pb.aredl.com/api/packs/').json()
    points: float = json[0]['points']
    packs: list[Pack] = [Pack
        (
        name=i['name'],
        color=i['color'],
        placement=i['placement_order'],
        points=points,
        demons=[ListDemon
            (
            name=e['name'],
            position=e['position'],
            level_id=e['level_id'],
            aredl_id=e['id']
            ) for e in i['Levels']],
        aredl_id=i['id']
        ) for i in json]
    return packs
