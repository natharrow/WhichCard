from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Card
from django.shortcuts import redirect
from cards.forms import CreditForm
from .object import ChosenCards
import operator
# Create your views here.


def home(request):
    return render(request, 'cards/homepage.html')


def get_display_cards(request):
    return render(request, 'cards/display_cards.html')


def get_info(request):
    # if this is a POST request we need to process the form data
    print("IN THE FORM")  # testing if we're in the method
    if request.method == 'POST':
        print("FORM IS VALID---")  # testing whether  form can be submitted
        # create a form instance and populate it with data from the request:
        form = CreditForm(request.POST)
        if form.is_valid():
            # extract the data from the form.cleaned_data
            groceries = form.cleaned_data['groceries']
            dining_out = form.cleaned_data['dining']
            gas = form.cleaned_data['gas']
            travel = form.cleaned_data['travels']
            everything_else = form.cleaned_data['etc']
            listofcards=get_best_cards(groceries, dining_out, gas, travel, everything_else)
            context = {}
            context['listofcards'] = listofcards
            return render(request, 'cards/forms.html', context)
            #return render(request, 'cards/display_cards.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreditForm()
    return render(request, 'cards/forms.html', {'form': form})



# The method will likely be split
def get_best_cards(grocery_input, dining_out_input, gas_input, travel_input, everything_else_input):
    cards_by_value = ChosenCards()
    card_set = Card.objects.all()

    for card in card_set:
        card_value = float(calculate_card_value(card, grocery_input, dining_out_input, gas_input, travel_input,
                                          everything_else_input))
        print("%s value: %d" %(card.cardName, card_value))
        cards_by_value.chosen_cards[card.cardName] = card_value

    print('Before sorting:')
    print(cards_by_value.chosen_cards)

    sorted_cards = sort_cards_by_value(cards_by_value.chosen_cards)

    print('After sorting:')
    print(sorted_cards)
    listofcards = list(sorted_cards.keys())
    return listofcards


def calculate_card_value(card, grocery_input, dining_out_input, gas_input, travel_input, everything_else_input):
    card_grocer_multiplier = card.groceryMultiplier
    card_restaurant_multiplier = card.restaurantMultiplier
    card_gas_multiplier = card.gasMultiplier
    card_travel_multiplier = card.travelMultiplier
    card_everything_else_multiplier = card.everythingElse
    card_reward_value = card.rewardValue
    card_annual_fee = card.annualFee

    card_value = float((((grocery_input * card_grocer_multiplier) + (dining_out_input * card_restaurant_multiplier)
                   + (gas_input * card_gas_multiplier) + (travel_input * card_travel_multiplier)
                   + (everything_else_input * card_everything_else_multiplier)) * card_reward_value) - card_annual_fee)

    return card_value


def sort_cards_by_value(cards):
    return dict(sorted(cards.items(), key=operator.itemgetter(1), reverse=True))


def about_us(request):
    return render(request, 'cards/AboutUs.html')
