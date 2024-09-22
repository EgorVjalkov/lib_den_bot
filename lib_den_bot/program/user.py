from dataclasses import dataclass

from lib_den_bot.BD_main import game_base
import lib_den_bot.program.database


@dataclass
class User:
    user_id: int
    user_status: str

    @property
    def leased_games(self) -> list:
        return game_base.get_leased_games(self.user_id)

    @staticmethod
    def get_gemes_list():
        return game_base.get_game_list()
