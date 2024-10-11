class StatsManager:
    def __init__(self, max_hp: int, max_stamina: int, max_mh: int):
        self.max_hp: int = max_hp
        self.max_stamina: int = max_stamina
        self.current_hp: int = max_hp
        self.current_stamina: int = max_stamina
        self.max_mh: int = max_mh
        self.current_mh: int = max_mh

    def take_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

    def restore_hp(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def use_stamina(self, amount: int) -> bool:
        if self.current_stamina >= amount:
            self.current_stamina -= amount
            return True
        return False

    def restore_stamina(self, amount: int):
        self.current_stamina = min(self.max_stamina, self.current_stamina + amount)

    def lose_mental_health(self, amount: int):
        self.current_mh = min(self.max_mh, self.current_mh - amount)

    def restore_mental_health(self, amount: int):
        self.current_mh = min(self.max_mh, self.current_mh + amount)

    def update_stats(self, max_hp: int, max_stamina: int, max_mental: int):
        self.max_hp = max_hp
        self.max_stamina = max_stamina
        self.max_mental = max_mental
        self.current_hp = min(self.current_hp, self.max_hp)
        self.current_stamina = min(self.current_stamina, self.max_stamina)
        self.max_mental = min(self.current_mh, self.max_mh)

    def is_dead(self):
        return self.current_hp <= 0
