from dataclasses import dataclass, field


# Classe pour gérer les statistiques vitales du joueur
@dataclass
class StatsManager:
    max_hp: int
    max_stamina: int
    current_hp: int = field(init=False)
    current_stamina: int = field(init=False)

    def __post_init__(self):
        self.current_hp = self.max_hp
        self.current_stamina = self.max_stamina

    def restore_hp(self, amount: int):
        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def restore_stamina(self, amount: int):
        self.current_stamina = min(self.current_stamina + amount, self.max_stamina)

    def take_damage(self, amount: int):
        self.current_hp = max(self.current_hp - amount, 0)

    def use_stamina(self, amount: int) -> bool:
        if self.current_stamina >= amount:
            self.current_stamina -= amount
            return True
        else:
            return False
