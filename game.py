import pygame as p
import spritePro as s
from base_page import BasePage
from card_view import CardView
from card import Card
from deck import Deck
from typing import List
from page_type import PageType
from card_type import CardRank
import config
from message_bus import step


def test(**kwargs):
    s.debug_log("нажал", kwargs)


def change_scene_game_over():
    s.debug_log("GAME OVER", [255, 255, 255])
    s.scene.set_scene_by_name(PageType.GAME_OVER)


class Game(s.Scene):
    def __init__(self):
        self.is_anim = False
        self.pos1_deck = (200, s.WH_C.y)
        self.pos2_deck = (s.WH.x - 200, s.WH_C.y)
        self.pos1_hand = (s.WH_C.x, 200)
        self.pos2_hand = (s.WH_C.x, s.WH.y - 200)
        step.connect(self.step)
        step.connect(test)

        self.deck_cards1 = []
        self.deck_cards2 = []

        super().__init__()
        self.t_count_hand1 = s.TextSprite(
            "рука 1 ", 64, pos=(20, 20), anchor=s.Anchor.TOP_LEFT, scene=self
        )
        self.t_count_hand2 = s.TextSprite(
            "2 ruka",
            64,
            pos=s.WH + p.Vector2(-20, -20),
            anchor=s.Anchor.BOTTOM_RIGHT,
            scene=self,
        )
        self.player1_button = s.Button(
            "",
            (202, 300),
            self.pos1_hand,
            "",
            on_click=lambda: step.send(is_first_player=True),
            scene=self,
        )
        self.player2_button = s.Button(
            "",
            (202, 300),
            self.pos2_hand,
            "",
            on_click=lambda: step.send(is_first_player=False),
            scene=self,
        )
        self.player1_button.alpha = 0
        self.player2_button.alpha = 0

    def on_enter(self):
        self.deck = Deck(config.min_card)
        self.card_list = []
        self.player1_cards: List[CardView] = []
        self.player2_cards: List[CardView] = []

        self.deck.shuffle()

        self.create_cards()

    def update(self, dt):
        self.t_count_hand1.set_text(f"рука 1 {self.player1_cards.__len__()} карт")
        self.t_count_hand2.set_text(f"рука 2 {self.player2_cards.__len__()} карт")

    def create_cards(self):
        s.debug_log("create card")
        counter = 0
        card = self.deck.get_card()
        while card is not None:
            which_player = counter % 2 == 0
            pos = self.pos1_hand if which_player else self.pos2_hand
            card_view = CardView(card, pos, scene=self)
            if which_player:
                self.player1_cards.append(card_view)
            else:
                self.player2_cards.append(card_view)
            card = self.deck.get_card()
            counter += 1

    def step(self, is_first_player: bool):
        if (
            self.is_anim
            or (self.player1_cards.__len__() == 0 and is_first_player)
            or (self.player2_cards.__len__() == 0 and not is_first_player)
        ):
            return
        s.debug_log("step")

        player_cards = self.player1_cards if is_first_player else self.player2_cards

        if is_first_player:
            if len(self.deck_cards1) + 1 - len(self.deck_cards2) >= 2:
                return
        else:
            if len(self.deck_cards2) + 1 - len(self.deck_cards1) >= 2:
                return
        s.audio_manager.play_sound("sounds\mb_card_deal_08.mp3")
        card = player_cards.pop(0)
        self._animation(is_first_player, card)

        if is_first_player:
            self.deck_cards1.append(card)
            card.sorting_order = self.deck_cards1.__len__()
        else:
            self.deck_cards2.append(card)
            card.sorting_order = self.deck_cards2.__len__()

        if len(self.deck_cards1) == len(self.deck_cards2):
            self._battle()

    def _battle(self):
        s.debug_log("battle")
        card1 = self.deck_cards1[-1].card
        card2 = self.deck_cards2[-1].card
        if card1 == card2  and self.player1_cards.__len__()!=0 and self.player2_cards.__len__()!=0:
            return
        s.Timer(1, self._move_to_winner)
        self.is_anim = True

    def _move_to_winner(self):
        
        card1:Card = self.deck_cards1[-1].card
        card2:Card = self.deck_cards2[-1].card

        s.debug_log_custom("[BATTLE]",f"{card1.rank.name} {card2.rank.name}",(255,200,200))
        is_first_win = card1>card2
        player_cards = self.player1_cards if is_first_win else self.player2_cards
        s.debug_log(f"выиграл{is_first_win}")
        final_pos = self.pos1_hand if is_first_win else self.pos2_hand
        s.debug_log_custom("[BATTLE]",f"карты ушли в {final_pos}",[0,255,0])
        cards = self.deck_cards1 + self.deck_cards2
        for i, cardView in enumerate(cards):
            player_cards.append(cardView)
            s.debug_log_warning(
                f"for power{cardView.card.rank},current_pos {cardView.position}, pos{final_pos}"
            )
            cardView.move(final_pos, 0.4 * i, False)
            if i == cards.__len__() - 1:
                s.Timer(0.4 * i + 0.7, self._off_anim)
        self.deck_cards1.clear()
        self.deck_cards2.clear()
        self.is_game_over()

    def _animation(self, is_first_player, card):
        s.debug_log("animation")
        card.set_visible(True)
        final_pos = self.pos1_deck if is_first_player else self.pos2_deck
        card.move(final_pos)

    def is_game_over(self):
        if self.player1_cards.__len__() == 0 or self.player2_cards.__len__() == 0:
            self.game_over()

    def game_over(self):
        s.Timer(2, change_scene_game_over)

    def _off_anim(self):
        self.is_anim = False
