import random

from dataclasses import dataclass

from basic_monopoli.domain.ports.scoreboards import ScoreBoardPort
from basic_monopoli.domain.ports.rulers import RulerPort
from basic_monopoli.domain.models.groups import PropertyBoxGroup
from .boxes import (
    BasicPropertyBox,
    StartingBox,
    PropertyBox,
    ProbabilityBox,
    ChanceBox,
    RentOnlyBox,
    StationBox,
    PrisonBox,
    MultipliedPropertyBox,
    StepOnlyBox,
)


@dataclass
class SimpleScoreBoard(ScoreBoardPort):
    ruler: RulerPort

    def get_boxes(self):
        letters = ["a", "b", "c", "d"]
        indexes = list(range(1, 9))
        scoreboard_index = 0
        box_types = list(BasicPropertyBox.BoxType)
        for letter in letters:
            for index in indexes:
                box_name = f"{letter}-{index}"
                scoreboard_index += 1
                yield BasicPropertyBox(
                    name=box_name,
                    box_type=random.choice(box_types),
                    scoreboard=self,
                    ruler=self.ruler,
                )


@dataclass
class StandardScoreBoard(SimpleScoreBoard):
    def __post_init__(self):
        self.stations = self.get_stations()
        self.societies = self.get_societies()
        super().__post_init__()

    def get_stations(self):
        @dataclass
        class Stations:
            sud: StationBox
            ovest: StationBox
            nord: StationBox
            est: StationBox

        group = PropertyBoxGroup(name="Stations", color="white")
        stations: list[StationBox] = []
        cardinals = ["sud", "ovest", "nord", "est"]
        for cardinal in cardinals:
            station = StationBox(
                name=cardinal.capitalize(),
                scoreboard=self,
                ruler=self.ruler,
                group=group,
                base_rent=60,
                base_price=120,
                house_price=0,
                hotel_price=0,
            )
            stations.append(station)
        return Stations(*stations)

    def get_societies(self):
        @dataclass
        class Sociecies:
            electric: MultipliedPropertyBox
            water: MultipliedPropertyBox

        group = PropertyBoxGroup(name="Societies", color="white")
        societies: list[MultipliedPropertyBox] = []
        societies_names = ["Società elettrica", "Società Acqua Potabile"]
        for society_name in societies_names:
            society = StationBox(
                name=society_name,
                scoreboard=self,
                ruler=self.ruler,
                group=group,
                base_rent=60,
                base_price=120,
                house_price=0,
                hotel_price=0,
            )
            societies.append(society)
        return Sociecies(*societies)

    def get_pink_group(self):
        group = PropertyBoxGroup(name="Pink", color="pink")
        yield PropertyBox(
            group=group,
            name="Vicolo Corto",
            base_rent=70,
            base_price=60,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield ProbabilityBox(scoreboard=self, ruler=self.ruler)
        yield PropertyBox(
            group=group,
            name="Vicolo Stetto",
            base_rent=70,
            base_price=60,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield RentOnlyBox(
            name="Tassa patrimoniale",
            base_rent=self.ruler.get_loop_reward() / 2,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_light_blue_group(self):
        group = PropertyBoxGroup(name="Light Blue", color="lightblue")
        yield PropertyBox(
            group=group,
            name="Bastioni Gran Sasso",
            base_rent=80,
            base_price=100,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield ChanceBox(scoreboard=self, ruler=self.ruler)
        yield PropertyBox(
            group=group,
            name="Viale Monterosa",
            base_rent=80,
            base_price=100,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Viale Vesuvio",
            base_rent=120,
            base_price=110,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_orange_group(self):
        group = PropertyBoxGroup(name="Orange", color="orange")
        yield PropertyBox(
            group=group,
            name="Via Accademia",
            base_rent=110,
            base_price=140,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield self.societies.electric
        yield PropertyBox(
            group=group,
            name="Corso Ateneo",
            base_rent=110,
            base_price=140,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Piazza università",
            base_rent=160,
            base_price=110,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_brown_group(self):
        group = PropertyBoxGroup(name="Brown", color="brown")
        yield PropertyBox(
            group=group,
            name="Via Verdi",
            base_rent=140,
            base_price=180,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield ProbabilityBox(scoreboard=self, ruler=self.ruler)
        yield PropertyBox(
            group=group,
            name="Corso Raffaello",
            base_rent=140,
            base_price=180,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Piazza Dante",
            base_rent=160,
            base_price=200,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_red_group(self):
        group = PropertyBoxGroup(name="Red", color="red")
        yield PropertyBox(
            group=group,
            name="Via Marco Polo",
            base_rent=170,
            base_price=220,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield ChanceBox(scoreboard=self, ruler=self.ruler)
        yield PropertyBox(
            group=group,
            name="Corso Magellano",
            base_rent=170,
            base_price=220,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Largo Colombo",
            base_rent=190,
            base_price=240,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_yellow_group(self):
        group = PropertyBoxGroup(name="Yellow", color="yellow")
        yield PropertyBox(
            group=group,
            name="Viale Costantino",
            base_rent=200,
            base_price=260,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Viale Traiano",
            base_rent=200,
            base_price=260,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield self.societies.water
        yield PropertyBox(
            group=group,
            name="Piazza Giulio Cesare",
            base_rent=220,
            base_price=280,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_green_group(self):
        group = PropertyBoxGroup(name="Green", color="green")
        yield PropertyBox(
            group=group,
            name="Via Roma",
            base_rent=230,
            base_price=300,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Corso Impero",
            base_rent=230,
            base_price=300,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield ProbabilityBox(scoreboard=self, ruler=self.ruler)
        yield PropertyBox(
            group=group,
            name="Largo Augusto",
            base_rent=250,
            base_price=320,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_purple_group(self):
        group = PropertyBoxGroup(name="Purple", color="purple")
        yield ChanceBox(scoreboard=self, ruler=self.ruler)
        yield PropertyBox(
            group=group,
            name="£Viale dei Giardini",
            base_rent=270,
            base_price=350,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )
        yield RentOnlyBox(
            name="Tassa di lusso",
            base_rent=self.ruler.get_loop_reward(),
            scoreboard=self,
            ruler=self.ruler,
        )
        yield PropertyBox(
            group=group,
            name="Parco della Vittoria",
            base_rent=300,
            base_price=400,
            house_price=50,
            hotel_price=75,
            scoreboard=self,
            ruler=self.ruler,
        )

    def get_south_side(self):
        yield from self.get_pink_group()
        yield self.stations.sud
        yield from self.get_light_blue_group()

    def get_west_side(self):
        yield from self.get_orange_group()
        yield self.stations.ovest
        yield from self.get_brown_group()

    def get_north_side(self):
        yield from self.get_red_group()
        yield self.stations.nord
        yield from self.get_yellow_group()

    def get_east_side(self):
        yield from self.get_green_group()
        yield self.stations.est
        yield from self.get_purple_group()

    def get_boxes(self):
        yield StartingBox(name="START", scoreboard=self, ruler=self.ruler)
        yield from self.get_south_side()
        yield StepOnlyBox(name="Transito", scoreboard=self, ruler=self.ruler)
        yield from self.get_west_side()
        yield StepOnlyBox(name="Parcheggio", scoreboard=self, ruler=self.ruler)
        yield from self.get_north_side()
        yield PrisonBox(scoreboard=self, ruler=self.ruler)
        yield from self.get_east_side()
