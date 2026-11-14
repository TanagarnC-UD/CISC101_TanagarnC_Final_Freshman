from dataclasses import dataclass
from drafter import *
from bakery import assert_equal
import random

set_website_title("Dungeon Game")
set_site_information(
    author="Tanagarn Chanpreechakul",
    description="Gacha game test with random battle mechanics",
    sources="Thanks to the Drafter docs and CISC101 LLM.",
    planning=["CISC101 Final Project Plan.pdf", "CISC101 Final Project Design.pdf"],
    links=["https://github.com/TanagarnC-UD/CISC101_TanagarnC_Final_Freshman"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Unit:
    """
    Unit format.
    
    Attributes:
    name: str - Self-explainatory.
    rarity: int - Rarity. Higher number, lower chance to pull. Multiplies attack_power in damage calculations.
    attack_power: int - Attack stat.
    unit_id: int - Self-explainatory.
    """
    name:  str
    rarity: int
    attack_power: int
    unit_id: int


@dataclass
class State:
    """
    Memory of the game.

    Attributes:
        gold: int - Currency used to pull units.
        enemy_hp: int - Current enemy hit points.
        enemies_defeated: int - How many enemies defeated. Used to scale maximium enemy_hp for each proceeding enemy.
        party: list[Unit] - Current units in a party.
        roster: list[Unit] - Currently owned units.
        question_data: list[int] - Math question data. Composed of three integers. See the earn route's functions.
        correct_answer: int - The correct answer to the math question.
        units_rolled_total: int - Creates new unit IDs everytime a unit is rolled.
    """
    gold: int
    enemy_hp: int
    enemies_defeated: int
    party: list[Unit]
    roster: list[Unit]
    question_data: list[int]
    correct_answer: int
    units_rolled_total: int

@route
def index(state: State) -> Page:
    """
    Main operations page. Shows current amount of gold and buttons to earn, roll, look at roster, and battle.
    
    Arguments:
        state:(State) - State dataclass memory.
    Returns:
        Page: Home menu of the game.
    """
    return Page(state, [
                Header("Dungeon Game"),
                Row("You currently have " + str(state.gold) + " gold."),
                Row(
                    Button("Earn Gold", earn),
                    Button("Recruitment", recruitment),
                    Button("Roster", roster),
                    Button("Battle", formation)
                    )
                ])

def question_maker() -> list[int]:
    """
    Outputs a randomized list of three integers for question_solver() to use.
    Element 0 is the operation (0 to 3).
        0 - Addition
        1 - Subtraction
        2 - Mutliplication
        3 - Exponential
    Element 1 is the first number.
    Element 2 is the second number.
    
    Arguments:
    
    Returns:
        list[int] - [operation, first number, second number]
    Notice:
        Can not unit test because it is too random.
    """
    operation = random.randint(0,3)
    question_data = []
    adding_subtracting_random_a = random.randint(-20,20)
    adding_subtracting_random_b = random.randint(-20,20)
    multiplying_random_a = random.randint(-10,10)
    multiplying_random_b = random.randint(-10,10)
    base_random = random.randint(-10,10)
    power_random = random.randint(0,3)
    if base_random == 0:
        power_random = random.randint(1,3)
        
    if operation == 0:
        question_data = [operation, adding_subtracting_random_a, adding_subtracting_random_b]
    elif operation == 1:
        question_data = [operation, adding_subtracting_random_a, adding_subtracting_random_b]
    elif operation == 2:
        question_data = [operation, multiplying_random_a, multiplying_random_b]
    elif operation == 3:
        question_data = [operation, base_random, power_random]
    return question_data
    
def question_solver(operation: int, element_a: int, element_b: int) -> int:
    """
    Uses the returned list made by question_maker() to solve for the answer.
    
    Arguments:
        operation: int - The math operation.
            0 - Addition
            1 - Subtraction
            2 - Mutliplication
            3 - Exponential
        element_a: int: First number.
        element_b: int: Second number.
    Returns:
        int - The answer.
    """
    answer = 0
    if operation == 0:
        answer = element_a + element_b
    elif operation == 1:
        answer = element_a - element_b
    elif operation == 2:
        answer = element_a * element_b
    elif operation == 3:
        answer = element_a ** element_b
    return answer

@route
def earn(state: State)  -> Page:
    """
    The page where the user could earn gold.
    Creates a randomized math question, displays it, and uses question_solver() to solve it.
    Waits for user input, and gives gold if input matches the answer.
    
    Arguments:
        state:(State) - State dataclass memory.
    Returns:
        Page: Sends to simple, randomized math question with textbox.
    Notice:
        Can not unit test because it is too random.
    """
    question_data = question_maker()
    state.question_data = question_data
    state.correct_answer = question_solver(question_data[0], question_data[1], question_data[2])
    
    if question_data[0] == 0:
        operation_sign = " + "
    elif question_data[0] == 1:
        operation_sign = " - "
    elif question_data[0] == 2:
        operation_sign = " * "
    elif question_data[0] == 3:
        operation_sign = " ^ "
    
    return Page(state, [
                Header("Earn Gold"),
                Row(str(question_data[1]), operation_sign, str(question_data[2])),
                Row(TextBox("user_answer")),
                Row(Button("Submit", check_answer))
                ])

@route
def check_answer(state: State, user_answer: str)  -> Page:
    """
    Checks answer.
    
    Arguments:
        state: State - State dataclass memory.
        user_answer: int - User input from the data.
    Returns:
        Page: Shows if right or not.
    """
    if user_answer == str(state.correct_answer):
        state.gold = state.gold + 50
        return Page(state, [
                    Header("Earn Gold"),
                    Row("Correct! You now have " + str(state.gold) + " gold."),
                    Row(
                        Button("Return", index),
                        Button("Try Again", earn)
                        )
                    ])
    else:
        return Page(state, [
                    Header("Earn Gold"),
                    Row("Incorrect! The answer was " + str(state.correct_answer) + "."),
                    Row(
                        Button("Return", index),
                        Button("Try Again", earn)
                        )
                    ])
    
@route
def recruitment(state: State)  -> Page:
    """
    Opens recruitment menu
    
    Arguments:
        state: State - State dataclass memory.
    Returns:
        Page: Recruitment page.
    """
    return Page(state, [
                Header("Recruitment"),
                Row("You currently have " + str(state.gold) + " gold."),
                Row("How many units would you like to recruit?"),
                Row("Recruiting ten at once guarantees at least one Grade 2 rarity unit."),
                Row(SelectBox("amount_rolling", ["1 Roll - 10 Gold", "10 Rolls - 100 Gold"], "1 Roll - 10 Gold")),
                Row(
                    Button("Return", index),
                    Button("Confirm", rolling)
                        )
                ])

def random_roll(state: State, current_roll: int) -> Unit:
    """
    Randomly creates a Unit.
    
    Arguments:
        current_roll: int - Used to figure out if user is rolling ten at once, so guaranteeing the 10th unit is at least rarity 2.
    Returns:
        Unit - The created Unit.
    Notice:
        Can not unit test because it is too random.
    """
    class_roll = random.randint(0, 2)
    rarity_roll = random.randint(1, 1000)
    if current_roll == 10:
        if rarity_roll >= 50:
            rarity = 3
        else:
            rarity = 2
    else:
        if rarity_roll >= 800:
            if rarity_roll >= 950:
                rarity = 3
            else:
                rarity = 2
        else:
            rarity = 1
    if class_roll == 0:
        return Unit("Sword Guy", rarity, 50, state.units_rolled_total)
    if class_roll == 1:
        return Unit("Shield Guy", rarity, 20, state.units_rolled_total)
    if class_roll == 2:
        return Unit("Bow Guy", rarity, 70, state.units_rolled_total)

@route
def rolling(state: State, amount_rolling: str)  -> Page:
    """
    Checks if user has enough gold and shows results
    
    Arguments:
        state: State - State dataclass memory.
        amount_rolling: str - 1 or 10 rolls.
    Returns:
        Page: Rolling page.
    Notice:
        Can not unit test because it is too random.
    """
    min_gold_one_roll = 10
    min_gold_ten_roll = 100
    roll_results = []
    current_roll = 0
    if amount_rolling == "1 Roll - 10 Gold":
        if state.gold < min_gold_one_roll:
            return Page(state, [
                        Header("Recruitment"),
                        Row("You don't have enough gold."),
                        Row(Button("Return", index))
                        ])
        else:
            state.gold = state.gold - 10
            while current_roll < 1:
                current_roll = current_roll + 1
                state.units_rolled_total = state.units_rolled_total + 1
                roll_results.append(random_roll(state, current_roll))
            for unit in roll_results:
                state.roster.append(unit)
            return Page(state, [
                        Header("Recruitment"),
                        Row(Table([
                            [roll_results[0].name, roll_results[0].rarity]],
                            ["Name", "Rarity"]
                            )),
                        Row(Button("Return", index))
                        ])
    elif amount_rolling == "10 Rolls - 100 Gold":
        if state.gold < min_gold_ten_roll:
            return Page(state, [
                        Header("Recruitment"),
                        Row("You don't have enough gold."),
                        Row(Button("Return", index))
                        ])
        else:
            state.gold = state.gold - 100
            while current_roll < 10:
                current_roll = current_roll + 1
                state.units_rolled_total = state.units_rolled_total + 1
                roll_results.append(random_roll(state, current_roll))
            for unit in roll_results:
                state.roster.append(unit)
            return Page(state, [
                        Header("Recruitment"),
                        Row(Table([
                            [roll_results[0].name, roll_results[0].rarity],
                            [roll_results[1].name, roll_results[1].rarity],
                            [roll_results[2].name, roll_results[2].rarity],
                            [roll_results[3].name, roll_results[3].rarity],
                            [roll_results[4].name, roll_results[4].rarity],
                            [roll_results[5].name, roll_results[5].rarity],
                            [roll_results[6].name, roll_results[6].rarity],
                            [roll_results[7].name, roll_results[7].rarity],
                            [roll_results[8].name, roll_results[8].rarity],
                            [roll_results[9].name, roll_results[9].rarity]],
                            ["Name", "Rarity"]
                            )),
                        Row("You now have " + str(state.gold) + " gold."),
                        Row(Button("Return", index))
                        ])

@route
def roster(state: State)  -> Page:
    """
    Shows current owned units
    
    Arguments:
        state: State - State dataclass memory.
    Returns:
        Page: Roster page.
    """    
    return Page(state, [
                Header("Roster"),
                Row("You own " + str(len(state.roster)) + " units total."),
                Row(Table([
                    [unit.name, unit.rarity, unit.attack_power]
                    for unit in state.roster],
                    ["Name", "Rarity", "Attack Power"]
                    )),
                Row(Button("Return", index))
                ])

@route
def formation(state: State)  -> Page:
    """
    Allows to form a party.
    
    Arguments:
        state: State - State dataclass memory.
    Returns:
        Page: Forming a party page.
    """
    state.party = []
    if state.roster:
        return Page(state, [
                Header("Party Formation"),
                Row("You own " + str(len(state.roster)) + " units total."),
                Row("You may select up to 10 units to form a party."),
                Row(Table([
                    [RelatedCheckBox("party", str(unit.unit_id)), unit.name, unit.rarity, unit.attack_power, unit.unit_id]
                    for unit in state.roster],
                    ["Select", "Name", "Rarity", "Attack Power", "ID"]
                    )),
                Row(Button("Return", index), Button("Proceed", battle))
                ])
    else:
        return Page(state, [
                Header("Party Formation"),
                Row("You have no units."),
                Row(Button("Return", index))
                ])

@route
def battle(state: State, party: list[str])  -> Page:
    """
    Checks if party has 1 to 10 members. If yes, allows the user to proceed.
    
    Arguments:
        state: State - State dataclass memory.
        party: list[str] - The party the user has assigned.
    Returns:
        Page: Party check page.
    """
    if len(party) == 0:
        return Page(state, [
                Header("Party Formation"),
                Row("You can't enter battle with no party members."),
                Row("You may select up to 10 units to form a party"),
                Row(Button("Return", index))
                ])
    elif len(party) > 10:
        return Page(state, [
                Header("Party Formation"),
                Row("You may only enter battle with no more than 10 party members."),
                Row("You assigned " + str(len(party) - 10) + " too many units to the party."),
                Row(Button("Return", index))
                ])
    else:
        removed_party_roster = []
        for unit in state.roster:
            if str(unit.unit_id) in party:
                state.party.append(unit)
            else:
                removed_party_roster.append(unit)
        state.roster = removed_party_roster
        return Page(state, [
                Header("Battle"),
                Row("Enemy " + str(state.enemies_defeated + 1) + " appears with " + str(state.enemy_hp) + " hit points!"),
                Row(Button("Proceed", battle_proceed))
                ])
    
def damage_calcuations(team: list[Unit]) -> float:
    """
    Calculates damage.
    
    Arguments:
        team: list[Unit] - The current party of user. Used team instead to avoid errors with checkbox.
    Returns:
        float - Damage
    """
    damage = 0
    half = 0.5
    for unit in team:
        damage = damage + (unit.attack_power * (unit.rarity * half))
    return damage

def hit_chance_calculations(team: list[Unit]) -> int:
    """
    Calculates hit chance for success.
    
    Arguments:
        team: list[Unit] - The current party of user. Used team instead to avoid errors with checkbox.
    Returns:
        int - Hit chance for success.
    """
    hit_chance = 0
    base_chance = 3
    two_base_add = 5
    three_base_add = 9
    rarity_two_total = 0
    rarity_three_total = 0
    for unit in team:
        if unit.rarity == 2:
            rarity_two_total = rarity_two_total + 1
        if unit.rarity == 3:
            rarity_three_total = rarity_three_total + 1
    for unit in team:
        hit_chance = hit_chance + (base_chance * unit.rarity)
    hit_chance = hit_chance + (two_base_add * rarity_two_total) + (three_base_add * rarity_three_total)
    if hit_chance > 95:
        hit_chance = 95
    return hit_chance

@route
def battle_proceed(state: State) -> Page:
    """
    Gets damage and success hit chance, and rolls actual chance of hitting.
    If the actual hit chance is lower or equal to the success, then it counts as a hit.
    Lets the enemy take damage and spawn a new enemy if the enemy is defeated.
    Clears the party after result.
    
    Arguments:
        state: State - State dataclass memory.
    Returns:
        Page: Forming a party page.
    Notice:
        Can not unit test because it is too random.
    """
    damage = damage_calcuations(state.party)
    hit_chance = hit_chance_calculations(state.party)
    roll_chance = random.randint(1,100)
    state.party = []
    if roll_chance <= hit_chance:
        state.enemy_hp = state.enemy_hp - damage
        if state.enemy_hp <= 0:
            base_reward = 50
            base_health_scale = 50
            state.enemies_defeated = state.enemies_defeated + 1
            state.enemy_hp = 100 + (base_health_scale * (state.enemies_defeated + 1))
            state.gold = state.gold + (base_reward * state.enemies_defeated)
            return Page(state, [
                    Header("Battle"),
                    Row("Enemy defeated!"),
                    Row("You will fight Enemy " + str(state.enemies_defeated + 1) + " next."),
                    Row("Earned " + str(base_reward * state.enemies_defeated) + " gold."),
                    Row(Button("Return", index))
                    ])
        else:
            return Page(state, [
                    Header("Battle"),
                    Row("Attack success!"),
                    Row("Enemy " + str(state.enemies_defeated + 1) + " survives with " + str(state.enemy_hp) + " hit points left."),
                    Row(Button("Return", index))
                    ])
    else:
        return Page(state, [
                Header("Battle"),
                Row("Attack failed..."),
                Row("Enemy " + str(state.enemies_defeated + 1) + " leaves with " + str(state.enemy_hp) + " hit points left."),
                Row(Button("Return", index))
                ])
    
#Unit tests. Used the LLM for this, because I'm pretty sure it works fine.
assert_equal(question_solver(0, 5, 3), 8)
assert_equal(question_solver(1, 5, 3), 2)
assert_equal(question_solver(2, 5, 3), 15)
assert_equal(question_solver(3, 2, 3), 8)
assert_equal(question_solver(0, -5, 3), -2)
assert_equal(question_solver(3, 5, 0), 1)

unit1 = Unit("Sword Guy", 1, 50, 1)
unit2 = Unit("Bow Guy", 2, 70, 2)
unit3 = Unit("Shield Guy", 3, 20, 3)

assert_equal(damage_calcuations([unit1]), 25.0)
assert_equal(damage_calcuations([unit2]), 70.0)
assert_equal(damage_calcuations([unit3]), 30.0)
assert_equal(damage_calcuations([unit1, unit2, unit3]), 125.0)
assert_equal(damage_calcuations([]), 0)

assert_equal(hit_chance_calculations([]), 0)
assert_equal(hit_chance_calculations([unit1]), 3)
assert_equal(hit_chance_calculations([unit2]), 11)
assert_equal(hit_chance_calculations([unit3]), 18)
assert_equal(hit_chance_calculations([unit1, unit2, unit3]), 32)
large_team = [Unit("Sword Guy", 3, 50, i) for i in range(1, 11)]
assert_equal(hit_chance_calculations(large_team), 95)

test_check_answer = State(0, 100, 0, [], [], [], 8, 0)
check_answer(test_check_answer, "8")
assert_equal(test_check_answer.gold, 50)
test_check_answer.gold = 0
check_answer(test_check_answer, "7")
assert_equal(test_check_answer.gold, 0)

test_battle1 = State(0, 100, 0, [], [], [], 0, 0)
battle(test_battle1, [])
assert_equal(test_battle1.party, [])
assert_equal(test_battle1.roster, [])

test_state = State(100, 100, 0, [unit2], [unit1], [0, 1, 1], 2, 0)
page_index = index(test_state)
assert_equal(page_index.state.gold, 100)

page_recruitment = recruitment(test_state)
assert_equal(page_recruitment.state.gold, 100)

page_roster = roster(test_state)
assert_equal(len(page_roster.state.roster), 1)

page_formation = formation(test_state)
assert_equal(len(page_formation.state.roster), 1)
assert_equal(page_formation.state.party, [])

test_units_battle = [
        Unit("Sword Guy", 1, 50, i)
        for i in range(1, 12)
    ]
test_battle_new = State(100, 100, 0, [], test_units_battle, [], 0, 11)
test_party_ids = [str(i) for i in range(1, 12)]
page_battle = battle(test_battle_new, test_party_ids)
assert_equal(len(page_battle.state.roster), 11)
assert_equal(len(page_battle.state.party), 0)

test_battle_valid = State(100, 100, 0, [], [unit1, unit2, unit3], [], 0, 3)
page_battle_valid = battle(test_battle_valid, ["1", "2"])
assert_equal(len(page_battle_valid.state.party), 2)
assert_equal(len(page_battle_valid.state.roster), 1)
assert_equal(page_battle_valid.state.roster[0].unit_id, 3)

starting = State(0, 100, 0, [], [], [], 0, 0)
start_server(starting)
    
