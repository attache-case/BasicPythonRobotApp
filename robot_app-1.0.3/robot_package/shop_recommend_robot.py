import os
import string
import csv

from robot_package.robot import Robot
from .utils import msg_template_reader

csv_file_name = 'ranking.csv'


class ShopRecommendRobot(Robot):

    msg_ask_user_name_template = msg_template_reader\
        .get_template_from_file('robot_package/texts/msg_ask_user_name_template.txt')
    msg_ask_agreement_for_restaurant_template = msg_template_reader \
        .get_template_from_file('robot_package/texts/msg_ask_agreement_for_restaurant_template.txt')
    msg_ask_favorite_restaurant_template = msg_template_reader\
        .get_template_from_file('robot_package/texts/msg_ask_favorite_restaurant_template.txt')

    def __init__(self, name='Shop Recommend Robot'):
        super().__init__(name)
        self._user_name = None

        if os.path.exists(csv_file_name) and os.path.isfile(csv_file_name):
            with open(csv_file_name, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                self.restaurant_ranking = {row['RestaurantName']: int(row['Count']) for row in reader}
        else:
            self.restaurant_ranking = {}

        self.restaurant_ranking = \
            {k: v for k, v in sorted(self.restaurant_ranking.items(), key=lambda x: -x[1])}

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name

    def ask_user_name(self):
        msg_ask_user_name = string.Template(self.msg_ask_user_name_template)
        msg_ask_user_name = msg_ask_user_name.substitute(robot_name=self.name)
        while True:
            super().print_msg(msg_ask_user_name)
            user_name_input = input()
            if user_name_input:
                self._user_name = user_name_input
                break

    def ask_agreement_for_restaurant(self, restaurant_name):
        msg_ask_agreement_for_restaurant = string.Template(self.msg_ask_agreement_for_restaurant_template)
        msg_ask_agreement_for_restaurant = msg_ask_agreement_for_restaurant.substitute(restaurant_name=restaurant_name)
        while True:
            super().print_msg(msg_ask_agreement_for_restaurant)
            yn_input = input()
            if yn_input in ['Yes', 'Y', 'y']:
                self.restaurant_ranking[restaurant_name] += 1
                break
            elif yn_input in ['No', 'N', 'n']:
                break
            else:
                continue

    def recommend_restaurant(self):
        for restaurant_name in self.restaurant_ranking.keys():
            self.ask_agreement_for_restaurant(restaurant_name)

    def ask_favorite_restaurant(self):
        msg_ask_favorite_restaurant = string.Template(self.msg_ask_favorite_restaurant_template)
        msg_ask_favorite_restaurant = msg_ask_favorite_restaurant.substitute(user_name=self._user_name)
        while True:
            super().print_msg(msg_ask_favorite_restaurant)
            favorite_restaurant_input = input()
            if favorite_restaurant_input:
                restaurant_name = favorite_restaurant_input.title()
                if restaurant_name in self.restaurant_ranking:
                    self.restaurant_ranking[restaurant_name] += 1
                else:
                    self.restaurant_ranking[restaurant_name] = 1
                break

    def qa(self):
        self.recommend_restaurant()
        self.ask_favorite_restaurant()

    def run(self):
        self.ask_user_name()
        self.qa()

    def __del__(self):
        with open(csv_file_name, 'w') as csv_file:
            field_names = ['RestaurantName', 'Count']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for restaurant_name, count in self.restaurant_ranking.items():
                writer.writerow({'RestaurantName': restaurant_name, 'Count': count})
